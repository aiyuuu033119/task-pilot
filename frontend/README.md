# Pydantic AI Chat Frontend

A modern chat interface built with Next.js, React, Tailwind CSS, shadcn/ui, and Zustand.

## Tech Stack

- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Reusable component library
- **Zustand** - State management
- **React Markdown** - Markdown rendering
- **Lucide Icons** - Icon library

## Features

- 🚀 Real-time chat with WebSocket connection
- 💅 Beautiful UI with shadcn/ui components
- 🎨 Dark mode support
- 📱 Responsive design
- 🔄 Auto-reconnect on connection loss
- 📝 Markdown support for messages
- 💬 Conversation history
- 🔌 Connection status indicator

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend server running on port 8000

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

The app will be available at http://localhost:3000

### Building for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js app directory
│   │   ├── globals.css   # Global styles
│   │   ├── layout.tsx    # Root layout
│   │   └── page.tsx      # Home page
│   ├── components/       # React components
│   │   ├── chat/        # Chat-specific components
│   │   └── ui/          # shadcn/ui components
│   └── lib/             # Utilities and hooks
│       ├── store.ts     # Zustand store
│       ├── utils.ts     # Utility functions
│       └── websocket.ts # WebSocket hook
├── public/              # Static assets
└── package.json         # Dependencies
```

## Configuration

### Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Customization

- **Theme**: Edit `src/app/globals.css` for color scheme
- **Components**: Modify files in `src/components/ui/`
- **Layout**: Update `src/app/layout.tsx`

## Development

### Adding New Components

Use shadcn/ui CLI to add components:

```bash
npx shadcn-ui@latest add [component-name]
```

### State Management

The Zustand store (`src/lib/store.ts`) manages:
- Conversations
- Messages
- Connection status
- Loading states
- Error handling

### WebSocket Integration

The WebSocket hook (`src/lib/websocket.ts`) handles:
- Connection management
- Auto-reconnection
- Message sending/receiving
- Error handling

## Deployment

### Static Export

```bash
npm run build
```

Serve the `out` directory with any static hosting service.

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Troubleshooting

### WebSocket Connection Issues
- Ensure backend is running on port 8000
- Check CORS settings on backend
- Verify WebSocket URL in environment variables

### Build Errors
- Clear `.next` directory: `rm -rf .next`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check TypeScript errors: `npm run type-check`

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature/my-feature`
5. Submit pull request