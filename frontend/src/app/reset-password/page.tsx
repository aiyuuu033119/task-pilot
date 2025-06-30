"use client"

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import { useAuthStore } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'

export default function ResetPasswordPage() {
  const [step, setStep] = useState<'request' | 'confirm'>('request')
  const [formData, setFormData] = useState({
    email: '',
    token: '',
    newPassword: '',
    confirmPassword: '',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [successMessage, setSuccessMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { requestPasswordReset, confirmPasswordReset, isAuthenticated, checkAuth } = useAuthStore()
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    checkAuth()
  }, [checkAuth])

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/chat')
    }
  }, [isAuthenticated, router])

  useEffect(() => {
    // Check if token is in URL params
    const token = searchParams.get('token')
    if (token) {
      setFormData(prev => ({ ...prev, token }))
      setStep('confirm')
    }
  }, [searchParams])

  const validateRequestForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.email) {
      newErrors.email = 'Email is required'
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const validateConfirmForm = () => {
    const newErrors: Record<string, string> = {}

    if (!formData.token) {
      newErrors.token = 'Reset token is required'
    }

    if (!formData.newPassword) {
      newErrors.newPassword = 'New password is required'
    } else if (formData.newPassword.length < 8) {
      newErrors.newPassword = 'Password must be at least 8 characters'
    }

    if (formData.newPassword !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleRequestSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateRequestForm()) {
      return
    }

    setIsLoading(true)
    try {
      await requestPasswordReset(formData.email)
      setSuccessMessage('Password reset instructions have been sent to your email.')
      setStep('confirm')
    } catch (error) {
      setErrors({ 
        submit: error instanceof Error ? error.message : 'Failed to send reset email' 
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleConfirmSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateConfirmForm()) {
      return
    }

    setIsLoading(true)
    try {
      await confirmPasswordReset(formData.token, formData.newPassword)
      setSuccessMessage('Password has been reset successfully. You can now sign in with your new password.')
      setTimeout(() => {
        router.push('/login')
      }, 2000)
    } catch (error) {
      setErrors({ 
        submit: error instanceof Error ? error.message : 'Failed to reset password' 
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }))
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
  }

  // If user is authenticated, show loading while redirecting
  if (isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Redirecting to chat...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {step === 'request' ? 'Reset Password' : 'Enter New Password'}
          </h1>
          <p className="text-gray-600">
            {step === 'request' 
              ? 'Enter your email to receive reset instructions'
              : 'Enter your new password below'
            }
          </p>
        </div>

        {/* Form Card */}
        <Card className="p-8 bg-white shadow-lg">
          {successMessage && (
            <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded mb-4">
              {successMessage}
            </div>
          )}

          {step === 'request' ? (
            <form onSubmit={handleRequestSubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                  Email Address
                </label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={handleInputChange('email')}
                  className={errors.email ? 'border-red-500' : ''}
                  placeholder="Enter your email address"
                  required
                />
                {errors.email && (
                  <p className="text-red-500 text-sm mt-1">{errors.email}</p>
                )}
              </div>

              <p className="text-sm text-gray-600">
                We'll send you instructions on how to reset your password.
              </p>

              {errors.submit && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {errors.submit}
                </div>
              )}

              <Button
                type="submit"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Sending...' : 'Send Reset Instructions'}
              </Button>

              <div className="text-center">
                <button
                  type="button"
                  onClick={() => setStep('confirm')}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Already have a token?
                </button>
              </div>
            </form>
          ) : (
            <form onSubmit={handleConfirmSubmit} className="space-y-4">
              <div>
                <label htmlFor="token" className="block text-sm font-medium text-gray-700 mb-1">
                  Reset Token
                </label>
                <Input
                  id="token"
                  type="text"
                  value={formData.token}
                  onChange={handleInputChange('token')}
                  className={errors.token ? 'border-red-500' : ''}
                  placeholder="Enter the reset token from your email"
                  required
                />
                {errors.token && (
                  <p className="text-red-500 text-sm mt-1">{errors.token}</p>
                )}
              </div>

              <div>
                <label htmlFor="newPassword" className="block text-sm font-medium text-gray-700 mb-1">
                  New Password
                </label>
                <Input
                  id="newPassword"
                  type="password"
                  value={formData.newPassword}
                  onChange={handleInputChange('newPassword')}
                  className={errors.newPassword ? 'border-red-500' : ''}
                  placeholder="Enter your new password"
                  required
                />
                {errors.newPassword && (
                  <p className="text-red-500 text-sm mt-1">{errors.newPassword}</p>
                )}
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                  Confirm New Password
                </label>
                <Input
                  id="confirmPassword"
                  type="password"
                  value={formData.confirmPassword}
                  onChange={handleInputChange('confirmPassword')}
                  className={errors.confirmPassword ? 'border-red-500' : ''}
                  placeholder="Confirm your new password"
                  required
                />
                {errors.confirmPassword && (
                  <p className="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>
                )}
              </div>

              {errors.submit && (
                <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                  {errors.submit}
                </div>
              )}

              <Button
                type="submit"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Resetting...' : 'Reset Password'}
              </Button>

              <div className="text-center">
                <button
                  type="button"
                  onClick={() => setStep('request')}
                  className="text-sm text-blue-600 hover:text-blue-800"
                >
                  Need a new token?
                </button>
              </div>
            </form>
          )}

          <div className="mt-6 text-center">
            <Link href="/login" className="text-sm text-blue-600 hover:text-blue-800">
              Back to Sign In
            </Link>
          </div>
        </Card>

        {/* Footer */}
        <div className="text-center mt-6 text-sm text-gray-500">
          <p>Having trouble? Contact support for assistance</p>
        </div>
      </div>
    </div>
  )
}