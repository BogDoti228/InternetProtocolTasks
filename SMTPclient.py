import base64
import json
import os
import socket
import ssl

HOST = "smtp.yandex.ru"
PORT = 465
USERNAME = "karakoskarakas2281337@yandex.ru"
PASSWORD = "atfanttsweqgkcgf"
SEPARATOR = "zxczxczxcSf1x1DeadInsideGhoul1000-7"


def build_data(config):
    attachments = config['attachments']
    letter = config['letter']
    data = generate_start_message(config)
    if attachments:
        data += f'Content-Type: multipart/mixed; boundary="{SEPARATOR}"\n\n\n'
        for attachment in config['attachments']:
            data = add_attachment(data, attachment)
        if letter:
            data = add_letter(data, letter)
        data += f'--{SEPARATOR}--\n.'
        return data
    elif letter:
        return data + 'Content-Type: text/plain\n\n' + f'{set_letter_points(letter)}\n.'
    else:
        return data + '\n.'


def add_letter(data, letter):
    return (data +
            f'--{SEPARATOR}\n' +
            generate_multipart_letter_message(letter))


def set_letter_points(string: str):
    lines = string.splitlines()
    if len(lines) == 1:
        return lines[0]
    res = ''
    for line in lines:
        if line == '':
            res += '\n'
        elif line[0] == '.':
            res += '.' + line + '\n'
        else:
            res += line + '\n'
    return res


def add_attachment(data, file_name):
    before = data
    try:
        data += (f'--{SEPARATOR}\n' + generate_multipart_file_message(
            file_name))
        with open(os.path.join('Additional', file_name), 'rb') as file:
            data += base64.b64encode(file.read()).decode()
        data += '\n'
        return data
    except Exception:
        return before


def generate_multipart_file_message(file):
    return (f'Content-Disposition: attachment; \n\tfilename="{file}"\n' +
            f'Content-Transfer-Encoding: base64\n' +
            f'Content-Type: image/jpg; \n\tname="{file}"\n\n')


def generate_multipart_letter_message(letter):
    return (f'Content-Transfer-Encoding: 8bit\n' +
            f'Content-Type: text/plain\n' +
            f'\n{set_letter_points(letter)}\n')


def generate_start_message(config):
    return (f'From: {USERNAME}\n' +
            f'To: {", ".join(config["receivers"])}\n' +
            f'Subject: {config["theme"]}\n' +
            'MIME-Version: 1.0\n')


def request(socket, request):
    socket.send((request + '\n').encode('utf8'))
    recv_data = socket.recv(65535).decode()
    return recv_data


if __name__ == '__main__':
    with open('Additional/config.json', 'rt', encoding='utf8') as file:
        config = json.loads(file.read())
    with open('Additional/letter.txt', 'rt', encoding='utf8') as file:
        config['letter'] = file.read()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        client = ssl.wrap_socket(client)
        print(client.recv(1024))
        print(request(client, 'EHLO ' + USERNAME))
        base64login = base64.b64encode(USERNAME.encode()).decode()
        base64password = base64.b64encode(PASSWORD.encode()).decode()
        print(request(client, 'AUTH LOGIN'))
        print(request(client, base64login))
        print(request(client, base64password))
        print(request(client, 'MAIL FROM:' + USERNAME))
        for receiver in config['receivers']:
            print(request(client, f'RCPT TO: {receiver}'))
        print(request(client, 'DATA'))
        print(request(client, build_data(config)))
        print(request(client, 'QUIT'))
