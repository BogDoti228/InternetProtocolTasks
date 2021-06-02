import urllib.request
import json

global new_access_token


def build_get_data_id_request(user_id):
    return "https://api.vk.com/method/users.get?user_ids=" + user_id + "&access_token=" + new_access_token + "&v=5.131"


def build_get_friends_request(user_id):
    return "https://api.vk.com/method/friends.get?user_id=" + user_id + "&fields=nickname&access_token=" + new_access_token + "&v=5.131"


def convert_id_or_nickname_to_id(user_id):
    with urllib.request.urlopen(build_get_data_id_request(user_id)) as answer_1:
        data_user = answer_1.read()
        parsed_data_user = json.loads(data_user)
        return str(parsed_data_user['response'][0]['id'])


def get_friends_of_user(user_id):
    with urllib.request.urlopen(build_get_friends_request(user_id)) as answer_1:
        data_friends = answer_1.read()
        parsed_data_friends = json.loads(data_friends)
        for friend_info in parsed_data_friends['response']['items']:
            print(friend_info['first_name'] + " " + friend_info['last_name'])


if __name__ == '__main__':
    new_access_token = input("Введите свой access token чтобы приложение работало ")
    while True:
        new_user_id = input("Введите id пользователя у которого хотите увидеть друзей ")
        if new_user_id == 'exit':
            print("Спасибо за использование")
            break
        try:
            converted_user_id = convert_id_or_nickname_to_id(new_user_id)
        except:
            print("Нет такого пользователя")
            continue
        try:
            get_friends_of_user(converted_user_id)
        except:
            print("Приватный аккаунт либо удален либо забанен")
            continue
