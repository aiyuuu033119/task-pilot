"use client"

import { useState, useEffect } from 'react'
import { useAuthStore } from '@/lib/auth'
import { LoginModal } from './login-modal'
import { RegistrationModal } from './registration-modal'
import { PasswordResetModal } from './password-reset-modal'
import { ProfileSettingsModal } from './profile-settings-modal'
import { Button } from '@/components/ui/button'

type AuthModalType = 'login' | 'register' | 'password-reset' | 'profile' | null

interface AuthManagerProps {
  showAuthButtons?: boolean
}

export function AuthManager({ showAuthButtons = true }: AuthManagerProps) {
  const [activeModal, setActiveModal] = useState<AuthModalType>(null)
  const { isAuthenticated, user, logout, checkAuth } = useAuthStore()

  useEffect(() => {
    // Check authentication status on mount
    checkAuth()
  }, [checkAuth])

  const handleCloseModal = () => {
    setActiveModal(null)
  }

  const handleSwitchModal = (modalType: AuthModalType) => {
    setActiveModal(modalType)
  }

  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  if (!showAuthButtons) {
    return (
      <>
        <LoginModal
          isOpen={activeModal === 'login'}
          onClose={handleCloseModal}
          onSwitchToRegister={() => handleSwitchModal('register')}
          onSwitchToPasswordReset={() => handleSwitchModal('password-reset')}
        />
        <RegistrationModal
          isOpen={activeModal === 'register'}
          onClose={handleCloseModal}
          onSwitchToLogin={() => handleSwitchModal('login')}
        />
        <PasswordResetModal
          isOpen={activeModal === 'password-reset'}
          onClose={handleCloseModal}
          onSwitchToLogin={() => handleSwitchModal('login')}
        />
        <ProfileSettingsModal
          isOpen={activeModal === 'profile'}
          onClose={handleCloseModal}
        />
      </>
    )
  }

  if (isAuthenticated && user) {
    return (
      <>
        <div className="flex items-center gap-4">
          <div className="text-sm">
            <span className="text-gray-600">Welcome, </span>
            <button
              onClick={() => setActiveModal('profile')}
              className="font-medium text-blue-600 hover:text-blue-800"
            >
              {user.display_name || user.full_name || user.email}
            </button>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={handleLogout}
          >
            Sign Out
          </Button>
        </div>

        <ProfileSettingsModal
          isOpen={activeModal === 'profile'}
          onClose={handleCloseModal}
        />
      </>
    )
  }

  return (
    <>
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveModal('login')}
        >
          Sign In
        </Button>
        <Button
          size="sm"
          onClick={() => setActiveModal('register')}
        >
          Sign Up
        </Button>
      </div>

      <LoginModal
        isOpen={activeModal === 'login'}
        onClose={handleCloseModal}
        onSwitchToRegister={() => handleSwitchModal('register')}
        onSwitchToPasswordReset={() => handleSwitchModal('password-reset')}
      />
      <RegistrationModal
        isOpen={activeModal === 'register'}
        onClose={handleCloseModal}
        onSwitchToLogin={() => handleSwitchModal('login')}
      />
      <PasswordResetModal
        isOpen={activeModal === 'password-reset'}
        onClose={handleCloseModal}
        onSwitchToLogin={() => handleSwitchModal('login')}
      />
      <ProfileSettingsModal
        isOpen={activeModal === 'profile'}
        onClose={handleCloseModal}
      />
    </>
  )
}