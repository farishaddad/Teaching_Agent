/**
 * Course Materials — list/upload/delete objects in the RAG S3 bucket and
 * trigger a Knowledge Base re-sync (ingestion) so new material is searchable.
 */

import { useRef, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  listMaterials,
  deleteMaterial,
  syncKnowledgeBase,
  uploadMaterial,
  MaterialItem,
} from '../../api/admin';

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

function formatDate(iso: string): string {
  const d = new Date(iso);
  return isNaN(d.getTime()) ? iso : d.toLocaleString();
}

export default function MaterialsList() {
  const queryClient = useQueryClient();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);

  const { data, isLoading, error } = useQuery({
    queryKey: ['admin-materials'],
    queryFn: () => listMaterials(),
  });

  const items = data?.items ?? [];

  const deleteMutation = useMutation({
    mutationFn: deleteMaterial,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['admin-materials'] }),
    onError: (err: Error) => alert(`Delete failed: ${err.message}`),
  });

  const syncMutation = useMutation({
    mutationFn: syncKnowledgeBase,
    onSuccess: (result: { jobs?: unknown[] }) => {
      const n = Array.isArray(result?.jobs) ? result.jobs.length : 0;
      alert(
        `Knowledge Base sync started (${n} data source${n === 1 ? '' : 's'}). ` +
        `Ingestion runs in the background and may take a few minutes.`
      );
    },
    onError: (err: Error) => alert(`Sync failed: ${err.message}`),
  });

  async function handleFileSelected(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    // Reset the input so selecting the same file again re-triggers change.
    if (fileInputRef.current) fileInputRef.current.value = '';
    if (!file) return;

    setUploading(true);
    try {
      await uploadMaterial(file);
      await queryClient.invalidateQueries({ queryKey: ['admin-materials'] });
    } catch (err) {
      alert(`Upload failed: ${(err as Error).message}`);
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Course Materials</h1>
          {data?.bucket && (
            <p className="text-xs text-gray-400 mt-0.5 font-mono">{data.bucket}</p>
          )}
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => syncMutation.mutate()}
            disabled={syncMutation.isPending}
            className="bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {syncMutation.isPending ? 'Syncing…' : '↻ Sync Knowledge Base'}
          </button>
          <button
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {uploading ? 'Uploading…' : '+ Upload File'}
          </button>
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            onChange={handleFileSelected}
            accept=".pdf,.md,.txt,.docx,.pptx,.html,.csv,.json"
          />
        </div>
      </div>

      <p className="text-xs text-gray-500">
        Files uploaded here are stored in the RAG source bucket. After adding or
        removing files, click <span className="font-medium">Sync Knowledge Base</span> to
        re-index them so the assistant can use the updated content.
      </p>

      {/* Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">File</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Size</th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Modified</th>
              <th className="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {isLoading ? (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-gray-400">
                  Loading materials…
                </td>
              </tr>
            ) : error ? (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-red-500">
                  Failed to load materials: {(error as Error).message}
                </td>
              </tr>
            ) : items.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-4 py-8 text-center text-gray-400">
                  No materials uploaded yet.
                </td>
              </tr>
            ) : (
              items.map((item: MaterialItem) => (
                <tr key={item.key} className="hover:bg-gray-50">
                  <td className="px-4 py-3 text-sm font-medium text-gray-900 break-all">
                    {item.key}
                  </td>
                  <td className="px-4 py-3 text-right text-sm text-gray-600 whitespace-nowrap">
                    {formatSize(item.size)}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-600 whitespace-nowrap">
                    {formatDate(item.last_modified)}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => {
                        if (confirm(`Delete "${item.key}"? This removes it from the source bucket.`)) {
                          deleteMutation.mutate(item.key);
                        }
                      }}
                      disabled={deleteMutation.isPending}
                      className="text-red-600 hover:text-red-800 text-xs font-medium disabled:opacity-50"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Summary */}
      <p className="text-xs text-gray-400">
        {items.length} file{items.length === 1 ? '' : 's'}
      </p>
    </div>
  );
}
