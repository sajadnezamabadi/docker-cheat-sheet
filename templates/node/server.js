const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = 3000;

// Database connection
const pool = new Pool({
  host: process.env.POSTGRES_HOST || 'db',
  database: process.env.POSTGRES_DB || 'nodedb',
  user: process.env.POSTGRES_USER || 'node',
  password: process.env.POSTGRES_PASSWORD || 'node',
  port: process.env.POSTGRES_PORT || 5432,
});

// In-memory storage (for demo)
let items = [];
let nextId = 1;

// Middleware
app.use(express.json());
app.use(express.static('public'));

// Home page
app.get('/', (req, res) => {
  const html = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Node.js Docker Demo</title>
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
            <h1>Node.js Docker Demo</h1>
            <p style="font-size: 1.2em; color: #333; margin-bottom: 30px;">
                Welcome to Node.js + Express running in Docker! 🚀
            </p>
            
            <div class="info-box">
                <strong>Framework:</strong> Express.js<br>
                <strong>Runtime:</strong> Node.js<br>
                <strong>Database:</strong> ${process.env.POSTGRES_DB || 'nodedb'}<br>
                <strong>Host:</strong> ${process.env.POSTGRES_HOST || 'db'}<br>
                <strong>Port:</strong> ${port}
            </div>
            
            <div class="endpoints">
                <h3>Available Endpoints:</h3>
                <div class="endpoint">GET /api/ - API Information</div>
                <div class="endpoint">GET /api/items - List all items</div>
                <div class="endpoint">POST /api/items - Create new item</div>
                <div class="endpoint">GET /api/items/:id - Get item by ID</div>
                <div class="endpoint">DELETE /api/items/:id - Delete item</div>
            </div>
            
            <a href="/api/" class="btn">View API Info</a>
            <a href="/api/items" class="btn" style="margin-left: 10px; background: #764ba2;">View Items</a>
        </div>
    </body>
    </html>
  `;
  res.send(html);
});

// API Info
app.get('/api/', (req, res) => {
  res.json({
    status: 'success',
    framework: 'Express.js',
    runtime: 'Node.js',
    database: process.env.POSTGRES_DB || 'nodedb',
    database_host: process.env.POSTGRES_HOST || 'db',
    message: 'Node.js API is working perfectly!',
    endpoints: {
      home: '/',
      api_info: '/api/',
      items: '/api/items',
      create_item: 'POST /api/items',
      get_item: 'GET /api/items/:id',
      delete_item: 'DELETE /api/items/:id'
    }
  });
});

// Get all items
app.get('/api/items', (req, res) => {
  res.json({
    status: 'success',
    count: items.length,
    items: items
  });
});

// Create item
app.post('/api/items', (req, res) => {
  const { name, description } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'Name is required' });
  }
  
  const item = {
    id: nextId++,
    name,
    description: description || '',
    createdAt: new Date().toISOString()
  };
  
  items.push(item);
  res.status(201).json({
    status: 'success',
    message: 'Item created',
    item: item
  });
});

// Get item by ID
app.get('/api/items/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const item = items.find(i => i.id === id);
  
  if (!item) {
    return res.status(404).json({ error: 'Item not found' });
  }
  
  res.json({
    status: 'success',
    item: item
  });
});

// Delete item
app.delete('/api/items/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const index = items.findIndex(i => i.id === id);
  
  if (index === -1) {
    return res.status(404).json({ error: 'Item not found' });
  }
  
  const deleted = items.splice(index, 1)[0];
  res.json({
    status: 'success',
    message: 'Item deleted',
    item: deleted
  });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

// Start server
app.listen(port, '0.0.0.0', () => {
  console.log(`🚀 Server running at http://0.0.0.0:${port}`);
  console.log(`📦 Database: ${process.env.POSTGRES_DB || 'nodedb'}`);
});

