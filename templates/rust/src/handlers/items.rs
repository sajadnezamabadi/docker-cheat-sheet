use actix_web::{web, HttpResponse, Responder, Result};
use sqlx::PgPool;
use chrono::DateTime;
use chrono::Utc;

use crate::models::{Item, CreateItem};

pub async fn list_items(pool: web::Data<PgPool>) -> Result<impl Responder> {
    let rows = sqlx::query("SELECT id, name, description, created_at FROM items ORDER BY id")
        .fetch_all(pool.get_ref())
        .await
        .map_err(|e| {
            eprintln!("Database error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    let items: Vec<Item> = rows
        .iter()
        .map(|row| Item {
            id: Some(row.get("id")),
            name: row.get("name"),
            description: row.get("description"),
            created_at: row.get::<Option<DateTime<Utc>>, _>("created_at")
                .map(|dt| dt.format("%Y-%m-%d %H:%M:%S").to_string()),
        })
        .collect();

    Ok(HttpResponse::Ok().json(items))
}

pub async fn get_item(pool: web::Data<PgPool>, path: web::Path<i32>) -> Result<impl Responder> {
    let id = path.into_inner();
    
    let row = sqlx::query("SELECT id, name, description, created_at FROM items WHERE id = $1")
        .bind(id)
        .fetch_optional(pool.get_ref())
        .await
        .map_err(|e| {
            eprintln!("Database error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    match row {
        Some(row) => {
            let item = Item {
                id: Some(row.get("id")),
                name: row.get("name"),
                description: row.get("description"),
                created_at: row.get::<Option<DateTime<Utc>>, _>("created_at")
                    .map(|dt| dt.format("%Y-%m-%d %H:%M:%S").to_string()),
            };
            Ok(HttpResponse::Ok().json(item))
        }
        None => Ok(HttpResponse::NotFound().json(serde_json::json!({
            "error": "Item not found"
        }))),
    }
}

pub async fn create_item(
    pool: web::Data<PgPool>,
    item: web::Json<CreateItem>,
) -> Result<impl Responder> {
    let result = sqlx::query(
        "INSERT INTO items (name, description) VALUES ($1, $2) RETURNING id, name, description, created_at"
    )
    .bind(&item.name)
    .bind(&item.description)
    .fetch_one(pool.get_ref())
    .await
    .map_err(|e| {
        eprintln!("Database error: {}", e);
        actix_web::error::ErrorInternalServerError("Database error")
    })?;

    let created_item = Item {
        id: Some(result.get("id")),
        name: result.get("name"),
        description: result.get("description"),
        created_at: result.get::<Option<DateTime<Utc>>, _>("created_at")
            .map(|dt| dt.format("%Y-%m-%d %H:%M:%S").to_string()),
    };

    Ok(HttpResponse::Created().json(created_item))
}

pub async fn delete_item(pool: web::Data<PgPool>, path: web::Path<i32>) -> Result<impl Responder> {
    let id = path.into_inner();
    
    let result = sqlx::query("DELETE FROM items WHERE id = $1")
        .bind(id)
        .execute(pool.get_ref())
        .await
        .map_err(|e| {
            eprintln!("Database error: {}", e);
            actix_web::error::ErrorInternalServerError("Database error")
        })?;

    if result.rows_affected() > 0 {
        Ok(HttpResponse::Ok().json(serde_json::json!({
            "message": "Item deleted successfully",
            "id": id
        })))
    } else {
        Ok(HttpResponse::NotFound().json(serde_json::json!({
            "error": "Item not found"
        })))
    }
}

