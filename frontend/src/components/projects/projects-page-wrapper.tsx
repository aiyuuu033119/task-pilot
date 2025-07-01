"use client"

import { AppHeader } from "@/components/navigation/app-header"
import { ProjectHeader } from "./project-header"
import { ProjectList } from "./project-list"

export function ProjectsPageWrapper() {
  return (
    <main className="min-h-screen bg-background">
      <AppHeader 
        title="Project Management" 
        subtitle="Organize and track your projects" 
      />
      <div className="container mx-auto px-4 py-6 max-w-7xl">
        <ProjectHeader />
        <ProjectList />
      </div>
    </main>
  )
}