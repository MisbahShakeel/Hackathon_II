from typing import List
from task_model import Task
from datetime import datetime, date


class SortService:
    def __init__(self):
        pass

    def sort_tasks(self, tasks: List[Task], sort_by: str = 'dueDate', order: str = 'asc') -> List[Task]:
        sorted_tasks = tasks[:]

        if sort_by == 'dueDate':
            sorted_tasks.sort(key=lambda task: self._get_due_date_sort_key(task), reverse=(order == 'desc'))
        elif sort_by == 'priority':
            sorted_tasks.sort(key=lambda task: self._get_priority_sort_key(task), reverse=(order == 'desc'))
        elif sort_by == 'createdAt':
            sorted_tasks.sort(key=lambda task: self._get_created_at_sort_key(task), reverse=(order == 'desc'))
        elif sort_by == 'title':
            sorted_tasks.sort(key=lambda task: self._get_title_sort_key(task), reverse=(order == 'asc' if order == 'desc' else False))
        else:
            # Default to due date sorting
            sorted_tasks.sort(key=lambda task: self._get_due_date_sort_key(task), reverse=(order == 'desc'))

        return sorted_tasks

    def _get_due_date_sort_key(self, task: Task):
        # Check if task is overdue
        is_overdue = self._is_overdue(task)

        # If overdue, prioritize it by making it "earlier" in sort
        if is_overdue:
            # Use a very early date to ensure overdue items come first
            return (0, task.due_date.isoformat() if task.due_date else "9999-12-31")
        else:
            # For non-overdue tasks, sort by due date (None values go to end)
            return (1, task.due_date.isoformat() if task.due_date else "9999-12-31")

    def _get_priority_sort_key(self, task: Task) -> int:
        priority_order = {'high': 3, 'medium': 2, 'low': 1}
        return priority_order.get(task.priority, 0)

    def _get_created_at_sort_key(self, task: Task) -> datetime:
        return task.created_at

    def _get_title_sort_key(self, task: Task) -> str:
        return task.title.lower()

    def _is_overdue(self, task: Task) -> bool:
        if not task.due_date or task.completed:
            return False
        today = date.today()
        due_date = task.due_date.date()
        return due_date < today

    def default_sort(self, tasks: List[Task]) -> List[Task]:
        return self.sort_tasks(tasks, 'dueDate', 'asc')