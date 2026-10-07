import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import type { Product } from './types'

export interface CartItem {
  product_id: string
  name: string
  price: number
  image_url: string
  size: string
  quantity: number
}

interface CartContextValue {
  items: CartItem[]
  count: number
  subtotal: number
  addItem: (product: Product, size: string) => void
  removeItem: (productId: string, size: string) => void
  clear: () => void
}

const STORAGE_KEY = 'campus-customs-cart'

const CartContext = createContext<CartContextValue | null>(null)

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartItem[]>(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored ? (JSON.parse(stored) as CartItem[]) : []
  })

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items))
  }, [items])

  const value = useMemo<CartContextValue>(() => {
    return {
      items,
      count: items.reduce((sum, i) => sum + i.quantity, 0),
      subtotal: items.reduce((sum, i) => sum + i.quantity * i.price, 0),
      addItem: (product, size) =>
        setItems((prev) => {
          // Same product + size stacks into one line item.
          const existing = prev.find(
            (i) => i.product_id === product.product_id && i.size === size,
          )
          if (existing) {
            return prev.map((i) =>
              i === existing ? { ...i, quantity: i.quantity + 1 } : i,
            )
          }
          return [
            ...prev,
            {
              product_id: product.product_id,
              name: product.name,
              price: product.price,
              image_url: product.image_url,
              size,
              quantity: 1,
            },
          ]
        }),
      removeItem: (productId, size) =>
        setItems((prev) =>
          prev.filter((i) => !(i.product_id === productId && i.size === size)),
        ),
      clear: () => setItems([]),
    }
  }, [items])

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart(): CartContextValue {
  const context = useContext(CartContext)
  if (!context) throw new Error('useCart must be used within CartProvider')
  return context
}
