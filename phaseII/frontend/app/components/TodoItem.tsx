'use client';

import { useState } from 'react';
import { Todo, TodoUpdate } from '../lib/types';
import { todoAPI } from '../lib/api';

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
    <li className="py-4 px-5 hover:bg-gray-50 transition-all duration-200 group">
      {isEditing ? (
        <div className="flex-grow mr-4">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="block w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm mb-2"
            placeholder="Todo title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="block w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            placeholder="Description (optional)"
            rows={2}
          />
          {error && (
            <div className="mt-2 text-sm text-red-600">{error}</div>
          )}
          <div className="mt-3 flex space-x-2">
            <button
              onClick={handleSaveEdit}
              disabled={loading}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 transition-all"
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
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-between">
          <div className="flex items-center flex-grow">
            <button
              onClick={handleToggleComplete}
              className={`h-5 w-5 flex items-center justify-center rounded-full border-2 flex-shrink-0 transition-all duration-200 ${
                todo.completed
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-gray-300 hover:border-indigo-400'
              }`}
              aria-label={todo.completed ? 'Mark as incomplete' : 'Mark as complete'}
            >
              {todo.completed && (
                <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              )}
            </button>
            <div className="ml-3 min-w-0 flex-1">
              <p
                className={`text-sm font-medium truncate ${
                  todo.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                }`}
              >
                {todo.title}
              </p>
              {todo.description && (
                <p className={`text-sm truncate ${todo.completed ? 'text-gray-400' : 'text-gray-500'}`}>
                  {todo.description}
                </p>
              )}
            </div>
          </div>
          
          <div className="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <span className="text-xs text-gray-400 hidden sm:inline">
              {new Date(todo.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
            </span>
            <button
              onClick={() => setIsEditing(true)}
              className="p-1.5 rounded-md text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 transition-all"
              aria-label="Edit todo"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              className="p-1.5 rounded-md text-gray-500 hover:text-red-600 hover:bg-red-50 transition-all"
              aria-label="Delete todo"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      )}
    </li>
  );
}