'use client'

import React, { useEffect, useRef } from 'react'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Card } from '@/components/ui/card'
import { Message } from './message'
import { MessageInput } from './message-input'
import { ConnectionStatus } from './connection-status'
import { useChatStore } from '@/lib/store'
import { useWebSocket } from '@/lib/websocket'
import { v4 as uuidv4 } from 'uuid'
import { Loader2 } from 'lucide-react'

export function ChatContainer() {
  const scrollRef = useRef<HTMLDivElement>(null)
  const { sendMessage, isConnected } = useWebSocket('ws://localhost:8000/ws')
  const {
    conversations,
    activeConversationId,
    isLoading,
    error,
    addMessage,
    addConversation,
    setActiveConversation,
  } = useChatStore()

  const activeConversation = conversations.find(c => c.id === activeConversationId)

  // Create initial conversation if none exists
  useEffect(() => {
    if (conversations.length === 0) {
      const newConversation = {
        id: uuidv4(),
        title: 'New Chat',
        messages: [],
        createdAt: new Date(),
        updatedAt: new Date(),
      }
      addConversation(newConversation)
      setActiveConversation(newConversation.id)
    } else if (!activeConversationId && conversations.length > 0) {
      // Set first conversation as active if none is selected
      setActiveConversation(conversations[0].id)
    }
  }, [conversations, activeConversationId, addConversation, setActiveConversation])

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [activeConversation?.messages])

  const handleSendMessage = (content: string) => {
    if (!activeConversationId) {
      console.warn('No active conversation to send message to')
      return
    }

    // Add user message to store
    const userMessage = {
      id: uuidv4(),
      role: 'user' as const,
      content,
      timestamp: new Date(),
    }
    addMessage(activeConversationId, userMessage)

    // Send via WebSocket
    sendMessage(content)
  }

  return (
    <Card className="flex flex-col h-screen max-h-screen">
      <div className="flex items-center justify-between p-4 border-b">
        <h1 className="text-xl font-semibold">AI Chat</h1>
        <ConnectionStatus isConnected={isConnected} />
      </div>

      <ScrollArea className="flex-1 p-4" ref={scrollRef}>
        {!activeConversation || activeConversation.messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            <p>Start a conversation by typing a message below.</p>
          </div>
        ) : (
          <div className="space-y-4">
            {activeConversation.messages.map((message) => (
              <Message
                key={message.id}
                role={message.role}
                content={message.content}
                timestamp={message.timestamp}
              />
            ))}
            {isLoading && (
              <div className="flex gap-3 mb-4">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                  <Loader2 className="w-5 h-5 text-primary-foreground animate-spin" />
                </div>
                <Card className="px-4 py-2 bg-muted">
                  <p className="text-sm text-muted-foreground">Thinking...</p>
                </Card>
              </div>
            )}
          </div>
        )}
        
        {error && (
          <div className="mt-4 p-4 bg-destructive/10 text-destructive rounded-lg">
            <p className="text-sm">{error}</p>
          </div>
        )}
      </ScrollArea>

      <MessageInput
        onSend={handleSendMessage}
        disabled={!isConnected || !activeConversationId}
        isLoading={isLoading}
      />
    </Card>
  )
}