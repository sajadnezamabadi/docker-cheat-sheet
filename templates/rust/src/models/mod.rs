use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Item {
    pub id: Option<i32>,
    pub name: String,
    pub description: Option<String>,
    pub created_at: Option<String>,
}

#[derive(Deserialize, Debug)]
pub struct CreateItem {
    pub name: String,
    pub description: Option<String>,
}

