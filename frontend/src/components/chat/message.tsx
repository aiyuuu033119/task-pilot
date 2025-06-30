import React from 'react'
import { cn } from '@/lib/utils'
import { Card } from '@/components/ui/card'
import ReactMarkdown from 'react-markdown'
import { User, Bot } from 'lucide-react'

interface MessageProps {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

export function Message({ role, content, timestamp }: MessageProps) {
  const isUser = role === 'user'

  return (
    <div className={cn('flex gap-3 mb-4', isUser ? 'justify-end' : 'justify-start')}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
          <Bot className="w-5 h-5 text-primary-foreground" />
        </div>
      )}
      
      <Card className={cn(
        'max-w-[80%] px-4 py-2',
        isUser ? 'bg-primary text-primary-foreground' : 'bg-muted'
      )}>
        <div className="prose prose-sm dark:prose-invert max-w-none">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
        <div className={cn(
          'text-xs mt-1',
          isUser ? 'text-primary-foreground/70' : 'text-muted-foreground'
        )}>
          {timestamp.toLocaleTimeString()}
        </div>
      </Card>
      
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 rounded-full bg-secondary flex items-center justify-center">
          <User className="w-5 h-5 text-secondary-foreground" />
        </div>
      )}
    </div>
  )
}