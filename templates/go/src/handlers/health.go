package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

// Health handles health check endpoint
func Health(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":  "ok",
		"message": "Go API is running",
	})
}

// APIInfo returns API information
func APIInfo(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"name":    "Go REST API",
		"version": "1.0.0",
		"endpoints": gin.H{
			"GET /":              "Homepage",
			"GET /health":        "Health check",
			"GET /api/":          "API info",
			"GET /api/items":     "List all items",
			"POST /api/items":    "Create new item",
			"GET /api/items/:id": "Get item by ID",
			"DELETE /api/items/:id": "Delete item by ID",
		},
	})
}

