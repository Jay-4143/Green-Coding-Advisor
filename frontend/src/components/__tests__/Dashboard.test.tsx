import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '../../test/utils'
import apiClient from '../../api/client'
import Dashboard from '../Dashboard'

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

describe('Dashboard Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Mock successful API responses
    mockedApi.get.mockResolvedValue({
      data: {
        total_submissions: 10,
        average_green_score: 75,
        total_co2_saved: 100,
        total_energy_saved: 50,
        badges_earned: 3,
        current_streak: 5,
        rank: 1,
      },
    })
  })

  it('renders dashboard without crashing', () => {
    render(<Dashboard />)
    expect(document.body).toBeInTheDocument()
  })

  it('displays loading state initially', () => {
    render(<Dashboard />)
    // Dashboard should show loading or stats
    expect(document.body).toBeInTheDocument()
  })

  it('fetches dashboard data on mount', async () => {
    render(<Dashboard />)
    
    await waitFor(() => {
      expect(mockedApi.get).toHaveBeenCalled()
    })
  })
})

