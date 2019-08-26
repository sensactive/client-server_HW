from fabric.api import local


def server():
    local('python server')


def migrate():
    local('python server -m')


def client():
    local(f'python client')


def notebook():
    local('jupyter notebook')


def test():
    local('pytest --cov-report term-missing --cov server')


def kill():
    local('lsof -t -i tcp:8000 | xargs kill')
