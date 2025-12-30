use actix_web::{web, App, HttpServer};
use sqlx::PgPool;
use std::env;

mod handlers;
mod models;
mod database;
mod routes;

use database::init_db;
use routes::configure_routes;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();

    let database_url = env::var("DATABASE_URL").unwrap_or_else(|_| {
        format!(
            "postgres://{}:{}@{}/{}",
            env::var("POSTGRES_USER").unwrap_or_else(|_| "rust".to_string()),
            env::var("POSTGRES_PASSWORD").unwrap_or_else(|_| "rust".to_string()),
            env::var("POSTGRES_HOST").unwrap_or_else(|_| "db".to_string()),
            env::var("POSTGRES_DB").unwrap_or_else(|_| "rustdb".to_string()),
        )
    });

    println!("Connecting to database...");
    let pool = PgPool::connect(&database_url)
        .await
        .expect("Failed to connect to database");

    println!("Initializing database...");
    init_db(&pool).await.expect("Failed to initialize database");

    println!("Starting server on 0.0.0.0:8000");
    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(pool.clone()))
            .configure(configure_routes)
    })
    .bind("0.0.0.0:8000")?
    .run()
    .await
}
