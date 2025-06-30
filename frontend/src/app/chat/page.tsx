"use client"

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/auth'
import { ChatContainer } from '@/components/chat/chat-container'
import { AuthManager } from '@/components/auth/auth-manager'

export default function ChatPage() {
  const { isAuthenticated, checkAuth, isLoading } = useAuthStore()
  const router = useRouter()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/login')
    }
  }, [isAuthenticated, isLoading, router])

  // Show loading while checking authentication
  if (isLoading || !isAuthenticated) {
    return (
      <div className="h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading chat...</p>
        </div>
      </div>
    )
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
          <AuthManager />
        </div>
      </header>

      {/* Chat Interface */}
      <div className="flex-1">
        <ChatContainer />
      </div>
    </main>
  )
}