'use client';

import { useState } from 'react';
import { Todo, TodoUpdate } from '@/lib/types';
import { todoAPI } from '@/lib/api';

interface TodoItemProps {
  todo: Todo;
  onUpdate: (updatedTodo: Todo) => void;
  onDelete: (id: string) => void;
}

export default function TodoItem({ todo, onUpdate, onDelete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleToggleComplete = async () => {
    try {
      const updateData: TodoUpdate = {
        completed: !todo.completed
      };

      const response = await todoAPI.update(todo.id, updateData);
      onUpdate(response.data);
    } catch (err: any) {
      console.error('Failed to update todo:', err);
      setError('Failed to update todo');
    }
  };

  const handleSaveEdit = async () => {
    if (!editTitle.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const updateData: TodoUpdate = {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      };

      const response = await todoAPI.update(todo.id, updateData);
      onUpdate(response.data);
      setIsEditing(false);
    } catch (err: any) {
      console.error('Failed to update todo:', err);
      setError(err.message || 'Failed to update todo');
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await todoAPI.delete(todo.id);
        onDelete(todo.id);
      } catch (err: any) {
        console.error('Failed to delete todo:', err);
        setError('Failed to delete todo');
      }
    }
  };

  return (
    <li className="py-4 flex items-center justify-between">
      {isEditing ? (
        <div className="flex-grow mr-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm mb-2"
            placeholder="Todo title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Description (optional)"
            rows={2}
          />
          {error && (
            <div className="mt-2 text-sm text-red-600">{error}</div>
          )}
          <div className="mt-2 flex space-x-2">
            <button
              onClick={handleSaveEdit}
              disabled={loading}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={() => {
                setIsEditing(false);
                setEditTitle(todo.title);
                setEditDescription(todo.description || '');
                setError(null);
              }}
              className="inline-flex items-center px-3 py-1 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="flex items-center">
            <input
              id={`todo-${todo.id}`}
              type="checkbox"
              checked={todo.completed}
              onChange={handleToggleComplete}
              className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            />
            <label
              htmlFor={`todo-${todo.id}`}
              className={`ml-3 block text-sm font-medium ${
                todo.completed ? 'text-gray-500 line-through' : 'text-gray-700'
              }`}
            >
              {todo.title}
            </label>
            {todo.description && (
              <span className="ml-2 text-sm text-gray-500">{todo.description}</span>
            )}
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-500">
              {new Date(todo.created_at).toLocaleDateString()}
            </span>
            <button
              onClick={() => setIsEditing(true)}
              className="ml-2 inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Edit
            </button>
            <button
              onClick={handleDelete}
              className="ml-1 inline-flex items-center px-2.5 py-0.5 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
            >
              Delete
            </button>
          </div>
        </>
      )}
    </li>
  );
}