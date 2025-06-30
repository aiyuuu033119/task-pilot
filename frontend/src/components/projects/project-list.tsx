"use client"

import { useState, useEffect } from 'react'
import { Calendar, Clock, Users, Tag, MoreVertical, Edit, Trash, Eye } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { ProjectModal } from './project-modal'
import { useProjectStore } from '@/lib/project-store'
import { Project } from '@/types/project'
import { cn } from '@/lib/utils'

export function ProjectList() {
  const [editingProject, setEditingProject] = useState<Project | null>(null)
  const { getFilteredProjects, deleteProject, setLoading, setProjects } = useProjectStore()
  const projects = getFilteredProjects()

  // Mock data for development
  useEffect(() => {
    const mockProjects: Project[] = [
      {
        id: '1',
        name: 'E-commerce Platform Redesign',
        description: 'Complete overhaul of the existing e-commerce platform with modern UI/UX',
        status: 'active',
        priority: 'high',
        startDate: '2024-01-15',
        endDate: '2024-06-30',
        progress: 65,
        teamMembers: [
          { id: '1', name: 'John Doe', email: 'john@example.com', role: 'Project Manager' },
          { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'UI/UX Designer' },
        ],
        tags: ['frontend', 'design', 'e-commerce'],
        createdAt: '2024-01-10T10:00:00Z',
        updatedAt: '2024-03-15T14:30:00Z',
        userId: 'user123',
      },
      {
        id: '2',
        name: 'Mobile App Development',
        description: 'Native mobile application for iOS and Android platforms',
        status: 'active',
        priority: 'medium',
        startDate: '2024-02-01',
        endDate: '2024-08-31',
        progress: 40,
        teamMembers: [
          { id: '3', name: 'Bob Wilson', email: 'bob@example.com', role: 'Mobile Developer' },
        ],
        tags: ['mobile', 'ios', 'android'],
        createdAt: '2024-01-25T09:00:00Z',
        updatedAt: '2024-03-10T11:20:00Z',
        userId: 'user123',
      },
      {
        id: '3',
        name: 'API Integration',
        description: 'Integrate third-party APIs for payment and shipping',
        status: 'completed',
        priority: 'high',
        startDate: '2023-11-01',
        endDate: '2024-01-31',
        progress: 100,
        teamMembers: [
          { id: '4', name: 'Alice Brown', email: 'alice@example.com', role: 'Backend Developer' },
        ],
        tags: ['backend', 'api', 'integration'],
        createdAt: '2023-10-28T08:00:00Z',
        updatedAt: '2024-01-31T16:45:00Z',
        userId: 'user123',
      },
    ]
    
    setProjects(mockProjects)
  }, [setProjects])

  const handleDelete = async (id: string) => {
    if (confirm('Are you sure you want to delete this project?')) {
      deleteProject(id)
    }
  }

  const getStatusColor = (status: Project['status']) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'completed': return 'bg-blue-100 text-blue-800'
      case 'on-hold': return 'bg-yellow-100 text-yellow-800'
      case 'cancelled': return 'bg-red-100 text-red-800'
    }
  }

  const getPriorityColor = (priority: Project['priority']) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-gray-100 text-gray-800'
    }
  }

  if (projects.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No projects found. Create your first project!</p>
      </div>
    )
  }

  return (
    <>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {projects.map((project) => (
          <div
            key={project.id}
            className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow"
          >
            {/* Header */}
            <div className="flex justify-between items-start mb-4">
              <div className="flex-1">
                <h3 className="font-semibold text-lg mb-1">{project.name}</h3>
                <p className="text-sm text-gray-600 line-clamp-2">{project.description}</p>
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => setEditingProject(project)}>
                    <Edit className="mr-2 h-4 w-4" />
                    Edit
                  </DropdownMenuItem>
                  <DropdownMenuItem 
                    onClick={() => handleDelete(project.id)}
                    className="text-red-600"
                  >
                    <Trash className="mr-2 h-4 w-4" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            {/* Status and Priority */}
            <div className="flex gap-2 mb-4">
              <Badge className={cn('text-xs', getStatusColor(project.status))}>
                {project.status}
              </Badge>
              <Badge className={cn('text-xs', getPriorityColor(project.priority))}>
                {project.priority}
              </Badge>
            </div>

            {/* Progress */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Progress</span>
                <span className="font-medium">{project.progress}%</span>
              </div>
              <Progress value={project.progress} className="h-2" />
            </div>

            {/* Tags */}
            {project.tags.length > 0 && (
              <div className="flex items-center gap-2 mb-4 flex-wrap">
                <Tag className="w-3 h-3 text-gray-500" />
                {project.tags.map((tag) => (
                  <span key={tag} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Footer */}
            <div className="flex items-center justify-between text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <Calendar className="w-3 h-3" />
                <span>{new Date(project.startDate).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center gap-1">
                <Users className="w-3 h-3" />
                <span>{project.teamMembers.length}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Edit Modal */}
      {editingProject && (
        <ProjectModal
          isOpen={!!editingProject}
          onClose={() => setEditingProject(null)}
          project={editingProject}
        />
      )}
    </>
  )
}