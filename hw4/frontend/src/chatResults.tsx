import { createContext, useContext, useMemo, useState } from 'react'
import type { Product } from './types'

interface ChatResults {
  /** The shopper's question that produced these matches. */
  query: string
  /** The products the agent matched, to render on the Products page. */
  matches: Product[]
}

interface ChatResultsContextValue extends ChatResults {
  active: boolean
  setResults: (query: string, matches: Product[]) => void
  clear: () => void
}

const ChatResultsContext = createContext<ChatResultsContextValue | null>(null)

export function ChatResultsProvider({ children }: { children: React.ReactNode }) {
  const [results, setResultsState] = useState<ChatResults>({ query: '', matches: [] })

  const value = useMemo<ChatResultsContextValue>(
    () => ({
      ...results,
      active: results.matches.length > 0,
      setResults: (query, matches) => setResultsState({ query, matches }),
      clear: () => setResultsState({ query: '', matches: [] }),
    }),
    [results],
  )

  return (
    <ChatResultsContext.Provider value={value}>{children}</ChatResultsContext.Provider>
  )
}

export function useChatResults(): ChatResultsContextValue {
  const context = useContext(ChatResultsContext)
  if (!context) throw new Error('useChatResults must be used within ChatResultsProvider')
  return context
}
