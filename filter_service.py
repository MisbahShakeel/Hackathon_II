from typing import List, Dict, Optional
from task_model import Task
from datetime import datetime, date


class FilterService:
    def __init__(self):
        pass

    def search_tasks(self, tasks: List[Task], query: str) -> List[Task]:
        if not query or not isinstance(query, str):
            return tasks

        normalized_query = query.lower().strip()

        return [
            task for task in tasks
            if normalized_query in task.title.lower() or
            (task.description and normalized_query in task.description.lower())
        ]

    def filter_tasks(self, tasks: List[Task], filters: Optional[Dict] = None) -> List[Task]:
        filters = filters or {}
        filtered_tasks = tasks[:]

        # Filter by status
        if 'status' in filters:
            status = filters['status']
            if status == 'active':
                filtered_tasks = [task for task in filtered_tasks if not task.completed]
            elif status == 'completed':
                filtered_tasks = [task for task in filtered_tasks if task.completed]

        # Filter by priority
        if 'priority' in filters and filters['priority'] != 'all':
            priority = filters['priority']
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        # Filter by tags
        if 'tags' in filters and isinstance(filters['tags'], list) and filters['tags']:
            tags = filters['tags']
            filtered_tasks = [
                task for task in filtered_tasks
                if any(tag in task.tags for tag in tags)
            ]

        # Filter by due date range
        if 'due_date_range' in filters:
            due_date_range = filters['due_date_range']
            today = date.today()

            filtered_tasks = [
                task for task in filtered_tasks
                if self._matches_due_date_filter(task, due_date_range, today)
            ]

        return filtered_tasks

    def _matches_due_date_filter(self, task: Task, due_date_range: str, today: date) -> bool:
        if not task.due_date:
            return due_date_range == 'no-date'

        task_due_date = task.due_date.date()

        if due_date_range == 'today':
            return task_due_date == today
        elif due_date_range == 'upcoming':
            return task_due_date > today and not task.completed
        elif due_date_range == 'overdue':
            return task_due_date < today and not task.completed
        elif due_date_range == 'no-date':
            return not task.due_date
        else:  # 'all' or default
            return True

    def search_and_filter(self, tasks: List[Task], query: str, filters: Dict) -> List[Task]:
        result = self.search_tasks(tasks, query)
        result = self.filter_tasks(result, filters)
        return result

    def get_unique_tags(self, tasks: List[Task]) -> List[str]:
        all_tags = []
        for task in tasks:
            all_tags.extend(task.tags)
        return sorted(list(set(all_tags)))

    def get_tasks_by_priority(self, tasks: List[Task], priority: str) -> List[Task]:
        return [task for task in tasks if task.priority == priority]

    def get_completed_tasks(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if task.completed]

    def get_active_tasks(self, tasks: List[Task]) -> List[Task]:
        return [task for task in tasks if not task.completed]

    def get_overdue_tasks(self, tasks: List[Task]) -> List[Task]:
        today = date.today()
        return [
            task for task in tasks
            if task.due_date and not task.completed and task.due_date.date() < today
        ]

    def get_tasks_due_today(self, tasks: List[Task]) -> List[Task]:
        today = date.today()
        return [
            task for task in tasks
            if task.due_date and task.due_date.date() == today and not task.completed
        ]