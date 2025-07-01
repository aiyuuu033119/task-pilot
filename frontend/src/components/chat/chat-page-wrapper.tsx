"use client"

import { AppHeader } from "@/components/navigation/app-header"
import { ChatContainer } from "@/components/chat/chat-container"

export function ChatPageWrapper() {
  return (
    <main className="h-screen bg-background flex flex-col">
      <AppHeader 
        title="AI Chat Assistant" 
        subtitle="Powered by Pydantic AI & MCP" 
      />
      <div className="flex-1">
        <ChatContainer />
      </div>
    </main>
  )
}