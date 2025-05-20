from app.models import Task, User
from app import db

def can_mark_task_completed(task):
    """
    Check if all dependencies of the given task are completed.
    Returns True if the task can be marked as 'completed', else False.
    """
    for dependency in task.dependencies:
        if dependency.status != 'completed':
            return False
    return True


def has_circular_dependency(task, new_dependencies):
    """
    Detect if adding new dependencies to a task would introduce a cycle.

    task: Task object being updated
    new_dependencies: List of Task objects to be added as dependencies

    Returns True if a cycle would be created, else False.
    """
    visited = set()
    stack = []

    def visit(current_task):
        if current_task.id in stack:
            return True  
        if current_task.id in visited:
            return False

        visited.add(current_task.id)
        stack.append(current_task.id)

        for dep in current_task.dependencies:
            if visit(dep):
                return True

        stack.pop()
        return False

    original_dependencies = list(task.dependencies)
    task.dependencies = new_dependencies

    result = visit(task)


    task.dependencies = original_dependencies
    return result


def can_delete_user(user):
    """
    Return True if the user can be deleted (i.e., no pending or in-progress tasks assigned to them).
    """
    for task in user.tasks:
        if task.status in ('pending', 'in-progress'):
            return False
    return True
