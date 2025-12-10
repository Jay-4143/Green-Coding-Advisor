import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '../../test/utils'
import userEvent from '@testing-library/user-event'
import apiClient from '../../api/client'
import LoginModal from '../LoginModal'

// Mock the API client module without using top-level variables inside the factory
vi.mock('../../api/client', () => {
  const mockApi = {
    get: vi.fn(),
    post: vi.fn(),
  }
  return {
    default: mockApi,
    api: mockApi,
    setTokens: vi.fn(),
  }
})

const mockedApi = apiClient as unknown as {
  get: ReturnType<typeof vi.fn>
  post: ReturnType<typeof vi.fn>
}

describe('LoginModal Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('does not render when closed', () => {
    const onClose = vi.fn()
    const onSuccess = vi.fn()
    const { container } = render(
      <LoginModal isOpen={false} onClose={onClose} onSuccess={onSuccess} />
    )
    expect(container.firstChild).toBeNull()
  })

  it('renders login form when open', () => {
    const onClose = vi.fn()
    const onSuccess = vi.fn()
    render(<LoginModal isOpen={true} onClose={onClose} onSuccess={onSuccess} />)
    
    // Check for login heading or button
    expect(screen.getByText(/login/i)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument()
  })

  it('allows user to input email', async () => {
    const user = userEvent.setup()
    const onClose = vi.fn()
    const onSuccess = vi.fn()
    render(<LoginModal isOpen={true} onClose={onClose} onSuccess={onSuccess} />)
    
    const emailInput = screen.getByPlaceholderText(/your\.email@example\.com/i)
    await user.type(emailInput, 'test@example.com')
    expect(emailInput).toHaveValue('test@example.com')
  })

  it('allows user to input password', async () => {
    const user = userEvent.setup()
    const onClose = vi.fn()
    const onSuccess = vi.fn()
    render(<LoginModal isOpen={true} onClose={onClose} onSuccess={onSuccess} />)
    
    const passwordInput = screen.getByPlaceholderText(/enter your password/i)
    await user.type(passwordInput, 'Password123!')
    expect(passwordInput).toHaveValue('Password123!')
  })
})
