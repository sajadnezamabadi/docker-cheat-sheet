use actix_web::{HttpResponse, Responder};

pub async fn home() -> impl Responder {
    HttpResponse::Ok().body(r#"
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rust API</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                h1 { color: #333; }
                .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
                code { background: #e0e0e0; padding: 2px 5px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <h1>🚀 Rust REST API</h1>
            <p>Welcome to the Rust API with PostgreSQL!</p>
            <h2>Endpoints:</h2>
            <div class="endpoint"><code>GET /health</code> - Health check</div>
            <div class="endpoint"><code>GET /api/</code> - API information</div>
            <div class="endpoint"><code>GET /api/items</code> - List all items</div>
            <div class="endpoint"><code>POST /api/items</code> - Create new item</div>
            <div class="endpoint"><code>GET /api/items/{id}</code> - Get item by ID</div>
            <div class="endpoint"><code>DELETE /api/items/{id}</code> - Delete item by ID</div>
            <h2>Try it:</h2>
            <p><a href="/api/">API Info</a> | <a href="/api/items">Items List</a> | <a href="/health">Health Check</a></p>
        </body>
        </html>
    "#)
}

