import { useEffect, useRef, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { fetchChatHistory, sendChat } from '../api'
import { useAuth } from '../auth'
import { useChatResults } from '../chatResults'
import { formatPrice, type Product } from '../types'

/** Read the product id from a /products/:id detail URL, else null. */
function currentProductIdFrom(pathname: string): string | null {
  const parts = pathname.split('/').filter(Boolean)
  return parts[0] === 'products' && parts[1] ? parts[1] : null
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  /** Products the assistant chose to show alongside its reply. */
  products?: Product[]
}

const GREETING: ChatMessage = {
  role: 'assistant',
  content:
    "Hi! I'm the Campus Customs shop assistant. Ask me about sizes, colors, prices, or what we have in stock.",
}

export default function ChatWidget() {
  const { user } = useAuth()
  const { setResults } = useChatResults()
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<ChatMessage[]>([GREETING])
  const [draft, setDraft] = useState('')
  const [pending, setPending] = useState(false)
  const threadRef = useRef<HTMLDivElement>(null)

  // Reload the shopper's saved conversation when they sign in; reset on sign-out.
  useEffect(() => {
    if (!user) {
      setMessages([GREETING])
      return
    }
    let cancelled = false
    fetchChatHistory(user.id)
      .then((items) => {
        if (cancelled) return
        const restored: ChatMessage[] = items.map((item) => ({
          role: item.role,
          content: item.content,
          products: item.products,
        }))
        setMessages([GREETING, ...restored])
      })
      .catch(() => {
        /* keep the greeting if history can't be loaded */
      })
    return () => {
      cancelled = true
    }
  }, [user])

  // Keep the newest message in view as the thread grows.
  useEffect(() => {
    threadRef.current?.scrollTo({ top: threadRef.current.scrollHeight })
  }, [messages, pending, open])

  async function sendMessage(text: string) {
    const trimmed = text.trim()
    if (!trimmed || pending) return

    // Send the conversation so far (excluding the opening greeting) as context.
    const history = messages
      .filter((m) => m !== GREETING)
      .map((m) => ({ role: m.role, content: m.content }))

    setMessages((prev) => [...prev, { role: 'user', content: trimmed }])
    setDraft('')
    setPending(true)
    try {
      const reply = await sendChat(
        trimmed,
        history,
        user?.id ?? null,
        currentProductIdFrom(location.pathname),
      )
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: reply.reply, products: reply.products },
      ])
      // Push the matches onto the Products page and take the shopper there to see them.
      if (reply.products.length > 0) {
        setResults(trimmed, reply.products)
        navigate('/products')
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: 'Something went wrong reaching the shop. Try again?' },
      ])
    } finally {
      setPending(false)
    }
  }

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    void sendMessage(draft)
  }

  // Shown only before the shopper has said anything, to make a first question one click away.
  const suggestions = ['What hoodies do you have?', 'Cheapest fleece', 'Show me crewnecks']
  const conversationStarted = messages.some((m) => m.role === 'user')

  if (!open) {
    return (
      <button type="button" className="chat-launcher" onClick={() => setOpen(true)}>
        Ask the shop
      </button>
    )
  }

  return (
    <aside className="chat-panel" aria-label="Campus Customs shop assistant">
      <header className="chat-header">
        <div>
          <strong>Shop Assistant</strong>
          <small>Campus Customs</small>
        </div>
        <button
          type="button"
          className="chat-close"
          onClick={() => setOpen(false)}
          aria-label="Close chat"
        >
          &times;
        </button>
      </header>

      <div className="chat-thread" ref={threadRef}>
        {messages.map((message, index) => (
          <div key={index} className="turn">
            <div className={`bubble bubble-${message.role}`}>{message.content}</div>
            {message.products && message.products.length > 0 && (
              <div className="chat-products">
                {message.products.map((product) => (
                  <Link
                    key={product.product_id}
                    to={`/products/${product.product_id}`}
                    className="chat-product"
                    onClick={() => setOpen(false)}
                  >
                    <img src={product.image_url} alt={product.name} loading="lazy" />
                    <span className="chat-product-name">{product.name}</span>
                    <span className="chat-product-price">{formatPrice(product.price)}</span>
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
        {pending && (
          <div className="bubble bubble-assistant typing" aria-label="Shop assistant is typing">
            <span className="dot" />
            <span className="dot" />
            <span className="dot" />
          </div>
        )}
      </div>

      {!conversationStarted && !pending && (
        <div className="chat-suggestions">
          {suggestions.map((text) => (
            <button
              key={text}
              type="button"
              className="chat-suggestion"
              onClick={() => void sendMessage(text)}
            >
              {text}
            </button>
          ))}
        </div>
      )}

      <form className="chat-input" onSubmit={handleSubmit}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Do you have this in a medium?"
          aria-label="Message the shop assistant"
        />
        <button type="submit" disabled={pending || !draft.trim()}>
          Send
        </button>
      </form>
    </aside>
  )
}
