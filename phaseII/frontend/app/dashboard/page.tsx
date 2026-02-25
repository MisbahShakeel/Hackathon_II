'use client'

import { useEffect } from 'react';
import { useAtomValue } from 'jotai';
import { userAtom } from '../hooks/useAuth';
import TodoList from '../components/TodoList';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const user = useAtomValue(userAtom);
  const router = useRouter();

  useEffect(() => {
    if (!user) {
      router.push('/login');
      return;
    }
  }, [user, router]);

  if (!user) {
    return null; // Redirect happens in useEffect
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-cyan-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-10 animate-fade-in">
          <div className="relative inline-block">
            <div className="absolute -inset-1 bg-gradient-to-r from-indigo-400 to-cyan-400 rounded-lg blur opacity-75"></div>
            <h1 className="relative text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-cyan-600 mb-3">
              Welcome Back, {user.email.split('@')[0]}!
            </h1>
          </div>
          <p className="text-lg text-gray-600 mt-2">Manage your tasks efficiently</p>
        </div>

        <div className="bg-white rounded-2xl shadow-xl p-6 card border border-gray-100 overflow-hidden">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
            <div className="flex items-center">
              <div className="p-2 bg-indigo-100 rounded-lg mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-800">My Tasks</h2>
            </div>
            <div className="flex items-center text-sm text-gray-500 bg-gray-50 px-3 py-2 rounded-lg">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
            </div>
          </div>

          <TodoList userId={user.id} />
        </div>
      </div>
    </div>
  );
}