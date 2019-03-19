import requests
import itertools
import json
import codecs
import time
from pprint import pprint


class User:
    def __init__(self, id):
        self.id = id

    def get_params(self):
        return dict(user_id=self.id, access_token=TOKEN, v=5.92)

    def get_all_data(self,d,f):
        params = {'access_token': TOKEN, 'v': 5.92,
                  'code': ''
                          'var groups = API.groups.get({user_id:'+str(self.id)+'}).items;' # группы User
                          'var counts = API.groups.get({user_id:'+str(self.id)+'}).count;' # количество групп User
                           'var usr_friends = API.friends.get({user_id:'+str(self.id)+'}).items;'
                           'var i=5*' +str(d)+';'
                           'var friends_group_list=[];'
                          'while (i <(5+5*'+str(d)+'+' +str(f)+')){'
                            'var friend = usr_friends[i];'
                            'var fr_groups = API.groups.get({user_id: friend}).items;'
                             'friends_group_list = friends_group_list + [fr_groups];'
                             'i = i+1;'
                                                                               '};'
                            'return {"groups":groups, "fr_group":friends_group_list, "usr_friends":usr_friends};'
                        }
        try:
            response = requests.get(
                'https://api.vk.com/method/execute',
                params
            )
            time.sleep(0.33)
            return response.json()
        except Exception as e:
            print(e)


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
    output_dict = {}
    out_groups = []
    N = input('Введите N, оно будет равняться максимальному количеству друзей которые состоят в группах, которые выдаст Программа  ')
    user_input = input('Введите id или имя пользователя: ')
    user = get_user(user_input)
    d = 0
    y = 0

    output_dict = user.get_all_data(d,y)
    groups_list = output_dict['response']['groups']
    fr_group_list = []
    usr_friends_list = output_dict['response']['usr_friends']
    d = len(usr_friends_list)//5 # понимаем сколько раз запрашивать список членов групп
    f = len(usr_friends_list)%5
    i = 0
    while i < d:
        if (i + 1) == d:
            y = f
        print('- - -')
        output_dict = user.get_all_data(i,y)
        i += 1
        z = 0
        while z <= (len(output_dict['response']['fr_group'])-1):
            fr_group_list.append(output_dict['response']['fr_group'][z])
            z += 1


    pprint(usr_friends_list[185])
    #print(groups_list)
    pprint(fr_group_list[185])




#    list_to_json(output_list_json, 'groups_com.json')
#    print('ID групп, в которых есть общие друзья, но не более чем {} человек  '.format(N), output_list)

if __name__ == "__main__":
    with open('token.json', 'r') as file:
        data = json.load(file)
        TOKEN = data[0]['token']

    main()