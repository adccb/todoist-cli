from lib.err import ProjectNotFoundError

# Projects
def project_owned_by_user(project, user_id):
    return project['user_id'] != user_id or project['parent_id'] == None and project['name'][0] != '_'

def get_project_or_none(state, project_name):
    projects = [ project for project in state['projects'] if project['name'] == project_name ]
    if len(projects) < 1:
        return None
    return projects[0]

# Tasks
def is_spoonsy_task(task, lookup):
    labels = task['labels']
    if len(labels) == 0:
        return False

    spoonsy_tasks = [ label for label in task['labels'] if label[1].startswith('s_') ]
    return spoonsy_tasks if len(spoonsy_tasks) else False

# Labels
def convert_labels(labels):
    return { label['id']: label['name'] for label in labels }

def calculate_values(labels):
    lookup = { 's_0': 0, 's_1': 1, 's_2': 2, 's_3': 3, 's_5_plus': 5 }
    return sum([ lookup[label[1]] for label in labels if label[1].startswith('s_') ])

