#!/usr/bin/env python3
"""
CLI Todo Application - Manage your tasks from the command line
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class TaskManager:
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks = self.load_tasks()
        self.next_id = self._get_next_id()

    def load_tasks(self) -> Dict[str, Any]:
        """Load tasks from the data file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"tasks": {}, "subtasks": {}}
        return {"tasks": {}, "subtasks": {}}

    def _get_next_id(self) -> int:
        """Get the next available numeric ID."""
        all_task_ids = list(self.tasks["tasks"].keys()) + list(self.tasks["subtasks"].keys())
        if not all_task_ids:
            return 1
        numeric_ids = []
        for task_id in all_task_ids:
            try:
                numeric_ids.append(int(task_id))
            except ValueError:
                continue  # Skip non-numeric IDs
        return max(numeric_ids) + 1 if numeric_ids else 1

    def save_tasks(self):
        """Save tasks to the data file."""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=2, default=str)

        # Update next_id after saving
        self.next_id = self._get_next_id()

    def generate_task_id(self) -> str:
        """Generate a unique numeric task ID."""
        task_id = str(self.next_id)
        self.next_id += 1
        return task_id

    def add_task(self, title: str, priority: str = "medium", due_date: Optional[str] = None,
                 tags: List[str] = None, parent_id: Optional[str] = None) -> str:
        """Add a new task."""
        task_id = self.generate_task_id()
        task = {
            "id": task_id,
            "title": title,
            "priority": priority.lower(),
            "due_date": due_date,
            "tags": tags or [],
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "parent_id": parent_id
        }

        if parent_id:
            self.tasks["subtasks"][task_id] = task
        else:
            self.tasks["tasks"][task_id] = task

        self.save_tasks()
        return task_id

    def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None,
                   due_date_filter: Optional[str] = None, tags: List[str] = None) -> List[Dict[str, Any]]:
        """List tasks based on filters."""
        tasks = list(self.tasks["tasks"].values())

        # Apply filters
        if status:
            tasks = [t for t in tasks if t["status"] == status]

        if priority:
            tasks = [t for t in tasks if t["priority"] == priority.lower()]

        if due_date_filter:
            now = datetime.now()
            if due_date_filter == "overdue":
                tasks = [t for t in tasks if t["due_date"] and datetime.fromisoformat(t["due_date"]) < now and t["status"] != "completed"]
            elif due_date_filter == "today":
                today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                today_end = today_start + timedelta(days=1)
                tasks = [t for t in tasks if t["due_date"] and
                         today_start <= datetime.fromisoformat(t["due_date"]) < today_end]
            elif due_date_filter == "week":
                week_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
                week_end = week_start + timedelta(days=7)
                tasks = [t for t in tasks if t["due_date"] and
                         week_start <= datetime.fromisoformat(t["due_date"]) < week_end]

        if tags:
            for tag in tags:
                tasks = [t for t in tasks if tag in t["tags"]]

        return sorted(tasks, key=lambda x: (x["priority"] == "high", x["priority"] == "medium", x.get("due_date", "")), reverse=True)

    def complete_task(self, task_id: str) -> bool:
        """Mark a task as complete."""
        if task_id in self.tasks["tasks"]:
            self.tasks["tasks"][task_id]["status"] = "completed"
            self.tasks["tasks"][task_id]["completed_at"] = datetime.now().isoformat()
            self.save_tasks()
            return True
        elif task_id in self.tasks["subtasks"]:
            self.tasks["subtasks"][task_id]["status"] = "completed"
            self.tasks["subtasks"][task_id]["completed_at"] = datetime.now().isoformat()
            self.save_tasks()
            return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """Delete a task."""
        if task_id in self.tasks["tasks"]:
            # Also delete subtasks
            subtasks_to_delete = [sid for sid, subtask in self.tasks["subtasks"].items() if subtask["parent_id"] == task_id]
            for sid in subtasks_to_delete:
                del self.tasks["subtasks"][sid]

            del self.tasks["tasks"][task_id]
            self.save_tasks()
            return True
        elif task_id in self.tasks["subtasks"]:
            del self.tasks["subtasks"][task_id]
            self.save_tasks()
            return True
        return False

    def update_task(self, task_id: str, **kwargs) -> bool:
        """Update task properties."""
        target_task = None

        if task_id in self.tasks["tasks"]:
            target_task = self.tasks["tasks"][task_id]
        elif task_id in self.tasks["subtasks"]:
            target_task = self.tasks["subtasks"][task_id]

        if target_task:
            for key, value in kwargs.items():
                if key in target_task and value is not None:
                    target_task[key] = value
            self.save_tasks()
            return True
        return False

    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """Search tasks by title or tags."""
        all_tasks = list(self.tasks["tasks"].values()) + list(self.tasks["subtasks"].values())
        query_lower = query.lower()
        return [t for t in all_tasks if query_lower in t["title"].lower() or
                any(query_lower in tag.lower() for tag in t["tags"])]

    def add_subtask(self, parent_id: str, title: str, priority: str = "medium",
                    due_date: Optional[str] = None, tags: List[str] = None) -> str:
        """Add a subtask to a parent task."""
        if parent_id not in self.tasks["tasks"]:
            raise ValueError(f"Parent task {parent_id} does not exist")

        return self.add_task(title, priority, due_date, tags, parent_id)

    def get_subtasks(self, parent_id: str) -> List[Dict[str, Any]]:
        """Get all subtasks for a parent task."""
        return [t for t in self.tasks["subtasks"].values() if t["parent_id"] == parent_id]

    def get_task_stats(self) -> Dict[str, Any]:
        """Get task statistics."""
        all_tasks = list(self.tasks["tasks"].values())
        completed_tasks = [t for t in all_tasks if t["status"] == "completed"]
        active_tasks = [t for t in all_tasks if t["status"] == "active"]
        overdue_tasks = [t for t in active_tasks if t["due_date"] and
                         datetime.fromisoformat(t["due_date"]) < datetime.now()]

        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for task in all_tasks:
            if task["priority"] in priority_counts:
                priority_counts[task["priority"]] += 1

        return {
            "total_tasks": len(all_tasks),
            "completed_tasks": len(completed_tasks),
            "active_tasks": len(active_tasks),
            "overdue_tasks": len(overdue_tasks),
            "priority_breakdown": priority_counts,
            "completion_rate": len(completed_tasks) / len(all_tasks) * 100 if all_tasks else 0
        }

    def add_recurring_task(self, title: str, priority: str, due_date: str,
                          recurrence: str, tags: List[str] = None) -> str:
        """Add a recurring task."""
        task_id = self.add_task(title, priority, due_date, tags)
        # In a real implementation, we would schedule the recurrence
        # For now, we just add it as a regular task with a recurrence note
        self.tasks["tasks"][task_id]["recurrence"] = recurrence
        self.save_tasks()
        return task_id


