from fabric.api import *

def serve():
	local('python manage.py runserver')

def shell():
	local('python manage.py shell')
