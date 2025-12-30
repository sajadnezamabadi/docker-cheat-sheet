package models

// Item represents an item in the database
type Item struct {
	ID          int    `json:"id" db:"id"`
	Name        string `json:"name" db:"name"`
	Description string `json:"description" db:"description"`
	CreatedAt   string `json:"created_at" db:"created_at"`
}

// CreateItemRequest represents the request to create an item
type CreateItemRequest struct {
	Name        string `json:"name" binding:"required"`
	Description string `json:"description"`
}

