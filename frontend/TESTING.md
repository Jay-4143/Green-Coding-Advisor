# Frontend Testing Guide

This project uses **Vitest** (Jest-compatible) with **React Testing Library** for frontend testing.

## Setup

The testing framework is already configured. Dependencies are installed in `package.json`.

## Running Tests

```bash
# Run all tests once
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with UI
npm test:ui

# Run tests with coverage report
npm test:coverage
```

## Test Structure

Tests are located in `src/components/__tests__/` directory, following the naming convention:
- `ComponentName.test.tsx` or `ComponentName.spec.tsx`

## Writing Tests

### Basic Component Test

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '../../test/utils'
import MyComponent from '../MyComponent'

describe('MyComponent', () => {
  it('renders without crashing', () => {
    render(<MyComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })
})
```

### Testing User Interactions

```typescript
import userEvent from '@testing-library/user-event'

it('handles user input', async () => {
  const user = userEvent.setup()
  render(<MyComponent />)
  
  const input = screen.getByPlaceholderText('Enter text')
  await user.type(input, 'Hello World')
  
  expect(input).toHaveValue('Hello World')
})
```

### Mocking API Calls

```typescript
import { vi } from 'vitest'
import apiClient from '../../api/client'

vi.mock('../../api/client', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}))

it('fetches data on mount', async () => {
  apiClient.get.mockResolvedValue({ data: { result: 'success' } })
  render(<MyComponent />)
  
  await waitFor(() => {
    expect(apiClient.get).toHaveBeenCalled()
  })
})
```

## Test Utilities

The `src/test/utils.tsx` file provides:
- Custom `render` function with Router provider
- Re-exports from `@testing-library/react`

## Coverage

Coverage reports are generated in `coverage/` directory when running `npm test:coverage`.

## Best Practices

1. **Test user behavior, not implementation details**
2. **Use semantic queries** (`getByRole`, `getByLabelText`) over `getByTestId`
3. **Mock external dependencies** (API calls, browser APIs)
4. **Keep tests simple and focused** - one assertion per test when possible
5. **Use descriptive test names** that explain what is being tested

## Common Patterns

### Testing Forms
```typescript
it('submits form with valid data', async () => {
  const user = userEvent.setup()
  const onSubmit = vi.fn()
  
  render(<Form onSubmit={onSubmit} />)
  
  await user.type(screen.getByLabelText('Email'), 'test@example.com')
  await user.click(screen.getByRole('button', { name: /submit/i }))
  
  expect(onSubmit).toHaveBeenCalledWith({ email: 'test@example.com' })
})
```

### Testing Async Operations
```typescript
it('displays loading state', async () => {
  render(<AsyncComponent />)
  
  expect(screen.getByText('Loading...')).toBeInTheDocument()
  
  await waitFor(() => {
    expect(screen.getByText('Loaded!')).toBeInTheDocument()
  })
})
```

## Troubleshooting

- **Tests not finding elements**: Use `screen.debug()` to see the rendered HTML
- **Async issues**: Use `waitFor` or `findBy*` queries for async elements
- **Router errors**: Ensure components using `useNavigate` or `Link` are wrapped in Router

