import requests
import re
import _thread
import time

commands = []


def formatCommand(cmd):
    cmd = cmd.strip()
    cmd = re.sub(' +', ' ', cmd)
    return cmd


def poll():
    while True:
        delete_ids = []
        length = len(commands)
        for i in range(length):
            id = commands[i]['id']
            res = requests.get(
                'http://localhost:5000/complete', params={'id': id})
            if res.json()['status']:
                if res.json()['result']:
                    print('Task completed - ', res.json()
                          ['result']['text'])
                    delete_ids.append(i)
        for index in delete_ids:
            print('Time taken - ', (time.time() -
                                    commands[index]['started']), 's')
            del commands[index]
        time.sleep(0.1)


_thread.start_new_thread(poll, ())

while True:
    command = input('> ')
    command = formatCommand(command)
    headers = {'content-type': 'application/json'}
    res = requests.post('http://localhost:5000/command',
                        json={'command': command})
    if res.json()['status']:
        print('Sent')
        commands.append(
            {'id': res.json()['inserted'], 'command': command, 'started': time.time()})
