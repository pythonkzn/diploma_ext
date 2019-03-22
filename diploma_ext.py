import requests
import itertools
import json
import codecs
from pprint import pprint
from modules.user import User
from modules.group import Group


def get_user(usr_in):
    try:
        int(usr_in)
        user = User(usr_in)
        return user
    except ValueError:
        params = {
            'user_ids': usr_in,
            'access_token': TOKEN,
            'v': 5.92
        }
        try:
            response_get_id = requests.get(
                'https://api.vk.com/method/users.get',
                params
            )
            user = User(int(response_get_id.json()['response'][0]['id']))  # получили по имени пользователя его id
            return user
        except Exception as e:
            print(response_get_id.json()['error']['error_msg'])



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
    def get_fr_group(var_div, var_float, var_null):
        i = 0
        while i < var_div:
            if (i + 1) == var_div:
                var_null = var_float
            print('{} запрос к API '.format(i) + ' из {}'.format(var_div - 1))
            sub_output_dict = usr.get_all_data(i, var_null)
            i += 1
            z = 0
            while z <= (len(output_dict['response']['fr_group']) - 1):
                fr_group_list.append(
                    sub_output_dict['response']['fr_group'][z])
                z += 1
        return fr_group_list

    def get_com_group(input_usr_friends_list, input_groups_list, input_fr_group_list):
        j = 0
        common_groups_list = []
        while j <= len(input_usr_friends_list):
            try:
                common_groups_list.append(
                    list(set(input_groups_list) & set(input_fr_group_list[j])))  # получили список общих групп c друзьями
                j += 1
            except Exception as e:
                j += 1

        sub_flat_common_group_list = list(
            itertools.chain.from_iterable(common_groups_list))  # делаем плоский список групп в которых состоят друзья
        return sub_flat_common_group_list

    def get_res_list(input_list_com, input_list_group):
        sub_output_group_list = []
        buf_dict = {}
        finish_list = []
        for group in input_list_group:
            count = 0
            for fr_com_groups in input_list_com:
                if group == fr_com_groups:  # group - это одна из групп в которой состоит User,
                    # fr_com_groups - одна из групп в которой состоит друг User, если они
                    # равны, то номер группы фиксируется сначала в буфере buf_dict, а далее в списке finish_list
                    count += 1
                    buf_dict = {group: count}
                if count == 0:
                    buf_dict = {group: '0'}
            finish_list.append(
                buf_dict)  # формируем словарь в котором группе сопоставлено количество друзей которые в ней тож состоят
        i = 0
        while i <= (len(finish_list) - 1):
            if int(finish_list[i][groups_list[i]]) <= int(nn):  # выбираем группы, в которых есть друзья не более, чем N
                sub_output_group_list.append(list(finish_list[i].keys()))
            i += 1
        return sub_output_group_list

    try:
        null_cof_1 = 0
        null_cof_2 = 0  # нулевые коэффициенты для того чтобы получить первые пять списков от execute
        output_dict = usr.get_all_data(null_cof_1, null_cof_2)  # получаем список групп и друзей User
        groups_list = output_dict['response']['groups']
        fr_group_list = []
        usr_friends_list = output_dict['response']['usr_friends']  # формируем список id друзей User
        int_div = len(usr_friends_list) // 5  # понимаем сколько раз запрашивать execute запрос
        float_div = len(usr_friends_list) % 5
        fr_group_list = get_fr_group(int_div, float_div, null_cof_2)  # формируем список списков групп друзей
        flat_common_group_list = get_com_group(usr_friends_list, groups_list, fr_group_list)  # делаем список плоским
        output_group_list = get_res_list(flat_common_group_list, groups_list)  # получили список общих групп < N
        output_group_list = list(itertools.chain.from_iterable(output_group_list))  # делаем его плоским
        output_list = get_output_data(output_group_list)  # получаем json в требуемом формате
        return output_list
    except Exception as e:
            pass


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
