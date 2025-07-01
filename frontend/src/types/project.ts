export interface Project {
  id: string
  name: string
  description: string
  status: 'active' | 'completed' | 'on-hold' | 'cancelled'
  priority: 'low' | 'medium' | 'high'
  startDate: string
  endDate?: string
  progress: number
  teamMembers: TeamMember[]
  tags: string[]
  createdAt: string
  updatedAt: string
  userId: string
}

export interface TeamMember {
  id: string
  name: string
  email: string
  role: string
  avatar?: string
}

export interface ProjectStats {
  total: number
  active: number
  completed: number
  onHold: number
  cancelled: number
}

export interface ProjectFilter {
  status?: Project['status']
  priority?: Project['priority']
  search?: string
  tags?: string[]
  dateRange?: {
    start: string
    end: string
  }
}

export interface CreateProjectDto {
  name: string
  description: string
  status: Project['status']
  priority: Project['priority']
  startDate: string
  endDate?: string
  tags: string[]
}

export interface UpdateProjectDto extends Partial<CreateProjectDto> {
  progress?: number
}