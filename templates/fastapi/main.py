from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import os
from datetime import datetime

app = FastAPI(
    title="FastAPI Docker Demo",
    description="A simple FastAPI application running in Docker",
    version="1.0.0"
)

# In-memory database (for demo)
items_db = []

class Item(BaseModel):
    name: str
    description: str = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str = None
    created_at: str

@app.get("/", response_class=HTMLResponse)
async def root():
    """Home page with Docker info"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI Docker Demo</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 700px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            .status {
                display: inline-block;
                padding: 5px 15px;
                background: #28a745;
                color: white;
                border-radius: 20px;
                font-size: 0.9em;
                margin-bottom: 20px;
            }
            .info-box {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
            }
            .info-box strong {
                color: #667eea;
            }
            .endpoints {
                margin-top: 30px;
            }
            .endpoint {
                background: #f8f9fa;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                font-family: monospace;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #5568d3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <span class="status">✓ Running</span>
            <h1>FastAPI Docker Demo</h1>
            <p style="font-size: 1.2em; color: #333; margin-bottom: 30px;">
                Welcome to FastAPI running in Docker! 🚀
            </p>
            
            <div class="info-box">
                <strong>Framework:</strong> FastAPI<br>
                <strong>Database:</strong> """ + os.environ.get('POSTGRES_DB', 'fastapidb') + """<br>
                <strong>Host:</strong> """ + os.environ.get('POSTGRES_HOST', 'db') + """<br>
                <strong>Current Time:</strong> """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
            </div>
            
            <div class="endpoints">
                <h3>Available Endpoints:</h3>
                <div class="endpoint">GET /api/ - API Information</div>
                <div class="endpoint">GET /items/ - List all items</div>
                <div class="endpoint">POST /items/ - Create new item</div>
                <div class="endpoint">GET /docs - Interactive API Documentation</div>
            </div>
            
            <a href="/docs" class="btn">View API Docs</a>
            <a href="/api/" class="btn" style="margin-left: 10px; background: #764ba2;">API Info</a>
        </div>
    </body>
    </html>
    """
    return html_content

@app.get("/api/")
async def api_info():
    """API information endpoint"""
    return {
        "status": "success",
        "framework": "FastAPI",
        "database": os.environ.get('POSTGRES_DB', 'fastapidb'),
        "database_host": os.environ.get('POSTGRES_HOST', 'db'),
        "message": "FastAPI is working perfectly!",
        "endpoints": {
            "home": "/",
            "api_info": "/api/",
            "items": "/items/",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/items/", response_model=List[ItemResponse])
async def get_items():
    """Get all items"""
    return items_db

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: Item):
    """Create a new item"""
    new_item = ItemResponse(
        id=len(items_db) + 1,
        name=item.name,
        description=item.description,
        created_at=datetime.now().isoformat()
    )
    items_db.append(new_item)
    return new_item

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id < 1 or item_id > len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id - 1]

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item by ID"""
    if item_id < 1 or item_id > len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id - 1)
    # Update IDs
    for i, item in enumerate(items_db):
        item.id = i + 1
    return {"message": "Item deleted", "item": deleted_item}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

