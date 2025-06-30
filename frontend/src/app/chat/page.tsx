import { auth } from "@clerk/nextjs/server"
import { redirect } from "next/navigation"
import { UserButton } from "@clerk/nextjs"
import { ChatContainer } from '@/components/chat/chat-container'

export default async function ChatPage() {
  const { userId } = await auth()
  
  // Double-check authentication on the server side
  if (!userId) {
    redirect('/')
  }

  return (
    <main className="h-screen bg-background flex flex-col">
      {/* Header with Authentication */}
      <header className="bg-white border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-gray-900">AI Chat Assistant</h1>
            <p className="text-sm text-gray-600">Powered by Pydantic AI & MCP</p>
          </div>
          <UserButton afterSignOutUrl="/" />
        </div>
      </header>

      {/* Chat Interface */}
      <div className="flex-1">
        <ChatContainer />
      </div>
    </main>
  )
}