/**
 * Admin Dashboard — Main overview page
 * Shows KPI cards, daily trends chart, top topics, and common weaknesses
 */

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { fetchDashboard, fetchCosts } from '../../api/admin';
import MetricsCards from './MetricsCards';
import DailyTrendChart from './DailyTrendChart';
import TopTopics from './TopTopics';
import CostBreakdown from './CostBreakdown';
import WeaknessAlerts from './WeaknessAlerts';

export default function AdminDashboard() {
  const [period, setPeriod] = useState(30);

  const { data: dashboard, isLoading, error } = useQuery({
    queryKey: ['admin-dashboard', period],
    queryFn: () => fetchDashboard(period),
    refetchInterval: 60000, // Refresh every minute
  });

  const { data: costs } = useQuery({
    queryKey: ['admin-costs', period],
    queryFn: () => fetchCosts(period),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-3 text-gray-500">Loading dashboard...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-700">Failed to load dashboard data. Please try again.</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Instructor Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">
            Agentic AI Course — Student Activity & Analytics
          </p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-600">Period:</label>
          <select
            value={period}
            onChange={(e) => setPeriod(Number(e.target.value))}
            className="border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:ring-2 focus:ring-blue-500"
          >
            <option value={7}>Last 7 days</option>
            <option value={14}>Last 14 days</option>
            <option value={30}>Last 30 days</option>
            <option value={60}>Last 60 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      {/* KPI Cards */}
      {dashboard && <MetricsCards data={dashboard} />}

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Daily Trend (2/3 width) */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Daily Activity</h2>
          {dashboard && <DailyTrendChart metrics={dashboard.daily_metrics} />}
        </div>

        {/* Top Topics (1/3 width) */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Top Topics</h2>
          {dashboard && <TopTopics topics={dashboard.top_topics} />}
        </div>
      </div>

      {/* Second Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Cost Breakdown */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">AWS Cost Breakdown</h2>
          {costs && <CostBreakdown data={costs} />}
        </div>

        {/* Weakness Alerts */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            ⚠️ Common Weaknesses
          </h2>
          {dashboard && <WeaknessAlerts weaknesses={dashboard.common_weaknesses} />}
        </div>
      </div>
    </div>
  );
}
