'use client';

import { useState, useEffect } from 'react';
import { Todo } from '@/lib/types';
import { todoAPI } from '@/lib/api';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';

interface TodoListProps {
  userId: string;
}

export default function TodoList({ userId }: TodoListProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTodos();
  }, [userId]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await todoAPI.getAll();
      setTodos(response.data);
      setError(null);
    } catch (err: any) {
      console.error('Failed to fetch todos:', err);
      setError('Failed to load todos');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = (newTodo: Todo) => {
    setTodos([newTodo, ...todos]);
  };

  const handleUpdateTodo = (updatedTodo: Todo) => {
    setTodos(todos.map(todo => todo.id === updatedTodo.id ? updatedTodo : todo));
  };

  const handleDeleteTodo = (id: string) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"></div>
        <p className="mt-2 text-gray-600">Loading todos...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4 mb-4">
        <div className="text-sm text-red-700">{error}</div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow overflow-hidden sm:rounded-lg">
      <div className="px-4 py-5 sm:px-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900">Your Todos</h3>
        <p className="mt-1 max-w-2xl text-sm text-gray-500">
          Manage your tasks efficiently
        </p>
      </div>
      <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
        <TodoForm onAddTodo={handleAddTodo} />
        
        {todos.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">No todos yet. Add your first todo above!</p>
          </div>
        ) : (
          <ul className="divide-y divide-gray-200">
            {todos.map((todo) => (
              <TodoItem
                key={todo.id}
                todo={todo}
                onUpdate={handleUpdateTodo}
                onDelete={handleDeleteTodo}
              />
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}