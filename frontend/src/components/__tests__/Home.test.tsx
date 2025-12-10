import { describe, it, expect } from 'vitest'
import { render, screen } from '../../test/utils'
import Home from '../Home'

describe('Home Component', () => {
  it('renders the main heading', () => {
    render(<Home />)
    const heading = screen.getByRole('heading', { level: 1 })
    expect(heading).toHaveTextContent('Green Coding Advisor')
  })

  it('renders the tagline', () => {
    render(<Home />)
    expect(screen.getByText(/AI-Enhanced Platform for Sustainable Coding Practices/i)).toBeInTheDocument()
  })

  it('renders Get Started link', () => {
    render(<Home />)
    const getStartedLink = screen.getByRole('link', { name: /get started/i })
    expect(getStartedLink).toBeInTheDocument()
    expect(getStartedLink).toHaveAttribute('href', '/submit')
  })

  it('renders Learn More link', () => {
    render(<Home />)
    const learnMoreLink = screen.getByRole('link', { name: /learn more/i })
    expect(learnMoreLink).toBeInTheDocument()
    expect(learnMoreLink).toHaveAttribute('href', '/about')
  })

  it('renders features section heading', () => {
    render(<Home />)
    expect(screen.getByRole('heading', { name: /Why Choose Green Coding Advisor/i })).toBeInTheDocument()
  })
})
