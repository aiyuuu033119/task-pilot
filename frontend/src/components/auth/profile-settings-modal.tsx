"use client"

import { useState, useEffect } from 'react'
import { useAuthStore, User } from '@/lib/auth'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'

interface ProfileSettingsModalProps {
  isOpen: boolean
  onClose: () => void
}

export function ProfileSettingsModal({ isOpen, onClose }: ProfileSettingsModalProps) {
  const { user, updateProfile, isLoading } = useAuthStore()
  const [formData, setFormData] = useState({
    full_name: '',
    display_name: '',
    job_title: '',
    timezone: 'UTC',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [successMessage, setSuccessMessage] = useState('')

  useEffect(() => {
    if (user) {
      setFormData({
        full_name: user.full_name || '',
        display_name: user.display_name || '',
        job_title: user.job_title || '',
        timezone: user.timezone || 'UTC',
      })
    }
  }, [user])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!user) return

    try {
      // Only send fields that have changed
      const updates: Partial<User> = {}
      
      if (formData.full_name !== (user.full_name || '')) {
        updates.full_name = formData.full_name || null
      }
      if (formData.display_name !== (user.display_name || '')) {
        updates.display_name = formData.display_name || null
      }
      if (formData.job_title !== (user.job_title || '')) {
        updates.job_title = formData.job_title || null
      }
      if (formData.timezone !== user.timezone) {
        updates.timezone = formData.timezone
      }

      if (Object.keys(updates).length === 0) {
        setSuccessMessage('No changes to save')
        return
      }

      await updateProfile(updates)
      setSuccessMessage('Profile updated successfully!')
      setErrors({})
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(''), 3000)
    } catch (error) {
      setErrors({ 
        submit: error instanceof Error ? error.message : 'Failed to update profile' 
      })
    }
  }

  const handleInputChange = (field: string) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData(prev => ({ ...prev, [field]: e.target.value }))
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }))
    }
    if (successMessage) {
      setSuccessMessage('')
    }
  }

  const handleClose = () => {
    setErrors({})
    setSuccessMessage('')
    onClose()
  }

  if (!isOpen || !user) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <Card className="w-full max-w-md p-6 bg-white max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Profile Settings</h2>
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

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email (read-only) */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <Input
              type="email"
              value={user.email}
              disabled
              className="bg-gray-50"
            />
            <p className="text-xs text-gray-500 mt-1">Email cannot be changed</p>
          </div>

          {/* Full Name */}
          <div>
            <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-1">
              Full Name
            </label>
            <Input
              id="full_name"
              type="text"
              value={formData.full_name}
              onChange={handleInputChange('full_name')}
              placeholder="Enter your full name"
            />
          </div>

          {/* Display Name */}
          <div>
            <label htmlFor="display_name" className="block text-sm font-medium text-gray-700 mb-1">
              Display Name
            </label>
            <Input
              id="display_name"
              type="text"
              value={formData.display_name}
              onChange={handleInputChange('display_name')}
              placeholder="How should others see your name?"
            />
          </div>

          {/* Job Title */}
          <div>
            <label htmlFor="job_title" className="block text-sm font-medium text-gray-700 mb-1">
              Job Title
            </label>
            <Input
              id="job_title"
              type="text"
              value={formData.job_title}
              onChange={handleInputChange('job_title')}
              placeholder="Enter your job title"
            />
          </div>

          {/* Timezone */}
          <div>
            <label htmlFor="timezone" className="block text-sm font-medium text-gray-700 mb-1">
              Timezone
            </label>
            <select
              id="timezone"
              value={formData.timezone}
              onChange={handleInputChange('timezone')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="UTC">UTC</option>
              <option value="America/New_York">Eastern Time</option>
              <option value="America/Chicago">Central Time</option>
              <option value="America/Denver">Mountain Time</option>
              <option value="America/Los_Angeles">Pacific Time</option>
              <option value="Europe/London">London</option>
              <option value="Europe/Paris">Paris</option>
              <option value="Europe/Berlin">Berlin</option>
              <option value="Asia/Tokyo">Tokyo</option>
              <option value="Asia/Shanghai">Shanghai</option>
              <option value="Asia/Kolkata">India</option>
              <option value="Australia/Sydney">Sydney</option>
            </select>
          </div>

          {/* Account Status */}
          <div className="bg-gray-50 p-3 rounded">
            <div className="text-sm">
              <div className="flex justify-between items-center mb-1">
                <span className="text-gray-600">Account Status:</span>
                <span className={user.is_verified ? 'text-green-600' : 'text-yellow-600'}>
                  {user.is_verified ? 'Verified' : 'Unverified'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Member Since:</span>
                <span className="text-gray-800">
                  {new Date(user.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>

          {errors.submit && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {errors.submit}
            </div>
          )}

          <div className="flex gap-3">
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              className="flex-1"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1"
              disabled={isLoading}
            >
              {isLoading ? 'Updating...' : 'Save Changes'}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  )
}