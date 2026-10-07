import type { AuthUser, Product } from './types'

async function get<T>(path: string): Promise<T> {
  const response = await fetch(path)
  if (!response.ok) {
    throw new Error(`Request failed (${response.status})`)
  }
  return (await response.json()) as T
}

/** POST JSON and surface the backend's error `detail` as the thrown message. */
async function post<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    const detail = data?.detail
    const message =
      typeof detail === 'string' ? detail : 'Something went wrong. Please try again.'
    throw new Error(message)
  }
  return data as T
}

export const fetchProducts = () => get<Product[]>('/api/products')

export const fetchProduct = (productId: string) =>
  get<Product>(`/api/products/${encodeURIComponent(productId)}`)

export const fetchCategories = () => get<string[]>('/api/categories')

export interface SignupInput {
  first_name: string
  last_name: string
  email: string
  password: string
}

export const signup = (input: SignupInput) => post<AuthUser>('/api/signup', input)

export const login = (email: string, password: string) =>
  post<AuthUser>('/api/login', { email, password })

export interface ChatTurnInput {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatResponse {
  reply: string
  products: Product[]
}

export const sendChat = (
  message: string,
  history: ChatTurnInput[],
  userId: number | null,
  currentProductId: string | null,
) =>
  post<ChatResponse>('/api/chat', {
    message,
    history,
    user_id: userId,
    current_product_id: currentProductId,
  })

export interface ChatHistoryItem {
  role: 'user' | 'assistant'
  content: string
  products: Product[]
}

export const fetchChatHistory = (userId: number) =>
  get<ChatHistoryItem[]>(`/api/chat/history?user_id=${userId}`)