def setup_parser():
    """Set up the argument parser."""
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
        """.strip()
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium', help='Task priority')
    add_parser.add_argument('--due', dest='due_date', help='Due date (YYYY-MM-DD)')
    add_parser.add_argument('--tags', help='Comma-separated tags')

    # List command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--status', choices=['active', 'completed'], help='Filter by status')
    list_parser.add_argument('--priority', choices=['low', 'medium', 'high'], help='Filter by priority')
    list_parser.add_argument('--due-date', dest='due_date_filter', choices=['overdue', 'today', 'week'],
                            help='Filter by due date')
    list_parser.add_argument('--tags', help='Filter by tags (comma-separated)')

    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark task as complete')
    complete_parser.add_argument('task_id', help='Task ID to complete')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('task_id', help='Task ID to delete')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update task properties')
    update_parser.add_argument('task_id', help='Task ID to update')
    update_parser.add_argument('--title', help='New task title')
    update_parser.add_argument('--priority', choices=['low', 'medium', 'high'], help='New priority')
    update_parser.add_argument('--due', dest='due_date', help='New due date (YYYY-MM-DD)')
    update_parser.add_argument('--status', choices=['active', 'completed'], help='New status')
    update_parser.add_argument('--tags', help='New tags (comma-separated)')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks')
    search_parser.add_argument('query', help='Search query')

    # Subtask command
    subtask_parser = subparsers.add_parser('subtask', help='Manage subtasks')
    subtask_subparsers = subtask_parser.add_subparsers(dest='subtask_command', help='Subtask commands')

    # Subtask add
    subtask_add_parser = subtask_subparsers.add_parser('add', help='Add a subtask')
    subtask_add_parser.add_argument('parent_id', help='Parent task ID')
    subtask_add_parser.add_argument('title', help='Subtask title')
    subtask_add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium', help='Subtask priority')
    subtask_add_parser.add_argument('--due', dest='due_date', help='Due date (YYYY-MM-DD)')
    subtask_add_parser.add_argument('--tags', help='Comma-separated tags')

    # Stats command
    subparsers.add_parser('stats', help='Show task statistics')

    # Recurring command
    recurring_parser = subparsers.add_parser('recurring', help='Manage recurring tasks')
    recurring_subparsers = recurring_parser.add_subparsers(dest='recurring_command', help='Recurring task commands')

    # Recurring add
    recurring_add_parser = recurring_subparsers.add_parser('add', help='Add a recurring task')
    recurring_add_parser.add_argument('title', help='Recurring task title')
    recurring_add_parser.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium', help='Task priority')
    recurring_add_parser.add_argument('--due', dest='due_date', help='Due date (YYYY-MM-DD)')
    recurring_add_parser.add_argument('--recurrence', choices=['daily', 'weekly', 'monthly', 'yearly'],
                                     default='weekly', help='Recurrence pattern')
    recurring_add_parser.add_argument('--tags', help='Comma-separated tags')

    return parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    task_manager = TaskManager()

    try:
        if args.command == 'add':
            tags = args.tags.split(',') if args.tags else []
            task_id = task_manager.add_task(args.title, args.priority, args.due_date, tags)
            print(f"Task added successfully with ID: {task_id}")

        elif args.command == 'list':
            tags = args.tags.split(',') if args.tags else None
            tasks = task_manager.list_tasks(args.status, args.priority, args.due_date_filter, tags)

            if not tasks:
                print("No tasks found.")
                return

            print(f"Found {len(tasks)} task(s):")
            for task in tasks:
                status_icon = "COMPLETED" if task["status"] == "completed" else "ACTIVE"
                priority = task["priority"].upper()
                due_date = task["due_date"] or "No due date"
                tags_str = ", ".join(task["tags"]) if task["tags"] else "No tags"

                print(f"[{status_icon}] [{task['id'][:8]}...] {task['title']} | "
                      f"Priority: {priority} | Due: {due_date} | Tags: {tags_str}")

        elif args.command == 'complete':
            if task_manager.complete_task(args.task_id):
                print(f"Task {args.task_id} marked as complete!")
            else:
                print(f"Task {args.task_id} not found!")

        elif args.command == 'delete':
            if task_manager.delete_task(args.task_id):
                print(f"Task {args.task_id} deleted successfully!")
            else:
                print(f"Task {args.task_id} not found!")

        elif args.command == 'update':
            update_data = {}
            if args.title is not None:
                update_data['title'] = args.title
            if args.priority is not None:
                update_data['priority'] = args.priority
            if args.due_date is not None:
                update_data['due_date'] = args.due_date
            if args.status is not None:
                update_data['status'] = args.status
            if args.tags is not None:
                update_data['tags'] = args.tags.split(',')

            if task_manager.update_task(args.task_id, **update_data):
                print(f"Task {args.task_id} updated successfully!")
            else:
                print(f"Task {args.task_id} not found!")

        elif args.command == 'search':
            tasks = task_manager.search_tasks(args.query)
            if not tasks:
                print(f"No tasks found for query '{args.query}'")
                return

            print(f"Found {len(tasks)} task(s) for query '{args.query}':")
            for task in tasks:
                status_icon = "COMPLETED" if task["status"] == "completed" else "ACTIVE"
                priority = task["priority"].upper()
                due_date = task["due_date"] or "No due date"
                tags_str = ", ".join(task["tags"]) if task["tags"] else "No tags"

                print(f"[{status_icon}] [{task['id'][:8]}...] {task['title']} | "
                      f"Priority: {priority} | Due: {due_date} | Tags: {tags_str}")

        elif args.command == 'subtask':
            if args.subtask_command == 'add':
                tags = args.tags.split(',') if args.tags else []
                try:
                    task_id = task_manager.add_subtask(args.parent_id, args.title, args.priority, args.due_date, tags)
                    print(f"Subtask added successfully with ID: {task_id}")
                except ValueError as e:
                    print(f"Error: {e}")
            else:
                print("Subcommand required. Use 'subtask add <parent-id> <title>'")

        elif args.command == 'stats':
            stats = task_manager.get_task_stats()
            print("Task Statistics:")
            print(f"  Total tasks: {stats['total_tasks']}")
            print(f"  Completed tasks: {stats['completed_tasks']}")
            print(f"  Active tasks: {stats['active_tasks']}")
            print(f"  Overdue tasks: {stats['overdue_tasks']}")
            print(f"  Completion rate: {stats['completion_rate']:.1f}%")
            print("  Priority breakdown:")
            for priority, count in stats['priority_breakdown'].items():
                print(f"    {priority.capitalize()}: {count}")

        elif args.command == 'recurring':
            if args.recurring_command == 'add':
                tags = args.tags.split(',') if args.tags else []
                task_id = task_manager.add_recurring_task(args.title, args.priority, args.due_date,
                                                        args.recurrence, tags)
                print(f"Recurring task added successfully with ID: {task_id}")
            else:
                print("Subcommand required. Use 'recurring add <title> [options]'")

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()