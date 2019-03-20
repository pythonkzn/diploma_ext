import requests
import itertools
import json
import codecs
import time
from pprint import pprint


class User:
    def __init__(self, id):
        self.id = id

    def get_all_data(self, d, f):
        params = {'access_token': TOKEN, 'v': 5.92,
                  'code': ''
                          'var groups =API.groups.get({user_id:' + str(self.id) + '}).items;'  # группы User
                          'var counts = API.groups.get({user_id:' + str(self.id) + '}).count;'  # количество групп User
                          'var usr_friends = API.friends.get({user_id:' + str(self.id) + '}).items;'
                          'var i=5*' + str(d) + ';'
                          'var friends_group_list=[];'
                          'while (i <(5+5*' + str(d) + '+' + str(f) + '))'
                                         '{''var friend = usr_friends[i];'
                                         'var fr_groups = API.groups.get({user_id: friend}).items;'  # группы  друзей
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
            print(response.json())


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


def get_output_list(usr, nn):
    d = 0
    y = 0
    output_dict = usr.get_all_data(d, y)
    groups_list = output_dict['response']['groups']
    fr_group_list = []
    usr_friends_list = output_dict['response']['usr_friends']  # формируем список id друзей User
    d = len(usr_friends_list) // 5  # понимаем сколько раз запрашивать список членов групп
    f = len(usr_friends_list) % 5
    i = 0
    while i < d:
        if (i + 1) == d:
            y = f
        print('{} запрос к API '.format(i) + ' из {}'.format(d - 1))
        output_dict = usr.get_all_data(i, y)
        i += 1
        z = 0
        while z <= (len(output_dict['response']['fr_group']) - 1):
            fr_group_list.append(
                output_dict['response']['fr_group'][z])  # формируем список списков групп в которых состоят друзья User
            z += 1
    j = 0
    common_groups_list = []
    while j <= len(usr_friends_list):
        try:
            common_groups_list.append(
                list(set(groups_list) & set(fr_group_list[j])))  # получили список общих групп User и его друзей
            j += 1
        except Exception as e:
            j += 1

    flat_common_group_list = list(
        itertools.chain.from_iterable(common_groups_list))  # делаем плоский список групп в которых состоят друзья

    output_group_list = []
    buf_dict = {}
    finish_list = []
    for group in groups_list:
        count = 0
        for fr_com_groups in flat_common_group_list:
            if group == fr_com_groups:  # group - это одна из групп в которой состоит User,
                # fr_com_groups - одна из групп в которой состоит друг User, если они
                # равны, то номер группы фиксируется сначала в буфере buf_dict, а далее в списке finish_list
                count += 1
                buf_dict = {group: count}
            if count == 0:
                buf_dict = {group: '0'}
        finish_list.append(
            buf_dict)  # формируем словарь в котором группе сопоставлено количество друзей которые в ней также состоят

    i = 0
    while i <= (len(finish_list) - 1):
        if int(finish_list[i][groups_list[i]]) <= int(nn):  # выбираем группы, в которых есть друзья, но не более, чем N
            output_group_list.append(list(finish_list[i].keys()))
        i += 1

    output_group_list = list(itertools.chain.from_iterable(output_group_list))
    output_list = get_output_data(output_group_list)
    return output_list


def main():
    N = input('Введите N, оно будет равняться максимальному количеству '
              'друзей которые состоят в группах, которые выдаст Программа  ')
    user_input = input('Введите id или имя пользователя: ')
    user = get_user(user_input)
    output_list = get_output_list(user, N)
    with codecs.open('groups.json', 'w', encoding='utf-8') as json_file:
        json.dump(output_list, json_file, ensure_ascii=False)
    pprint(output_list)


if __name__ == "__main__":
    with open('token.json', 'r') as file:
        data = json.load(file)
        TOKEN = data[0]['token']

main()
