#!/usr/bin/env python3
"""
CLI Todo Application

A command-line interface for managing tasks. This is the main application file
converted from the original web-based version to a CLI-based application.
"""
import argparse
import sys
import json
from datetime import datetime, date
from typing import List, Optional

# Import existing modules
from task_model import Task, Subtask
from storage_service import StorageService
from filter_service import FilterService
from sort_service import SortService


class TodoApp:
    def __init__(self):
        self.storage_service = StorageService()
        self.filter_service = FilterService()
        self.sort_service = SortService()
        self.tasks = self.storage_service.load_tasks()
        # Ensure the ID counter is properly set after loading tasks
        highest_id = 0
        for task in self.tasks:
            if task.id.isdigit():
                task_id = int(task.id)
                if task_id > highest_id:
                    highest_id = task_id
        from task_model import Task
        Task._next_id = highest_id + 1

    def save_tasks(self):
        """Save tasks to storage"""
        self.storage_service.save_tasks(self.tasks)

    def find_task_by_id(self, task_id: str) -> Optional[Task]:
        """Find a task by its ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def add_task(self, title: str, description: str = "", due_date: str = None,
                 priority: str = "medium", tags: List[str] = None):
        """Add a new task"""
        if not tags:
            tags = []

        task_data = {
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'tags': tags
        }

        task = Task(task_data)
        self.tasks.append(task)
        self.save_tasks()

        print(f"Task added successfully with ID: {task.id}")
        return task

    def list_tasks(self, status: str = None, priority: str = None, tags: List[str] = None,
                   due_date_range: str = None, search_query: str = "", sort_by: str = "dueDate",
                   sort_order: str = "asc", show_completed: bool = True):
        """List tasks with optional filtering and sorting"""
        # Prepare filters
        filters = {}
        if status and status != 'all':
            filters['status'] = status
        if priority and priority != 'all':
            filters['priority'] = priority
        if tags:
            filters['tags'] = tags
        if due_date_range and due_date_range != 'all':
            filters['due_date_range'] = due_date_range

        # Apply search and filters
        filtered_tasks = self.filter_service.search_and_filter(self.tasks, search_query, filters)

        # Apply completion filter
        if not show_completed:
            filtered_tasks = [task for task in filtered_tasks if not task.completed]

        # Apply sorting
        sorted_tasks = self.sort_service.sort_tasks(filtered_tasks, sort_by, sort_order)

        # Process recurring tasks - generate new instances if needed
        self.process_recurring_tasks()

        # Display tasks
        if not sorted_tasks:
            print("No tasks found.")
            return

        print(f"\nFound {len(sorted_tasks)} task(s):\n")
        print("-" * 80)

        for i, task in enumerate(sorted_tasks):
            self.display_task(task)
            if i < len(sorted_tasks) - 1:
                print("-" * 80)

    def display_task(self, task: Task):
        """Display a single task with enhanced formatting"""
        status = "[x]" if task.completed else "[ ]"
        priority_char = {"high": "H", "medium": "M", "low": "L"}[task.priority]

        # Format due date
        due_date_str = ""
        if task.due_date:
            due_date_str = f" | Due: {task.due_date.strftime('%Y-%m-%d')}"
            if task.is_overdue():
                due_date_str += " (OVERDUE!)"
            elif task.is_due_today():
                due_date_str += " (TODAY)"

        # Format tags
        tags_str = f" | Tags: {', '.join(task.tags)}" if task.tags else ""

        # Format subtasks
        subtask_info = ""
        if task.subtasks:
            completion = task.get_subtask_completion()
            subtask_info = f" | Subtasks: {completion['completed']}/{completion['total']} ({completion['percentage']}%)"

        # Print main task info
        print(f"{status} [{task.id[:8]}...] ({priority_char}) {task.title}")

        # Print description if exists
        if task.description:
            print(f"   Desc: {task.description}")

        # Print task metadata
        print(f"   Stats: Status={'Completed' if task.completed else 'Active'} | Priority={task.priority}{due_date_str}{tags_str}{subtask_info}")

        # Show subtasks if any
        if task.subtasks:
            print("   Subtasks:")
            for subtask in task.subtasks:
                sub_status = "[x]" if subtask.completed else "[ ]"
                print(f"     {sub_status} {subtask.title}")

        # Show recurrence info if applicable
        if task.has_recurring_pattern():
            recurrence = task.recurrence
            pattern = recurrence.get('pattern', 'unknown')
            interval = recurrence.get('interval', 1)
            end_condition = recurrence.get('end_condition', {})
            end_type = end_condition.get('type', 'never')

            recurrence_info = f" | Recurring: {pattern}"
            if interval > 1:
                recurrence_info += f" every {interval}"

            if end_type != 'never':
                recurrence_info += f" (ends: {end_type})"

            print(f"   {recurrence_info}")

        print()  # Extra newline for readability

    def process_recurring_tasks(self):
        """Process recurring tasks and generate new instances as needed."""
        # Get all recurring tasks that should generate new instances
        recurring_tasks_to_process = [task for task in self.tasks
                                      if task.is_recurring() and
                                      task.should_generate_next_instance() and
                                      not task.has_reached_end_condition()]

        for task in recurring_tasks_to_process:
            # Create a new instance based on the original task
            new_task = self.create_recurring_instance(task)
            if new_task:
                print(f"Generated new instance of recurring task: {new_task.title}")

        if recurring_tasks_to_process:
            self.save_tasks()

    def create_recurring_instance(self, original_task: Task) -> Optional[Task]:
        """Create a new instance of a recurring task based on its recurrence rule."""
        if not original_task.is_recurring():
            return None

        # Calculate the next due date
        next_due_date = original_task.calculate_next_due_date()

        # Create a new task with the same properties as the original
        new_task_data = {
            'title': original_task.title,
            'description': original_task.description,
            'due_date': next_due_date.isoformat() if next_due_date else None,
            'priority': original_task.priority,
            'tags': original_task.tags.copy(),
            'recurrence': original_task.recurrence,  # Preserve the recurrence rule
            'reminders': original_task.reminders  # Preserve the reminders
        }

        # Create new task instance
        new_task = Task(new_task_data)

        # Add to tasks list
        self.tasks.append(new_task)

        return new_task

    def set_task_recurrence(self, task_id: str, pattern: str, interval: int = 1, end_condition: Dict = None):
        """Set recurrence pattern for a task."""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        # Validate pattern
        valid_patterns = ['daily', 'weekly', 'monthly', 'custom']
        if pattern not in valid_patterns:
            print(f"Error: Invalid pattern '{pattern}'. Valid patterns are: {', '.join(valid_patterns)}")
            return False

        # Set default end condition if not provided
        if end_condition is None:
            end_condition = {'type': 'never'}

        # Create recurrence rule
        task.recurrence = {
            'pattern': pattern,
            'interval': interval,
            'end_condition': end_condition
        }

        self.save_tasks()
        print(f"Recurrence pattern '{pattern}' (every {interval}) set for task '{task.title}'.")
        return True

    def remove_task_recurrence(self, task_id: str):
        """Remove recurrence pattern from a task."""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        task.recurrence = None
        self.save_tasks()
        print(f"Recurrence pattern removed from task '{task.title}'.")
        return True

    def complete_task(self, task_id: str, completed: bool = True):
        """Mark a task as complete or incomplete"""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        task.completed = completed
        self.save_tasks()

        status = "completed" if completed else "marked as incomplete"
        print(f"Task '{task.title}' has been {status}.")
        return True

    def delete_task(self, task_id: str):
        """Delete a task by ID"""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        self.tasks.remove(task)
        self.save_tasks()

        print(f"Task '{task.title}' has been deleted.")
        return True

    def update_task(self, task_id: str, title: str = None, description: str = None,
                    due_date: str = None, priority: str = None, tags: List[str] = None):
        """Update a task's properties"""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if due_date is not None:
            update_data['due_date'] = due_date
        if priority is not None:
            update_data['priority'] = priority
        if tags is not None:
            update_data['tags'] = tags

        task.update(update_data)
        self.save_tasks()

        print(f"Task '{task.title}' has been updated.")
        return True

    def search_tasks(self, query: str):
        """Search tasks by title or description"""
        self.list_tasks(search_query=query)

    def add_subtask(self, task_id: str, title: str, completed: bool = False):
        """Add a subtask to a task"""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        subtask_data = {
            'title': title,
            'completed': completed
        }

        subtask = task.add_subtask(subtask_data)
        self.save_tasks()

        print(f"Subtask '{subtask.title}' added to task '{task.title}'.")
        return True

    def complete_subtask(self, task_id: str, subtask_id: str, completed: bool = True):
        """Mark a subtask as complete or incomplete"""
        task = self.find_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        subtask = None
        for st in task.subtasks:
            if st.id == subtask_id:
                subtask = st
                break

        if not subtask:
            print(f"Error: Subtask with ID {subtask_id} not found in task {task_id}.")
            return False

        subtask.completed = completed
        self.save_tasks()

        status = "completed" if completed else "marked as incomplete"
        print(f"Subtask '{subtask.title}' in task '{task.title}' has been {status}.")
        return True

    def stats(self):
        """Show task statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.completed])
        active_tasks = total_tasks - completed_tasks
        overdue_tasks = len([t for t in self.tasks if t.is_overdue()])

        # Priority breakdown
        priority_breakdown = {'high': 0, 'medium': 0, 'low': 0}
        for task in self.tasks:
            if task.priority in priority_breakdown:
                priority_breakdown[task.priority] += 1

        # Due date breakdown
        today_tasks = len([t for t in self.tasks if t.is_due_today()])
        upcoming_tasks = len([t for t in self.tasks if t.is_due_future()])

        print("\nTask Statistics:")
        print(f"Total tasks: {total_tasks}")
        print(f"Active tasks: {active_tasks}")
        print(f"Completed tasks: {completed_tasks}")
        print(f"Overdue tasks: {overdue_tasks}")
        print(f"Tasks due today: {today_tasks}")
        print(f"Upcoming tasks: {upcoming_tasks}")
        print("\nPriority Breakdown:")
        for priority, count in priority_breakdown.items():
            print(f"  {priority.capitalize()}: {count}")

        # Calculate completion percentage
        if total_tasks > 0:
            completion_percentage = (completed_tasks / total_tasks) * 100
            print(f"\nOverall completion: {completion_percentage:.1f}%")


def create_parser():
    """Create and configure the argument parser"""
    parser = argparse.ArgumentParser(
        description="CLI Todo Application - Manage your tasks from the command line",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  app.py add "Complete project" --priority high --due "2025-12-31" --tags work,important
  app.py list --status active --priority high
  app.py complete <task-id>
  app.py list --due-date overdue
  app.py search "project"
  app.py subtask add <task-id> "Write draft"
  app.py stats
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add task command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--description', '-d', help='Task description')
    add_parser.add_argument('--due', '-D', help='Due date (YYYY-MM-DD)')
    add_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], default='medium', help='Priority level')
    add_parser.add_argument('--tags', '-t', help='Comma-separated tags (e.g., work,important)')

    # List tasks command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=['active', 'completed', 'all'], default='all', help='Filter by status')
    list_parser.add_argument('--priority', choices=['low', 'medium', 'high', 'all'], default='all', help='Filter by priority')
    list_parser.add_argument('--tags', help='Filter by tags (comma-separated)')
    list_parser.add_argument('--due-date', '--due', dest='due_date_range',
                            choices=['all', 'today', 'upcoming', 'overdue', 'no-date'],
                            default='all', help='Filter by due date range')
    list_parser.add_argument('--search', '-s', help='Search in title or description')
    list_parser.add_argument('--sort', dest='sort_by', choices=['dueDate', 'priority', 'createdAt', 'title'],
                            default='dueDate', help='Sort by field')
    list_parser.add_argument('--order', choices=['asc', 'desc'], default='asc', help='Sort order')

    # Complete task command
    complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
    complete_parser.add_argument('task_id', help='Task ID to complete')
    complete_parser.add_argument('--incomplete', action='store_true', help='Mark as incomplete instead of complete')

    # Delete task command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', help='Task ID to delete')

    # Update task command
    update_parser = subparsers.add_parser('update', help='Update task properties')
    update_parser.add_argument('task_id', help='Task ID to update')
    update_parser.add_argument('--title', help='New title')
    update_parser.add_argument('--description', '-d', help='New description')
    update_parser.add_argument('--due', '-D', help='New due date (YYYY-MM-DD)')
    update_parser.add_argument('--priority', '-p', choices=['low', 'medium', 'high'], help='New priority')
    update_parser.add_argument('--tags', '-t', help='New tags (comma-separated)')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks')
    search_parser.add_argument('query', help='Search query')

    # Subtask command
    subtask_parser = subparsers.add_parser('subtask', help='Manage subtasks')
    subtask_subparsers = subtask_parser.add_subparsers(dest='subtask_command', help='Subtask commands')

    # Add subtask
    add_subtask_parser = subtask_subparsers.add_parser('add', help='Add a subtask')
    add_subtask_parser.add_argument('task_id', help='Task ID to add subtask to')
    add_subtask_parser.add_argument('title', help='Subtask title')
    add_subtask_parser.add_argument('--completed', action='store_true', help='Mark as completed initially')

    # Complete subtask
    complete_subtask_parser = subtask_subparsers.add_parser('complete', help='Mark subtask as complete')
    complete_subtask_parser.add_argument('task_id', help='Task ID containing the subtask')
    complete_subtask_parser.add_argument('subtask_id', help='Subtask ID to complete')
    complete_subtask_parser.add_argument('--incomplete', action='store_true', help='Mark as incomplete instead of complete')

    # Stats command
    subparsers.add_parser('stats', help='Show task statistics')

    # Recurring task command
    recurring_parser = subparsers.add_parser('recurring', help='Manage recurring tasks')
    recurring_subparsers = recurring_parser.add_subparsers(dest='recurring_command', help='Recurring task commands')

    # Add recurring task
    add_recurring_parser = recurring_subparsers.add_parser('add', help='Add recurrence pattern to task')
    add_recurring_parser.add_argument('task_id', help='Task ID to add recurrence to')
    add_recurring_parser.add_argument('--pattern', '-p', choices=['daily', 'weekly', 'monthly', 'custom'],
                                     required=True, help='Recurrence pattern')
    add_recurring_parser.add_argument('--interval', '-i', type=int, default=1,
                                     help='Recurrence interval (default: 1)')
    add_recurring_parser.add_argument('--end-never', action='store_true',
                                     help='Never end recurrence (default)')
    add_recurring_parser.add_argument('--end-after', type=int,
                                     help='End after specified number of occurrences')
    add_recurring_parser.add_argument('--end-on',
                                     help='End on specific date (YYYY-MM-DD)')

    # Remove recurring task
    remove_recurring_parser = recurring_subparsers.add_parser('remove', help='Remove recurrence pattern from task')
    remove_recurring_parser.add_argument('task_id', help='Task ID to remove recurrence from')

    return parser


def main():
    """Main entry point"""
    parser = create_parser()
    args = parser.parse_args()

    # Initialize app
    app = TodoApp()

    # Handle commands
    if args.command == 'add':
        tags = args.tags.split(',') if args.tags else []
        app.add_task(args.title, args.description, args.due, args.priority, tags)

    elif args.command == 'list':
        tags = args.tags.split(',') if args.tags else None
        app.list_tasks(
            status=args.status if args.status != 'all' else None,
            priority=args.priority if args.priority != 'all' else None,
            tags=tags,
            due_date_range=args.due_date_range if args.due_date_range != 'all' else None,
            search_query=args.search or "",
            sort_by=args.sort_by,
            sort_order=args.order
        )

    elif args.command == 'complete':
        app.complete_task(args.task_id, not args.incomplete)

    elif args.command == 'delete':
        app.delete_task(args.task_id)

    elif args.command == 'update':
        tags = args.tags.split(',') if args.tags else None
        app.update_task(
            args.task_id,
            title=args.title,
            description=args.description,
            due_date=args.due,
            priority=args.priority,
            tags=tags
        )

    elif args.command == 'search':
        app.search_tasks(args.query)

    elif args.command == 'subtask':
        if args.subtask_command == 'add':
            app.add_subtask(args.task_id, args.title, args.completed)
        elif args.subtask_command == 'complete':
            app.complete_subtask(args.task_id, args.subtask_id, not args.incomplete)
        else:
            parser.print_help()

    elif args.command == 'stats':
        app.stats()

    elif args.command == 'recurring':
        if args.recurring_command == 'add':
            # Build end condition
            end_condition = {'type': 'never'}  # default

            if args.end_after:
                end_condition = {'type': 'after_count', 'value': args.end_after}
            elif args.end_on:
                end_condition = {'type': 'on_date', 'value': args.end_on}
            elif args.end_never:
                end_condition = {'type': 'never'}

            app.set_task_recurrence(args.task_id, args.pattern, args.interval, end_condition)
        elif args.recurring_command == 'remove':
            app.remove_task_recurrence(args.task_id)
        else:
            parser.print_help()

    else:
        parser.print_help()


if __name__ == '__main__':
    main()