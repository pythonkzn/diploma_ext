import requests
import json

with open('token.json', 'r') as file:
    data = json.load(file)
    TOKEN = data[0]['token']

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