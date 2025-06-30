import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import { ProjectsPageWrapper } from "@/components/projects/projects-page-wrapper"

export default async function ProjectsPage() {
  const { userId } = await auth()
  
  if (!userId) {
    redirect('/')
  }

  return <ProjectsPageWrapper />
}