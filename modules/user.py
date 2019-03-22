import time
import requests
import json

with open('token.json', 'r') as file:
    data = json.load(file)
    TOKEN = data[0]['token']

class User:
    def __init__(self, id):
        self.id = id

    def get_all_data(self, d, f):
        params = {'access_token': TOKEN, 'v': 5.92,
                  'code': ''
                          'var groups =API.groups.get({user_id:' + str(self.id) + '}).items;'  # группы User
                          'var counts = API.groups.get({user_id:' + str(self.id) + '}).count;'  # количество групп User
                          'var usr_friends = API.friends.get({user_id:' + str(self.id) + '}).items;'
                          'var usr_friends_check_count = API.friends.get({user_id:' + str(self.id) + '}).count;'
                          'if (usr_friends_check_count > 5000){'
                          'usr_friends = usr_friends'
                          ' + API.friends.get({user_id:' + str(self.id) + ', offset: 5000}).items;}'
                          'var i=5*' + str(d) + ';'  # за один раз - 5 запросов 
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