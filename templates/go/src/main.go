package main

import (
	"log"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
	"go-api/src/database"
	"go-api/src/routes"
)

func main() {
	// Load environment variables
	godotenv.Load()

	// Initialize database
	if err := database.InitDB(); err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer database.DB.Close()

	// Set Gin mode
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	// Setup routes
	routes.SetupRoutes(r)

	// Get port from environment or use default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8000"
	}

	log.Printf("Starting server on 0.0.0.0:%s", port)
	if err := r.Run(":" + port); err != nil {
		log.Fatal("Failed to start server:", err)
	}
}

