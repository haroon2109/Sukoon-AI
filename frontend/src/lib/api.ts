import Cookies from 'js-cookie'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

interface FetchOptions extends RequestInit {
  headers?: Record<string, string>
}

export const fetchWithAuth = async (endpoint: string, options: FetchOptions = {}) => {
  const token = Cookies.get('sukoon_token')

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  }

  // If body is FormData, we shouldn't set Content-Type manually so the browser boundary is added
  if (options.body instanceof FormData) {
    delete (headers as any)['Content-Type']
  }

  // Format endpoint to ensure it doesn't duplicate the host if passed as a relative path
  let url = endpoint
  if (endpoint.startsWith('/api/') && !endpoint.includes('http')) {
    // If it's a relative next.js API route that proxies to backend (like rewrites in next.config)
    // we just use the relative endpoint
    url = endpoint
  } else if (endpoint.startsWith('/') && !endpoint.startsWith('/api')) {
    // If it's a direct backend call
    url = `${API_BASE_URL}${endpoint}`
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  if (response.status === 401) {
    // Token expired or invalid
    Cookies.remove('sukoon_token')
    
    // Only redirect if we are in the browser
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  return response
}
