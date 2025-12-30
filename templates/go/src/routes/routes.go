package routes

import (
	"github.com/gin-gonic/gin"
	"go-api/src/handlers"
)

// SetupRoutes configures all routes
func SetupRoutes(r *gin.Engine) {
	// Homepage
	r.GET("/", handlers.Home)

	// Health check
	r.GET("/health", handlers.Health)

	// API info
	r.GET("/api/", handlers.APIInfo)

	// Items routes
	api := r.Group("/api")
	{
		api.GET("/items", handlers.ListItems)
		api.POST("/items", handlers.CreateItem)
		api.GET("/items/:id", handlers.GetItem)
		api.DELETE("/items/:id", handlers.DeleteItem)
	}
}

