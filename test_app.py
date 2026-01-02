from task_model import Task, Subtask
from storage_service import StorageService
from filter_service import FilterService
from sort_service import SortService
from datetime import datetime, timedelta


def main():
    print("Testing Todo App Python Implementation")
    print("=" * 50)

    # Create some sample tasks
    task1_data = {
        'title': 'Complete project proposal',
        'description': 'Write and submit the project proposal',
        'due_date': (datetime.now() + timedelta(days=2)).isoformat(),
        'priority': 'high',
        'tags': ['work', 'important'],
        'subtasks': [
            {'title': 'Research', 'completed': True},
            {'title': 'Write draft', 'completed': False},
            {'title': 'Review', 'completed': False}
        ]
    }

    task2_data = {
        'title': 'Buy groceries',
        'description': 'Get groceries for the week',
        'due_date': datetime.now().isoformat(),
        'priority': 'medium',
        'tags': ['personal', 'shopping'],
        'subtasks': [
            {'title': 'Milk', 'completed': False},
            {'title': 'Bread', 'completed': True}
        ]
    }

    task3_data = {
        'title': 'Call dentist',
        'description': 'Schedule appointment',
        'due_date': (datetime.now() - timedelta(days=1)).isoformat(),  # Overdue
        'priority': 'low',
        'tags': ['personal'],
        'subtasks': []
    }

    # Create tasks
    task1 = Task(task1_data)
    task2 = Task(task2_data)
    task3 = Task(task3_data)

    tasks = [task1, task2, task3]
    print(f"Created {len(tasks)} tasks")

    # Test storage service
    storage = StorageService()
    storage.save_tasks(tasks)
    print("Tasks saved to storage")

    loaded_tasks = storage.load_tasks()
    print(f"Loaded {len(loaded_tasks)} tasks from storage")

    # Test filter service
    filter_service = FilterService()

    # Search for tasks
    search_results = filter_service.search_tasks(loaded_tasks, "project")
    print(f"Search results for 'project': {len(search_results)} tasks")

    # Filter by priority
    high_priority_tasks = filter_service.get_tasks_by_priority(loaded_tasks, "high")
    print(f"High priority tasks: {len(high_priority_tasks)}")

    # Get overdue tasks
    overdue_tasks = filter_service.get_overdue_tasks(loaded_tasks)
    print(f"Overdue tasks: {len(overdue_tasks)}")

    # Test sort service
    sort_service = SortService()

    # Sort by due date
    sorted_tasks = sort_service.sort_tasks(loaded_tasks, 'dueDate', 'asc')
    print("Tasks sorted by due date")

    # Print task details
    print("\nTask Details:")
    for i, task in enumerate(loaded_tasks, 1):
        print(f"\nTask {i}: {task.title}")
        print(f"  Description: {task.description}")
        print(f"  Due Date: {task.due_date}")
        print(f"  Priority: {task.priority}")
        print(f"  Tags: {', '.join(task.tags)}")
        print(f"  Completed: {task.completed}")
        print(f"  Is Overdue: {task.is_overdue()}")

        completion = task.get_subtask_completion()
        print(f"  Subtasks: {completion['completed']}/{completion['total']} ({completion['percentage']}%)")


if __name__ == "__main__":
    main()