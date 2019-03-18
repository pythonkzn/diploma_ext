import requests
import itertools
import json
import codecs
import time


class User:
    def __init__(self, id):
        self.id = id

    def get_params(self):
        return dict(user_id=self.id, access_token=TOKEN, v=5.92)

    def get_all_data(self):
        params = {'access_token': TOKEN, 'v': 5.92,
                  'code': 'return [API.groups.get({user_id:'+str(self.id)+'})];'}
        response = requests.get(
            'https://api.vk.com/method/execute',
            params
        )
        time.sleep(0.33)
        return response.json()['response']

    def common_group_list_n_fr(self, n):
        friends_group_list = []
        output_list = []
        groups_list = self.get_all_data()[0]['items'] # список групп User
        i = 0
        for group in groups_list:
            i += 1
            params = {'access_token': TOKEN, 'v': 5.92,
                      'code': 'return [API.groups.getMembers({group_id:' + str(group) + ', filter: "friends"})];'}
            try:  # обходим случаи по которым запрос не отвечает ожидаемым форматом
                response_get_friends = requests.get('https://api.vk.com/method/execute', params) # получаем список друзей которые в группе
                friends_group_list = response_get_friends.json()['response'][0]['items']
                if len(friends_group_list) <= n:
                    output_list.append(group)
                print('-','Осталось обработать {} групп'.format(i) ,' из {}'.format(self.get_all_data()[0]['count']))
                time.sleep(0.33)
            except Exception as e:
                print(e)  # выводим полученные ошибки от API VK
        return output_list

class Group:
    def __init__(self, id):
        self.id = id

    def get_params(self):
        return {
            'group_id': self.id,
            'fields': 'members_count',
            'access_token': TOKEN,
            'v': 5.92
        }

    def get_group_data(self):
        params = self.get_params()
        response_get_group = requests.get(
            'https://api.vk.com/method/groups.getById',
            params
        )
        group_data_dict = response_get_group.json()['response'][0]
        output_dict = {'name': group_data_dict['name'],
                       'gid': group_data_dict['id'],
                       'members_count': group_data_dict['members_count']}
        return output_dict

def get_user(usr_in):
    try:
        int(usr_in)
        user = User(usr_in)
    except ValueError:
        params = {
            'user_ids': usr_in,
            'access_token': TOKEN,
            'v': 5.92
        }
        response_get_id = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        user = User(int(response_get_id.json()['response'][0]['id']))  # получили по имени пользователя его id
    return user

def get_output_data(unc_gr):
    output_list = []
    for group in unc_gr:
        try:
            group = Group(group)
            output_list.append(group.get_group_data())
        except Exception as e:
            pass
    return output_list

def list_to_json(list, path_f):
    with codecs.open(path_f, 'w', encoding='utf-8') as json_file:
        json.dump(list, json_file, ensure_ascii=False)

def main():
    N = input('Введите N, оно будет равняться максимальному количеству друзей которые состоят в группах, которые выдаст Программа  ')
    user_input = input('Введите id или имя пользователя: ')
    user = get_user(user_input)
    common_groups = user.common_group_list_n_fr(int(N)) # получили список групп в которых есть общие друзьч не более N человек
    output_list_com = get_output_data(common_groups)
    list_to_json(output_list_com, 'groups_com.json')
    print('ID групп, в которых есть общие друзья, но не более чем {} человек  '.format(N), common_groups)

if __name__ == "__main__":
    with open('token.json', 'r') as file:
        data = json.load(file)
        TOKEN = data[0]['token']

    main()