'use client';

import { useState, useEffect } from 'react';
import { Todo } from '../lib/types';
import { todoAPI } from '../lib/api';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';

interface TodoListProps {
  userId: string;
}

export default function TodoList({ userId }: TodoListProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [filteredTodos, setFilteredTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchTodos();
  }, [userId]);

  // Filter todos based on search term
  useEffect(() => {
    if (searchTerm.trim() === '') {
      setFilteredTodos(todos);
    } else {
      const filtered = todos.filter(todo => 
        todo.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (todo.description && todo.description.toLowerCase().includes(searchTerm.toLowerCase()))
      );
      setFilteredTodos(filtered);
    }
  }, [searchTerm, todos]);

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

  // Calculate stats
  const totalTodos = todos.length;
  const completedTodos = todos.filter(todo => todo.completed).length;
  const pendingTodos = totalTodos - completedTodos;

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-indigo-500 mb-4"></div>
        <p className="text-gray-600">Loading your tasks...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-lg">
        <div className="flex">
          <div className="flex-shrink-0">
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
          <div className="ml-3">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stats Section */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 rounded-xl p-5 text-center shadow-sm border border-indigo-100">
          <div className="text-3xl font-bold text-indigo-700 mb-1">{totalTodos}</div>
          <div className="text-sm text-indigo-600 font-medium">Total Tasks</div>
        </div>
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-5 text-center shadow-sm border border-green-100">
          <div className="text-3xl font-bold text-green-700 mb-1">{completedTodos}</div>
          <div className="text-sm text-green-600 font-medium">Completed</div>
        </div>
        <div className="bg-gradient-to-br from-amber-50 to-amber-100 rounded-xl p-5 text-center shadow-sm border border-amber-100">
          <div className="text-3xl font-bold text-amber-700 mb-1">{pendingTodos}</div>
          <div className="text-sm text-amber-600 font-medium">Pending</div>
        </div>
      </div>

      {/* Add Todo Form */}
      <div className="bg-gradient-to-br from-gray-50 to-gray-100 p-5 rounded-xl border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <div className="p-2 bg-indigo-100 rounded-lg mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </div>
          Add New Task
        </h3>
        <TodoForm onAddTodo={handleAddTodo} />
      </div>

      {/* Todo List */}
      <div>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center">
            <div className="p-2 bg-indigo-100 rounded-lg mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            Your Tasks ({filteredTodos.length})
          </h3>
          
          {/* Search Bar */}
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>

        {filteredTodos.length === 0 ? (
          <div className="text-center py-12 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border-2 border-dashed border-gray-200">
            {todos.length === 0 ? (
              <>
                <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-gray-100 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks yet</h3>
                <p className="mt-1 text-gray-500">Get started by adding a new task.</p>
              </>
            ) : (
              <>
                <div className="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-gray-100 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks found</h3>
                <p className="mt-1 text-gray-500">Try adjusting your search terms.</p>
              </>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <ul className="divide-y divide-gray-100">
              {filteredTodos.map((todo) => (
                <TodoItem
                  key={todo.id}
                  todo={todo}
                  onUpdate={handleUpdateTodo}
                  onDelete={handleDeleteTodo}
                />
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}