/**
 * Create Student Modal — form for adding single or bulk students
 */

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createStudent, bulkCreateStudents } from '../../api/admin';

interface CreateStudentModalProps {
  onClose: () => void;
}

export default function CreateStudentModal({ onClose }: CreateStudentModalProps) {
  const [mode, setMode] = useState<'single' | 'bulk'>('single');
  const [form, setForm] = useState({
    email: '',
    first_name: '',
    last_name: '',
    cohort: 'cohort-2026-q3',
  });
  const [bulkText, setBulkText] = useState('');
  const [bulkResults, setBulkResults] = useState<any>(null);

  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createStudent,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-students'] });
      onClose();
    },
  });

  const bulkMutation = useMutation({
    mutationFn: bulkCreateStudents,
    onSuccess: (data) => {
      setBulkResults(data);
      queryClient.invalidateQueries({ queryKey: ['admin-students'] });
    },
  });

  const handleSingleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    createMutation.mutate(form);
  };

  const handleBulkSubmit = () => {
    // Parse CSV: email, first_name, last_name, cohort
    const lines = bulkText.trim().split('\n').filter(Boolean);
    const students = lines.map((line) => {
      const [email, first_name, last_name, cohort] = line.split(',').map((s) => s.trim());
      return { email, first_name, last_name, cohort: cohort || form.cohort };
    });
    bulkMutation.mutate({ students });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-lg font-bold text-gray-900">Add Students</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Mode Tabs */}
        <div className="px-6 pt-4 flex gap-2">
          <button
            onClick={() => setMode('single')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              mode === 'single' ? 'bg-blue-100 text-blue-700' : 'text-gray-500 hover:bg-gray-100'
            }`}
          >
            Single
          </button>
          <button
            onClick={() => setMode('bulk')}
            className={`px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              mode === 'bulk' ? 'bg-blue-100 text-blue-700' : 'text-gray-500 hover:bg-gray-100'
            }`}
          >
            Bulk Import
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-4">
          {mode === 'single' ? (
            <form onSubmit={handleSingleSubmit} className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">First Name</label>
                  <input
                    type="text"
                    required
                    value={form.first_name}
                    onChange={(e) => setForm({ ...form, first_name: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-600 mb-1">Last Name</label>
                  <input
                    type="text"
                    required
                    value={form.last_name}
                    onChange={(e) => setForm({ ...form, last_name: e.target.value })}
                    className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Email</label>
                <input
                  type="email"
                  required
                  value={form.email}
                  onChange={(e) => setForm({ ...form, email: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500"
                  placeholder="student@example.com"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-600 mb-1">Cohort</label>
                <select
                  value={form.cohort}
                  onChange={(e) => setForm({ ...form, cohort: e.target.value })}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm"
                >
                  <option value="cohort-2026-q3">Q3 2026</option>
                  <option value="cohort-2026-q4">Q4 2026</option>
                  <option value="cohort-2027-q1">Q1 2027</option>
                </select>
              </div>
              <p className="text-xs text-gray-500">
                Student will receive an invitation email with a temporary password.
              </p>
              <button
                type="submit"
                disabled={createMutation.isPending}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium disabled:opacity-50"
              >
                {createMutation.isPending ? 'Creating...' : 'Create Student Account'}
              </button>
              {createMutation.isError && (
                <p className="text-xs text-red-600">
                  Error: {(createMutation.error as any)?.message || 'Failed to create account'}
                </p>
              )}
            </form>
          ) : (
            <div className="space-y-3">
              <p className="text-xs text-gray-500">
                Paste CSV data: <code>email, first_name, last_name, cohort</code> (one per line)
              </p>
              <textarea
                rows={8}
                value={bulkText}
                onChange={(e) => setBulkText(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm font-mono focus:ring-2 focus:ring-blue-500"
                placeholder="alice@uni.edu, Alice, Smith, cohort-2026-q3&#10;bob@uni.edu, Bob, Jones, cohort-2026-q3"
              />
              <button
                onClick={handleBulkSubmit}
                disabled={bulkMutation.isPending || !bulkText.trim()}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium disabled:opacity-50"
              >
                {bulkMutation.isPending ? 'Creating...' : 'Bulk Create'}
              </button>

              {/* Bulk Results */}
              {bulkResults && (
                <div className="bg-gray-50 rounded-lg p-3 text-xs space-y-1">
                  <p className="font-medium text-gray-700">
                    Created: {bulkResults.created} / {bulkResults.results.length}
                  </p>
                  {bulkResults.results
                    .filter((r: any) => r.status !== 'created')
                    .map((r: any) => (
                      <p key={r.email} className="text-red-600">
                        ✗ {r.email}: {r.error || r.status}
                      </p>
                    ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
