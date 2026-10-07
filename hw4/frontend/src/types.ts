export interface InventoryItem {
  size: string
  quantity: number
}

export interface Product {
  product_id: string
  name: string
  garment_type: string
  category: string
  description: string
  short_description: string
  colors: string[]
  search_tags: string[]
  image_file_path: string
  image_url: string
  price: number
  inventory: InventoryItem[]
  total_stock: number
}

export interface AuthUser {
  id: number
  name: string
  email: string
  first_name: string | null
  last_name: string | null
}

export const formatPrice = (price: number): string => `$${price.toFixed(2)}`
