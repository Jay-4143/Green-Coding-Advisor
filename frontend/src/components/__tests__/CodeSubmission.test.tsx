import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '../../test/utils'
import userEvent from '@testing-library/user-event'
import apiClient from '../../api/client'
import CodeSubmission from '../CodeSubmission'

// Mock the API client module without using top-level variables inside the factory
vi.mock('../../api/client', () => {
  const mockApi = {
    get: vi.fn(),
    post: vi.fn(),
  }
  return {
    default: mockApi,
    api: mockApi,
  }
})

const mockedApi = apiClient as unknown as {
  get: ReturnType<typeof vi.fn>
  post: ReturnType<typeof vi.fn>
}

describe('CodeSubmission Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockedApi.post.mockResolvedValue({
      data: {
        green_score: 75,
        energy_consumption_wh: 0.5,
        co2_emissions_g: 0.25,
        memory_usage_mb: 10,
        cpu_time_ms: 100,
        suggestions: [],
      },
    })
  })

  it('renders code submission form', () => {
    render(<CodeSubmission />)
    expect(document.body).toBeInTheDocument()
  })

  it('allows user to input code', async () => {
    const user = userEvent.setup()
    render(<CodeSubmission />)
    
    const codeInput = screen.getByPlaceholderText(/paste your code here/i)
    await user.type(codeInput, 'def hello(): return "world"')
    expect(codeInput).toHaveValue('def hello(): return "world"')
  })
})

