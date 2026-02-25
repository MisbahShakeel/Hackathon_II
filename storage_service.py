import json
import os
from typing import List
from task_model import Task
from datetime import datetime


class StorageService:
    def __init__(self, storage_file: str = 'todo_tasks.json'):
        self.storage_file = storage_file

    def save_tasks(self, tasks: List[Task]) -> bool:
        try:
            tasks_data = [task.to_dict() for task in tasks]
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f'Error saving tasks to file: {e}')
            return False

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.storage_file):
            # Reset the ID counter when no file exists
            Task._next_id = 1
            return []

        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)

            tasks = []
            for task_data in tasks_data:
                # Convert date strings back to datetime objects
                if task_data.get('created_at'):
                    if isinstance(task_data['created_at'], str):
                        try:
                            task_data['created_at'] = datetime.fromisoformat(task_data['created_at'].replace('Z', '+00:00'))
                        except ValueError:
                            pass  # Keep original value if parsing fails
                if task_data.get('due_date'):
                    if isinstance(task_data['due_date'], str):
                        try:
                            task_data['due_date'] = datetime.fromisoformat(task_data['due_date'].replace('Z', '+00:00'))
                        except ValueError:
                            pass  # Keep original value if parsing fails

                # Handle reminders with datetime objects
                if task_data.get('reminders'):
                    for reminder in task_data['reminders']:
                        if reminder.get('value') and isinstance(reminder['value'], str):
                            try:
                                reminder['value'] = datetime.fromisoformat(reminder['value'].replace('Z', '+00:00'))
                            except ValueError:
                                pass  # Keep original value if parsing fails

                task = Task(task_data)
                tasks.append(task)

            # After loading all tasks, find the highest ID and set the next ID
            highest_id = 0
            for task in tasks:
                if task.id.isdigit():
                    task_id = int(task.id)
                    if task_id > highest_id:
                        highest_id = task_id
            Task._next_id = highest_id + 1

            return tasks
        except Exception as e:
            print(f'Error loading tasks from file: {e}')
            return []

    def clear_tasks(self) -> bool:
        try:
            if os.path.exists(self.storage_file):
                os.remove(self.storage_file)
            return True
        except Exception as e:
            print(f'Error clearing tasks from file: {e}')
            return False

    def get_storage_info(self):
        if not os.path.exists(self.storage_file):
            return {
                'size': 0,
                'percentage': 0
            }

        size = os.path.getsize(self.storage_file)
        # Assume 10MB limit for file storage
        limit = 10 * 1024 * 1024  # 10MB
        percentage = (size / limit) * 100 if limit > 0 else 0

        return {
            'size': size,
            'percentage': percentage
        }

    def is_near_capacity(self, threshold: float = 0.9) -> bool:
        info = self.get_storage_info()
        return info['percentage'] > threshold * 100