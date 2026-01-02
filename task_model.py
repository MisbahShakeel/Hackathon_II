from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import uuid


class Subtask:
    def __init__(self, data: Optional[Dict] = None):
        data = data or {}
        self.id: str = data.get('id', str(uuid.uuid4()))
        self.title: str = data.get('title', '')
        self.completed: bool = data.get('completed', False)

    @staticmethod
    def validate_title(title: str) -> bool:
        if not isinstance(title, str) or not title.strip():
            raise ValueError('Subtask title must be a non-empty string')
        if len(title) > 100:
            raise ValueError('Subtask title must be 100 characters or less')
        return True

    @staticmethod
    def validate_completed(completed: bool) -> bool:
        if not isinstance(completed, bool):
            raise ValueError('Subtask completed status must be a boolean')
        return True

    def validate(self) -> bool:
        self.validate_title(self.title)
        self.validate_completed(self.completed)
        return True

    def update(self, data: Dict):
        if 'title' in data:
            self.title = data['title']
        if 'completed' in data:
            self.completed = data['completed']
        self.validate()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }


class Task:
    # Class variable to track the next sequential ID
    _next_id = 1

    def __init__(self, data: Optional[Dict] = None):
        data = data or {}
        # Use sequential ID if not provided, otherwise use existing ID
        if 'id' in data and str(data['id']).isdigit():
            self.id: str = str(data['id'])
            # Update the next ID if this one is higher
            current_id = int(data['id'])
            if current_id >= Task._next_id:
                Task._next_id = current_id + 1
        else:
            self.id: str = str(Task._next_id)
            Task._next_id += 1

        self.title: str = data.get('title', '')
        self.description: str = data.get('description', '')
        self.completed: bool = data.get('completed', False)
        self.created_at: datetime = data.get('created_at') or datetime.now()
        self.due_date: Optional[datetime] = self._parse_date(data.get('due_date'))
        self.priority: str = data.get('priority', 'medium')
        self.tags: List[str] = data.get('tags', [])
        self.subtasks: List[Subtask] = [Subtask(subtask_data) for subtask_data in data.get('subtasks', [])]
        self.recurrence: Optional[Dict] = data.get('recurrence', None)
        self.reminders: List[Dict] = data.get('reminders', [])

    def _parse_date(self, date_value):
        if date_value is None:
            return None
        if isinstance(date_value, datetime):
            return date_value
        if isinstance(date_value, str):
            try:
                return datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            except ValueError:
                return datetime.fromtimestamp(float(date_value))
        return date_value

    @staticmethod
    def validate_title(title: str) -> bool:
        if not isinstance(title, str) or not title.strip():
            raise ValueError('Task title must be a non-empty string')
        if len(title) > 200:
            raise ValueError('Task title must be 200 characters or less')
        return True

    @staticmethod
    def validate_priority(priority: str) -> bool:
        valid_priorities = ['high', 'medium', 'low']
        if priority not in valid_priorities:
            raise ValueError(f'Priority must be one of: {", ".join(valid_priorities)}')
        return True

    @staticmethod
    def validate_tags(tags: List[str]) -> bool:
        if not isinstance(tags, list):
            raise ValueError('Tags must be an array')
        if len(tags) > 10:
            raise ValueError('Maximum 10 tags per task')
        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError('Each tag must be a string')
            if len(tag) > 50:
                raise ValueError('Each tag must be 50 characters or less')
        return True

    @staticmethod
    def validate_subtasks(subtasks: List[Subtask]) -> bool:
        if not isinstance(subtasks, list):
            raise ValueError('Subtasks must be an array')
        if len(subtasks) > 50:
            raise ValueError('Maximum 50 subtasks per task')
        return True

    def validate(self) -> bool:
        self.validate_title(self.title)
        self.validate_priority(self.priority)
        self.validate_tags(self.tags)
        self.validate_subtasks(self.subtasks)

        if self.due_date is not None and not isinstance(self.due_date, datetime):
            raise ValueError('Due date must be a valid datetime object or None')

        if not isinstance(self.completed, bool):
            raise ValueError('Completed status must be a boolean')

        if not isinstance(self.created_at, datetime):
            raise ValueError('Created at must be a valid datetime object')

        return True

    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        now = datetime.now().date()
        due_date = self.due_date.date()
        return not self.completed and due_date < now

    def is_due_today(self) -> bool:
        if not self.due_date:
            return False
        now = datetime.now().date()
        due_date = self.due_date.date()
        return now == due_date

    def is_due_future(self) -> bool:
        if not self.due_date:
            return False
        now = datetime.now().date()
        due_date = self.due_date.date()
        return due_date > now and not self.completed

    def get_subtask_completion(self) -> Dict[str, int]:
        if not self.subtasks:
            return {'completed': 0, 'total': 0, 'percentage': 0}

        completed = sum(1 for subtask in self.subtasks if subtask.completed)
        total = len(self.subtasks)
        percentage = round((completed / total) * 100) if total > 0 else 0

        return {'completed': completed, 'total': total, 'percentage': percentage}

    def add_subtask(self, subtask_data: Dict):
        subtask = Subtask(subtask_data)
        self.subtasks.append(subtask)
        return subtask

    def update(self, data: Dict):
        if 'title' in data:
            self.title = data['title']
        if 'description' in data:
            self.description = data['description']
        if 'completed' in data:
            self.completed = data['completed']
        if 'due_date' in data:
            self.due_date = self._parse_date(data['due_date'])
        if 'priority' in data:
            self.priority = data['priority']
        if 'tags' in data:
            self.tags = data['tags']
        if 'subtasks' in data:
            self.subtasks = [Subtask(subtask_data) for subtask_data in data['subtasks']]

        self.validate()
        return self

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'priority': self.priority,
            'tags': self.tags,
            'subtasks': [subtask.to_dict() for subtask in self.subtasks],
            'recurrence': self.recurrence,
            'reminders': self.reminders
        }

    def has_recurring_pattern(self) -> bool:
        """Check if the task has a recurrence pattern."""
        return self.recurrence is not None

    def is_recurring(self) -> bool:
        """Alias for has_recurring_pattern."""
        return self.has_recurring_pattern()

    def should_generate_next_instance(self) -> bool:
        """Check if this recurring task should generate a new instance."""
        if not self.has_recurring_pattern():
            return False

        # If task is completed, generate a new instance based on recurrence
        if self.completed:
            return True

        # If due date has passed and task is not completed, generate a new instance
        if self.due_date and not self.completed:
            now = datetime.now()
            if self.due_date < now:
                return True

        return False

    def calculate_next_due_date(self, current_due_date: Optional[datetime] = None) -> Optional[datetime]:
        """Calculate the next due date based on the recurrence pattern."""
        if not self.has_recurring_pattern():
            return None

        recurrence = self.recurrence
        base_date = current_due_date or self.due_date or datetime.now()

        if not base_date:
            return None

        pattern = recurrence.get('pattern', 'daily')
        interval = recurrence.get('interval', 1)

        if pattern == 'daily':
            return base_date + timedelta(days=interval)
        elif pattern == 'weekly':
            return base_date + timedelta(weeks=interval)
        elif pattern == 'monthly':
            # Handle month boundary correctly
            from calendar import monthrange
            year = base_date.year
            month = base_date.month + interval

            # Adjust year if we go beyond December
            while month > 12:
                year += 1
                month -= 12

            # Get the last day of the target month
            max_day = monthrange(year, month)[1]
            day = min(base_date.day, max_day)

            return base_date.replace(year=year, month=month, day=day,
                                   hour=base_date.hour, minute=base_date.minute,
                                   second=base_date.second, microsecond=base_date.microsecond)
        elif pattern == 'custom':
            # For custom patterns, use interval as days
            return base_date + timedelta(days=interval)
        else:
            return None  # Unknown pattern

    def has_reached_end_condition(self) -> bool:
        """Check if the recurrence has reached its end condition."""
        if not self.has_recurring_pattern():
            return False

        end_condition = self.recurrence.get('end_condition', {})
        end_type = end_condition.get('type', 'never')

        if end_type == 'never':
            return False
        elif end_type == 'after_count':
            # This would require tracking completion count, which we'll implement in the app
            return False
        elif end_type == 'on_date':
            end_date_str = end_condition.get('value')
            if end_date_str:
                try:
                    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))
                    now = datetime.now()
                    return now > end_date
                except ValueError:
                    return False
        return False