use actix_web::web;
use crate::handlers::{home, health, items};

pub fn configure_routes(cfg: &mut web::ServiceConfig) {
    cfg
        .route("/", web::get().to(home::home))
        .route("/health", web::get().to(health::health))
        .route("/api/", web::get().to(health::api_info))
        .route("/api/items", web::get().to(items::list_items))
        .route("/api/items", web::post().to(items::create_item))
        .route("/api/items/{id}", web::get().to(items::get_item))
        .route("/api/items/{id}", web::delete().to(items::delete_item));
}

