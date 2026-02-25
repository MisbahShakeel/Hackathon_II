# CLI Todo Application

This is a command-line interface (CLI) todo application. The main application file `app.py` now runs as a CLI application instead of a web application. It provides all the functionality of the original web app but through a terminal interface.

## Features

- Add, list, complete, update, and delete tasks
- Subtask management
- Task filtering and sorting
- Search functionality
- Statistics reporting
- JSON file-based storage

## Usage

### Basic Commands

```bash
# Add a new task
python app.py add "Task title" --description "Task description" --priority high --due "2025-12-31" --tags work,important

# List all tasks
python app.py list

# List tasks with filters
python app.py list --status active --priority high --due-date overdue

# Complete a task
python app.py complete <task-id>

# Delete a task
python app.py delete <task-id>

# Search tasks
python app.py search "query"

# Show statistics
python app.py stats
```

### Advanced Filtering

```bash
# Filter by status
python todo_cli.py list --status completed

# Filter by priority
python todo_cli.py list --priority high

# Filter by tags
python todo_cli.py list --tags work

# Filter by due date
python todo_cli.py list --due-date today

# Sort tasks
python todo_cli.py list --sort priority --order desc
```

### Subtask Management

```bash
# Add a subtask
python todo_cli.py subtask add <task-id> "Subtask title"

# Complete a subtask
python todo_cli.py subtask complete <task-id> <subtask-id>
```

### Update Task

```bash
# Update task properties
python todo_cli.py update <task-id> --title "New title" --priority high
```

## Task Status Indicators

- `[x]` - Completed task
- `[ ]` - Active task
- `(H)` - High priority
- `(M)` - Medium priority
- `(L)` - Low priority

## Storage

Tasks are stored in `todo_tasks.json` in the same format as the web application, making it compatible with both versions.

## Requirements

- Python 3.7+
- No additional dependencies (uses built-in modules)