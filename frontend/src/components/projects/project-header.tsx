"use client"

import { useState } from 'react'
import { Plus, Filter, Search } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { ProjectModal } from './project-modal'
import { useProjectStore } from '@/lib/project-store'

export function ProjectHeader() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const { filter, setFilter, getProjectStats } = useProjectStore()
  const stats = getProjectStats()

  const handleSearch = (value: string) => {
    setFilter({ ...filter, search: value })
  }

  const handleStatusFilter = (value: string) => {
    setFilter({ 
      ...filter, 
      status: value === 'all' ? undefined : value as any 
    })
  }

  const handlePriorityFilter = (value: string) => {
    setFilter({ 
      ...filter, 
      priority: value === 'all' ? undefined : value as any 
    })
  }

  return (
    <>
      <div className="mb-6">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600">Total Projects</p>
            <p className="text-2xl font-semibold">{stats.total}</p>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600">Active</p>
            <p className="text-2xl font-semibold text-green-600">{stats.active}</p>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600">Completed</p>
            <p className="text-2xl font-semibold text-blue-600">{stats.completed}</p>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600">On Hold</p>
            <p className="text-2xl font-semibold text-yellow-600">{stats.onHold}</p>
          </div>
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600">Cancelled</p>
            <p className="text-2xl font-semibold text-red-600">{stats.cancelled}</p>
          </div>
        </div>

        {/* Actions and Filters */}
        <div className="flex flex-col md:flex-row gap-4">
          <Button 
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            New Project
          </Button>

          <div className="flex-1 flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
              <Input
                placeholder="Search projects..."
                value={filter.search || ''}
                onChange={(e) => handleSearch(e.target.value)}
                className="pl-10"
              />
            </div>

            {/* Status Filter */}
            <Select
              value={filter.status || 'all'}
              onValueChange={handleStatusFilter}
            >
              <SelectTrigger className="w-full md:w-[180px]">
                <SelectValue placeholder="All Status" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Status</SelectItem>
                <SelectItem value="active">Active</SelectItem>
                <SelectItem value="completed">Completed</SelectItem>
                <SelectItem value="on-hold">On Hold</SelectItem>
                <SelectItem value="cancelled">Cancelled</SelectItem>
              </SelectContent>
            </Select>

            {/* Priority Filter */}
            <Select
              value={filter.priority || 'all'}
              onValueChange={handlePriorityFilter}
            >
              <SelectTrigger className="w-full md:w-[180px]">
                <SelectValue placeholder="All Priority" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Priority</SelectItem>
                <SelectItem value="high">High</SelectItem>
                <SelectItem value="medium">Medium</SelectItem>
                <SelectItem value="low">Low</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      {/* Create/Edit Modal */}
      {showCreateModal && (
        <ProjectModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
        />
      )}
    </>
  )
}