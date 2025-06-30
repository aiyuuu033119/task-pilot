import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import { ChatPageWrapper } from '@/components/chat/chat-page-wrapper'

export default async function ChatPage() {
  const { userId } = await auth()
  
  // Double-check authentication on the server side
  if (!userId) {
    redirect('/')
  }

  return <ChatPageWrapper />
}