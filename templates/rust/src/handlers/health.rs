use actix_web::{HttpResponse, Responder};

pub async fn health() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({
        "status": "ok",
        "message": "Rust API is running"
    }))
}

pub async fn api_info() -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({
        "name": "Rust REST API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "Homepage",
            "GET /health": "Health check",
            "GET /api/": "API info",
            "GET /api/items": "List all items",
            "POST /api/items": "Create new item",
            "GET /api/items/{id}": "Get item by ID",
            "DELETE /api/items/{id}": "Delete item by ID"
        }
    }))
}

