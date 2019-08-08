from fabric.api import local


def server():
    local('python server')


def client(mode):
    local(f'python client --mode {mode}')


def notebook():
    local('jupyter notebook')


def test():
    local('pytest --cov-report term-missing --cov server')


def kill():
    local('lsof -t -i tcp:7777 | xargs kill')
