from todoist import TodoistAPI
from statistics import mean

from lib.predicates import (
    get_project_or_none,
    convert_labels,
    project_owned_by_user,
    is_spoonsy_task,
    calculate_values,
)

class TaskManager:
    def __init__(self, settings):
        self.todoist = TodoistAPI(settings['API_KEY'])
        self.todoist.sync()
        self.user = self.todoist.state['user']['id']
        self.labels = convert_labels(self.todoist.state['labels'])

    def _sync(func):
        def synced(self, *args, **kwargs):
            self.todoist.sync()
            return func(self, *args, **kwargs)
        return synced

    @_sync
    def avg_spoons(self):
        completed_spoonsy_tasks = [ task for task in self.get_tasks() if is_spoonsy_task(task, self.labels) and task['date_completed'] ]
        return mean([ calculate_values(task['labels']) for task in completed_spoonsy_tasks ])

    @_sync
    def get_projects(self):
        return [ project for project in self.todoist.state['projects'] if project_owned_by_user(project, self.user) ]

    @_sync
    def get_tasks(self, project_name='all'):
        all_tasks = self.todoist.state['items']
        if project_name == 'all':
            return all_tasks
        else:
            project = get_project_or_none(all_tasks, project_name)
            return [ item for item in all_tasks if item['project_id'] == project['id'] ]


