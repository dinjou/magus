import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../App'

describe('App', () => {
  it('renders without crashing', async () => {
    const { container } = render(<App />)
    // App should render without throwing
    expect(container).toBeTruthy()
    // Should render login page by default (redirects from dashboard)
    expect(await screen.findByText(/sign in to your account/i)).toBeTruthy()
  })
})

