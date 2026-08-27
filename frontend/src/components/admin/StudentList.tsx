/**
 * Student List & Management — table with search, filter, and actions
 */

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { listStudents, createStudent, disableStudent, resetPassword } from '../../api/admin';
import CreateStudentModal from './CreateStudentModal';
import StudentProgressModal from './StudentProgressModal';

interface Student {
  student_id: string;
  email: string;
  first_name: string;
  last_name: string;
  cohort: string;
  enrollment_date: string;
  enabled: boolean;
  total_interactions: number;
  total_tokens_used: number;
}

export default function StudentList() {
  const [search, setSearch] = useState('');
  const [cohortFilter, setCohortFilter] = useState<string>('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<string | null>(null);

  const queryClient = useQueryClient();

  const { data: students = [], isLoading } = useQuery({
    queryKey: ['admin-students', cohortFilter],
    queryFn: () => listStudents(cohortFilter || undefined),
  });

  const disableMutation = useMutation({
    mutationFn: disableStudent,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-students'] }),
  });

  const resetMutation = useMutation({
    mutationFn: resetPassword,
    onSuccess: () => alert('Password reset email sent.'),
  });

  const filteredStudents = students.filter(
    (s: Student) =>
      s.email.toLowerCase().includes(search.toLowerCase()) ||
      s.first_name.toLowerCase().includes(search.toLowerCase()) ||
      s.last_name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Student Management</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          + Add Student
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Search by name or email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 border border-gray-300 rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        />
        <select
          value={cohortFilter}
          onChange={(e) => setCohortFilter(e.target.value)}
          className="border border-gray-300 rounded-lg px-3 py-2 text-sm"
        >
          <option value="">All Cohorts</option>
          <option value="cohort-2026-q3">Q3 2026</option>
          <option value="cohort-2026-q4">Q4 2026</option>
        </select>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Student</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Cohort</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Enrolled</th>
              <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Interactions</th>
              <th className="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {isLoading ? (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-gray-400">
                  Loading students...
                </td>
              </tr>
            ) : filteredStudents.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-gray-400">
                  No students found.
                </td>
              </tr>
            ) : (
              filteredStudents.map((student: Student) => (
                <tr key={student.student_id} className="hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {student.first_name} {student.last_name}
                      </p>
                      <p className="text-xs text-gray-500">{student.email}</p>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600">{student.cohort}</td>
                  <td className="px-4 py-3 text-sm text-gray-600">{student.enrollment_date}</td>
                  <td className="px-4 py-3 text-center text-sm font-medium">
                    {student.total_interactions}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span
                      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                        student.enabled
                          ? 'bg-green-100 text-green-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {student.enabled ? 'Active' : 'Disabled'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => setSelectedStudent(student.student_id)}
                        className="text-blue-600 hover:text-blue-800 text-xs font-medium"
                      >
                        Progress
                      </button>
                      <button
                        onClick={() => resetMutation.mutate(student.student_id)}
                        className="text-amber-600 hover:text-amber-800 text-xs font-medium"
                      >
                        Reset PW
                      </button>
                      <button
                        onClick={() => {
                          if (confirm(`Disable ${student.first_name}'s account?`)) {
                            disableMutation.mutate(student.student_id);
                          }
                        }}
                        className="text-red-600 hover:text-red-800 text-xs font-medium"
                        disabled={!student.enabled}
                      >
                        Disable
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Summary */}
      <p className="text-xs text-gray-400">
        Showing {filteredStudents.length} of {students.length} students
      </p>

      {/* Modals */}
      {showCreateModal && (
        <CreateStudentModal onClose={() => setShowCreateModal(false)} />
      )}
      {selectedStudent && (
        <StudentProgressModal
          studentId={selectedStudent}
          onClose={() => setSelectedStudent(null)}
        />
      )}
    </div>
  );
}
