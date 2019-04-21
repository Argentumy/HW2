import requests
from pprint import pprint
from urllib.parse import urlencode
from time import sleep


token = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
friends_id_list = []
friends_group_list = {}
user_groups_list = {}
user_id = input('Введите User ID: ')


def printProgressBar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    print()


class User:

    def __init__(self):
        self.token = token

    def get_friends_params(self):
        return {
            'v': '5.92',
            'access_token': token,
            'fields': 'nickname'
        }

    def get_groups_params(self):
        return {
            'v': '5.92',
            'access_token': token,
            'extended': '1',
            'fields': 'members_count'
        }

    def get_groups_params2(self):
        return {
            'user_id': user_id,
            'v': '5.92',
            'access_token': token,
            'extended': '1',
            'fields': 'members_count'
        }

    def get_friends(self):
        params = self.get_friends_params()

        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )
        return response.json()

    def get_groups(self):
        params = self.get_groups_params2()

        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params
        )

        for values in response.json().values():
            try:
                for bvalues in values['items']:
                    user_groups_list.setdefault('user', list())
                    user_groups_list['user'].append({'name': bvalues['name'], 'id': bvalues['id'],
                                                  'members_count': bvalues['members_count']})
            except KeyError as exception:
                print('No authorization to get this data.')

        sleep(0.25)

        return user_groups_list

    def get_friends_groups(self):
        params = self.get_friends_params()

        response = requests.get(
            'https://api.vk.com/method/friends.get',
            params
        )

        for a in response.json().values():
            for b in a['items']:
                friends_id_list.append(b['id'])

        l = len(friends_id_list)

        for i, a in enumerate(friends_id_list):
            params = {
                'user_id': a,
                'v': '5.92',
                'access_token': token,
                'extended': '1',
                'fields': 'members_count'
            }

            response = requests.get(
                'https://api.vk.com/method/groups.get',
                params
            )

            for values in response.json().values():
                try:
                    for bvalues in values['items']:
                        friends_group_list.setdefault(a, list())
                        friends_group_list[a].append({'name': bvalues['name'], 'id': bvalues['id'],
                                                      'members_count': bvalues['members_count']})
                except KeyError as exception:
                    print('No authorization to get this data.')

            sleep(0.25)

            printProgressBar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)

        return friends_group_list

    def compare_groups(self):
        group1 = self.get_groups()
        group2 = self.get_friends_groups()

        seta1 = set()
        seta2 = set()

        for value in group1.values():
            for value1 in value:
                seta1.add(value1['id'])

        for value2 in group2.values():
            for value3 in value2:
                seta2.add(value3['id'])

        diff = seta1.difference(seta2)

        for value4 in group1.values():
            for value5 in value4:
                for difference in diff:
                    if difference == value5['id']:
                        print(value5)


user = User()
user.compare_groups()
