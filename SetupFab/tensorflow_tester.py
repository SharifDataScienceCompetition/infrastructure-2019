#!/usr/bin/python
import json
import random
import string
import sys

from fabric import Connection
import fabric

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def _initialize(c):
    c.run('rm -f test.py')
    c.run('pip install tensorflow --user')
    c.run('echo "import tensorflow" >> test.py') 
    c.run( 'echo "ses=tensorflow.Session()" >> test.py')
    c.run( 'echo "ses.close()" >> test.py')
    test_result = c.run('python3 test.py')

    # print(test_result.exited)
    # print(test_result.ok)

    c.run('rm test.py')
    if 'Created TensorFlow device' in str(test_result):
        print('\033[32m -------> ok\033[0m'')
    else:
        print('\033[31m -------> shit happend\033[0m')

def _ssh_config(c):
    c.run('echo -e "PasswordAuthentication yes\n$(cat /etc/ssh/sshd_config)" > "/etc/ssh/sshd_config"')
    c.run('service ssh reload')

def _startConnection(host, user, port, password=None):
    c = Connection(host=host, user=user, port=port)
    return c



users = []
server_info = {}
servers = []


def main(server_info_path, servers_path: str = None):
    f = open(server_info_path, 'w+')

    if servers_path:
        server_file = fopen(server_info_path)
    # servers = json.load(server_file)
    count = 0
    for host, port in servers:
        print(servers)
        user = 'root'
        
        count += 1
        server_name = 'server' + str(count)
        server_info[server_name] = {}
        print('\033[33mHost:\033[0m ' , str(host) , '\033[33m - Port:\033[0m ', str(port) , end='' )
        c = _startConnection(host=host, user=user, port=port)
        _initialize(c)
        
        c.close()

    json_data = json.dumps(server_info)
    f.write(json_data)
    f.close()


if __name__ == '__main__':
    args = sys.argv
    if '-all' in args:
        f = open(args[2], 'r')
        server_info_path = args[3]
        line = f.readline()
        while line:
            pars = line.split()
            servers.append((pars[3].split('@')[1], pars[2],))
            line = f.readline()
    elif len(args) == 3:
        key = 1
        while key < len(args) - 1:
            servers.append((args[key], args[key + 1]))
            key += 2
        server_info_path = args[len(args) - 1]
    else:                                                                    
        print('''
        -help
        -all [remote_host_file] [added_users_file]
        [remote_host remote_port ...] [added_users_file]
        ''')
        exit(0)
    main(server_info_path)
