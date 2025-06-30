"use client"

import { useState } from 'react'
import { useAuthStore } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'

interface PasswordResetModalProps {
  isOpen: boolean
  onClose: () => void
  onSwitchToLogin: () => void
}

export function PasswordResetModal({ isOpen, onClose, onSwitchToLogin }: PasswordResetModalProps) {
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
  const { requestPasswordReset, confirmPasswordReset } = useAuthStore()

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
        onSwitchToLogin()
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

  const handleClose = () => {
    setStep('request')
    setFormData({ email: '', token: '', newPassword: '', confirmPassword: '' })
    setErrors({})
    setSuccessMessage('')
    onClose()
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <Card className="w-full max-w-md p-6 bg-white">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">
            {step === 'request' ? 'Reset Password' : 'Enter New Password'}
          </h2>
          <button
            onClick={handleClose}
            className="text-gray-500 hover:text-gray-700 text-xl"
          >
            ×
          </button>
        </div>

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
          </form>
        )}

        <div className="mt-6 text-center">
          <button
            onClick={onSwitchToLogin}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            Back to Sign In
          </button>
        </div>
      </Card>
    </div>
  )
}