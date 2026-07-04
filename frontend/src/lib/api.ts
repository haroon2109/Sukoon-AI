import Cookies from 'js-cookie'

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://sukoon-backend-62218171814.us-central1.run.app'

interface FetchOptions extends RequestInit {
  headers?: Record<string, string>
}

let isRedirectingToLogin = false;

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

  // Format endpoint to ensure correct relative path routing and prevent nested route 404s
  let url = endpoint;
  if (endpoint.startsWith('http://') || endpoint.startsWith('https://')) {
    url = endpoint;
  } else {
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    if (cleanEndpoint.startsWith('/api/')) {
      url = cleanEndpoint;
    } else {
      url = `${API_BASE_URL}${cleanEndpoint}`;
    }
  }

  const response = await fetch(url, {
    ...options,
    headers,
  })

  if (response.status === 401) {
    if (!isRedirectingToLogin) {
      isRedirectingToLogin = true;
      // Token expired or invalid
      Cookies.remove('sukoon_token')
      
      // Only redirect if we are in the browser
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
    } else {
      // Gracefully prevent duplicate redirect loops and layout flickering
      return new Response(JSON.stringify({ error: "Session expired. Redirecting..." }), {
        status: 401,
        headers: { "Content-Type": "application/json" }
      });
    }
  }

  return response
}
