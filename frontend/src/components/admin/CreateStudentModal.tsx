/**
 * Create Student Modal — form for adding single or bulk students
 */

import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createStudent, bulkCreateStudents, CreatedStudent } from '../../api/admin';

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
  const [sendEmail, setSendEmail] = useState(true);
  const [createdCreds, setCreatedCreds] = useState<CreatedStudent | null>(null);
  const [copied, setCopied] = useState(false);
  const [bulkText, setBulkText] = useState('');
  const [bulkResults, setBulkResults] = useState<any>(null);

  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createStudent,
    onSuccess: (result: CreatedStudent) => {
      queryClient.invalidateQueries({ queryKey: ['admin-students'] });
      // If we created without an email, keep the modal open to show the temp
      // password (the instructor must copy it — it can't be retrieved later).
      if (!result.email_sent && result.temporary_password) {
        setCreatedCreds(result);
      } else {
        onClose();
      }
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
    createMutation.mutate({ ...form, send_email: sendEmail });
  };

  const copyCreds = () => {
    if (!createdCreds?.temporary_password) return;
    const text =
      `Teaching Agent login\n` +
      `URL: ${window.location.origin}\n` +
      `Email: ${createdCreds.email}\n` +
      `Temporary password: ${createdCreds.temporary_password}\n` +
      `(You'll be asked to set a new password on first login.)`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
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

        {/* Mode Tabs (hidden while showing created credentials) */}
        <div className={`px-6 pt-4 flex gap-2 ${createdCreds ? 'hidden' : ''}`}>
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
          {createdCreds ? (
            /* Post-create credentials (no-email mode) — shown once; copy now. */
            <div className="space-y-3">
              <div className="flex items-start gap-2 bg-green-50 border border-green-200 rounded-lg p-3">
                <span className="text-green-600">✅</span>
                <p className="text-sm text-green-800">
                  Account created for <span className="font-medium">{createdCreds.email}</span>.
                  Share the temporary password below — it won't be shown again.
                </p>
              </div>
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 text-sm space-y-1">
                <div className="flex justify-between gap-2">
                  <span className="text-gray-500">Email</span>
                  <span className="font-mono text-gray-900 break-all">{createdCreds.email}</span>
                </div>
                <div className="flex justify-between gap-2">
                  <span className="text-gray-500">Temp password</span>
                  <span className="font-mono font-semibold text-gray-900 break-all">
                    {createdCreds.temporary_password}
                  </span>
                </div>
              </div>
              <p className="text-xs text-gray-500">
                The student sets their own password on first login. If it expires
                (7 days) or is lost, use <span className="font-medium">Reset PW</span> on
                the student row.
              </p>
              <div className="flex gap-2">
                <button
                  onClick={copyCreds}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium"
                >
                  {copied ? '✓ Copied' : '📋 Copy login details'}
                </button>
                <button
                  onClick={() => {
                    setCreatedCreds(null);
                    setForm({ email: '', first_name: '', last_name: '', cohort: form.cohort });
                  }}
                  className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200"
                >
                  Add another
                </button>
                <button
                  onClick={onClose}
                  className="px-4 py-2 rounded-lg text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200"
                >
                  Done
                </button>
              </div>
            </div>
          ) : mode === 'single' ? (
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
              {/* Invitation method */}
              <label className="flex items-start gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={sendEmail}
                  onChange={(e) => setSendEmail(e.target.checked)}
                  className="mt-0.5"
                />
                <span className="text-xs text-gray-600">
                  <span className="font-medium text-gray-800">Send invitation email</span>
                  <br />
                  {sendEmail
                    ? 'Cognito emails the student a temporary password. Requires email delivery to be enabled (SES out of sandbox).'
                    : "No email is sent. You'll get a temporary password to share with the student directly — use this while email delivery is limited."}
                </span>
              </label>
              <button
                type="submit"
                disabled={createMutation.isPending}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg text-sm font-medium disabled:opacity-50"
              >
                {createMutation.isPending
                  ? 'Creating...'
                  : sendEmail
                    ? 'Create & Email Invitation'
                    : 'Create Student Account'}
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
