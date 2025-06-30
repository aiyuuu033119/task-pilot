"use client"

import { SignInButton, SignUpButton, SignedIn, SignedOut } from "@clerk/nextjs"
import { useRouter } from "next/navigation"
import { useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function Home() {
  const router = useRouter()

  useEffect(() => {
    // If already signed in, redirect to chat
    const checkAuth = () => {
      const signedIn = document.querySelector('[data-signed-in="true"]')
      if (signedIn) {
        router.push('/chat')
      }
    }
    checkAuth()
  }, [router])

  return (
    <>
      <SignedIn>
        <div data-signed-in="true" className="hidden" />
        {/* This will trigger the redirect */}
      </SignedIn>
      
      <SignedOut>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
          <div className="max-w-md w-full">
            {/* Logo and Title */}
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Welcome to AI Chat</h1>
              <p className="text-gray-600">Sign in to start chatting with our AI assistant</p>
            </div>

            {/* Login Card */}
            <Card className="p-8 bg-white shadow-lg">
              <div className="space-y-4">
                <div className="text-center mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">Get Started</h2>
                  <p className="text-sm text-gray-600">Choose how you'd like to continue</p>
                </div>

                <SignInButton mode="modal" forceRedirectUrl="/chat">
                  <Button className="w-full" size="lg">
                    Sign In
                  </Button>
                </SignInButton>

                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <span className="w-full border-t" />
                  </div>
                  <div className="relative flex justify-center text-xs uppercase">
                    <span className="bg-white px-2 text-gray-500">Or</span>
                  </div>
                </div>

                <SignUpButton mode="modal" forceRedirectUrl="/chat">
                  <Button variant="outline" className="w-full" size="lg">
                    Create Account
                  </Button>
                </SignUpButton>
              </div>

              <div className="mt-6 text-center text-sm text-gray-500">
                <p>By continuing, you agree to our Terms of Service</p>
              </div>
            </Card>

            {/* Features */}
            <div className="mt-8 grid grid-cols-3 gap-4 text-center">
              <div>
                <div className="text-blue-600 mb-2">
                  <svg className="w-6 h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <p className="text-sm text-gray-600">Fast Responses</p>
              </div>
              <div>
                <div className="text-blue-600 mb-2">
                  <svg className="w-6 h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <p className="text-sm text-gray-600">Secure & Private</p>
              </div>
              <div>
                <div className="text-blue-600 mb-2">
                  <svg className="w-6 h-6 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <p className="text-sm text-gray-600">AI-Powered</p>
              </div>
            </div>
          </div>
        </div>
      </SignedOut>
    </>
  )
}