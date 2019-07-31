from lib.TaskManager import TaskManager
from json import load

# grab settings
settings = ''
with open('./settings.json') as f:
    settings = load(f)

tm = TaskManager(settings)

