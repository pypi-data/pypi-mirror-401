//! Python PyO3 bindings for StateSet ACP Handler

use once_cell::sync::Lazy;
use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::RwLock;
use uuid::Uuid;

// In-memory session store
static SESSIONS: Lazy<RwLock<HashMap<String, CheckoutSessionInternal>>> =
    Lazy::new(|| RwLock::new(HashMap::new()));

// ============================================================================
// Types
// ============================================================================

#[pyclass]
#[derive(Clone, Serialize, Deserialize)]
pub struct Money {
    #[pyo3(get, set)]
    pub amount: i64,
    #[pyo3(get, set)]
    pub currency: String,
}

#[pymethods]
impl Money {
    #[new]
    fn new(amount: i64, currency: String) -> Self {
        Money { amount, currency }
    }

    fn __repr__(&self) -> String {
        format!("Money(amount={}, currency='{}')", self.amount, self.currency)
    }
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize, Default)]
pub struct Address {
    #[pyo3(get, set)]
    pub name: Option<String>,
    #[pyo3(get, set)]
    pub line1: Option<String>,
    #[pyo3(get, set)]
    pub line2: Option<String>,
    #[pyo3(get, set)]
    pub city: Option<String>,
    #[pyo3(get, set)]
    pub region: Option<String>,
    #[pyo3(get, set)]
    pub postal_code: Option<String>,
    #[pyo3(get, set)]
    pub country: Option<String>,
    #[pyo3(get, set)]
    pub phone: Option<String>,
    #[pyo3(get, set)]
    pub email: Option<String>,
}

#[pymethods]
impl Address {
    #[new]
    #[pyo3(signature = (name=None, line1=None, line2=None, city=None, region=None, postal_code=None, country=None, phone=None, email=None))]
    fn new(
        name: Option<String>,
        line1: Option<String>,
        line2: Option<String>,
        city: Option<String>,
        region: Option<String>,
        postal_code: Option<String>,
        country: Option<String>,
        phone: Option<String>,
        email: Option<String>,
    ) -> Self {
        Address {
            name,
            line1,
            line2,
            city,
            region,
            postal_code,
            country,
            phone,
            email,
        }
    }
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize, Default)]
pub struct Customer {
    #[pyo3(get, set)]
    pub billing_address: Option<Address>,
    #[pyo3(get, set)]
    pub shipping_address: Option<Address>,
}

#[pymethods]
impl Customer {
    #[new]
    #[pyo3(signature = (billing_address=None, shipping_address=None))]
    fn new(billing_address: Option<Address>, shipping_address: Option<Address>) -> Self {
        Customer {
            billing_address,
            shipping_address,
        }
    }
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize)]
pub struct LineItem {
    #[pyo3(get, set)]
    pub id: String,
    #[pyo3(get, set)]
    pub title: String,
    #[pyo3(get, set)]
    pub quantity: i32,
    #[pyo3(get, set)]
    pub unit_price: Money,
    #[pyo3(get, set)]
    pub variant_id: Option<String>,
    #[pyo3(get, set)]
    pub sku: Option<String>,
    #[pyo3(get, set)]
    pub image_url: Option<String>,
}

#[pymethods]
impl LineItem {
    fn __repr__(&self) -> String {
        format!(
            "LineItem(id='{}', title='{}', quantity={})",
            self.id, self.title, self.quantity
        )
    }
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize)]
pub struct Totals {
    #[pyo3(get, set)]
    pub subtotal: Money,
    #[pyo3(get, set)]
    pub tax: Money,
    #[pyo3(get, set)]
    pub shipping: Money,
    #[pyo3(get, set)]
    pub discount: Money,
    #[pyo3(get, set)]
    pub grand_total: Money,
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize)]
pub struct CheckoutSession {
    #[pyo3(get)]
    pub id: String,
    #[pyo3(get)]
    pub status: String,
    #[pyo3(get)]
    pub items: Vec<LineItem>,
    #[pyo3(get)]
    pub totals: Totals,
    #[pyo3(get)]
    pub customer: Option<Customer>,
    #[pyo3(get)]
    pub created_at: String,
    #[pyo3(get)]
    pub updated_at: String,
}

#[pymethods]
impl CheckoutSession {
    fn __repr__(&self) -> String {
        format!(
            "CheckoutSession(id='{}', status='{}', items={})",
            self.id,
            self.status,
            self.items.len()
        )
    }
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize)]
pub struct Order {
    #[pyo3(get)]
    pub id: String,
    #[pyo3(get)]
    pub checkout_session_id: String,
    #[pyo3(get)]
    pub status: String,
    #[pyo3(get)]
    pub permalink_url: Option<String>,
}

#[pymethods]
impl Order {
    fn __repr__(&self) -> String {
        format!("Order(id='{}', status='{}')", self.id, self.status)
    }
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize)]
pub struct CheckoutSessionWithOrder {
    #[pyo3(get)]
    pub session: CheckoutSession,
    #[pyo3(get)]
    pub order: Order,
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize)]
pub struct RequestItem {
    #[pyo3(get, set)]
    pub id: String,
    #[pyo3(get, set)]
    pub quantity: i32,
}

#[pymethods]
impl RequestItem {
    #[new]
    fn new(id: String, quantity: i32) -> Self {
        RequestItem { id, quantity }
    }
}

#[pyclass]
#[derive(Clone, Serialize, Deserialize, Default)]
pub struct PaymentRequest {
    #[pyo3(get, set)]
    pub delegated_token: Option<String>,
    #[pyo3(get, set)]
    pub method: Option<String>,
}

#[pymethods]
impl PaymentRequest {
    #[new]
    #[pyo3(signature = (delegated_token=None, method=None))]
    fn new(delegated_token: Option<String>, method: Option<String>) -> Self {
        PaymentRequest {
            delegated_token,
            method,
        }
    }
}

// Internal types
#[derive(Clone, Serialize, Deserialize)]
struct CheckoutSessionInternal {
    id: String,
    status: String,
    items: Vec<LineItem>,
    totals: Totals,
    customer: Option<Customer>,
    created_at: String,
    updated_at: String,
}

impl From<CheckoutSessionInternal> for CheckoutSession {
    fn from(s: CheckoutSessionInternal) -> Self {
        CheckoutSession {
            id: s.id,
            status: s.status,
            items: s.items,
            totals: s.totals,
            customer: s.customer,
            created_at: s.created_at,
            updated_at: s.updated_at,
        }
    }
}

// ============================================================================
// Helper Functions
// ============================================================================

fn get_product(id: &str) -> Option<LineItem> {
    match id {
        "prod_laptop_001" => Some(LineItem {
            id: id.to_string(),
            title: "MacBook Pro 14\"".to_string(),
            quantity: 1,
            unit_price: Money {
                amount: 199900,
                currency: "USD".to_string(),
            },
            variant_id: Some("var_001".to_string()),
            sku: Some("MBP14-M3".to_string()),
            image_url: Some("https://example.com/mbp14.jpg".to_string()),
        }),
        "prod_mouse_002" => Some(LineItem {
            id: id.to_string(),
            title: "Magic Mouse".to_string(),
            quantity: 1,
            unit_price: Money {
                amount: 9900,
                currency: "USD".to_string(),
            },
            variant_id: Some("var_002".to_string()),
            sku: Some("MM-WHITE".to_string()),
            image_url: Some("https://example.com/mouse.jpg".to_string()),
        }),
        "prod_keyboard_003" => Some(LineItem {
            id: id.to_string(),
            title: "Magic Keyboard".to_string(),
            quantity: 1,
            unit_price: Money {
                amount: 29900,
                currency: "USD".to_string(),
            },
            variant_id: Some("var_003".to_string()),
            sku: Some("MK-SILVER".to_string()),
            image_url: Some("https://example.com/keyboard.jpg".to_string()),
        }),
        _ => None,
    }
}

fn calculate_totals(items: &[LineItem]) -> Totals {
    let subtotal: i64 = items
        .iter()
        .map(|i| i.unit_price.amount * i.quantity as i64)
        .sum();
    let tax = (subtotal as f64 * 0.0875) as i64;
    let shipping = if subtotal > 10000 { 0 } else { 999 };
    let discount = 0;
    let grand_total = subtotal + tax + shipping - discount;

    Totals {
        subtotal: Money {
            amount: subtotal,
            currency: "USD".to_string(),
        },
        tax: Money {
            amount: tax,
            currency: "USD".to_string(),
        },
        shipping: Money {
            amount: shipping,
            currency: "USD".to_string(),
        },
        discount: Money {
            amount: discount,
            currency: "USD".to_string(),
        },
        grand_total: Money {
            amount: grand_total,
            currency: "USD".to_string(),
        },
    }
}

// ============================================================================
// ACP Client Class
// ============================================================================

#[pyclass]
pub struct AcpClient {
    api_key: Option<String>,
}

#[pymethods]
impl AcpClient {
    #[new]
    #[pyo3(signature = (api_key=None))]
    fn new(api_key: Option<String>) -> Self {
        AcpClient { api_key }
    }

    fn create_checkout_session(&self, items: Vec<RequestItem>) -> PyResult<CheckoutSession> {
        if items.is_empty() {
            return Err(PyValueError::new_err("At least one item is required"));
        }

        let mut line_items = Vec::new();
        for item in items {
            if let Some(mut product) = get_product(&item.id) {
                product.quantity = item.quantity;
                line_items.push(product);
            } else {
                return Err(PyValueError::new_err(format!(
                    "Product not found: {}",
                    item.id
                )));
            }
        }

        let now = chrono::Utc::now().to_rfc3339();
        let totals = calculate_totals(&line_items);

        let session = CheckoutSessionInternal {
            id: Uuid::new_v4().to_string(),
            status: "not_ready_for_payment".to_string(),
            items: line_items,
            totals,
            customer: None,
            created_at: now.clone(),
            updated_at: now,
        };

        // Store session
        SESSIONS
            .write()
            .map_err(|_| PyRuntimeError::new_err("Failed to acquire lock"))?
            .insert(session.id.clone(), session.clone());

        Ok(session.into())
    }

    fn get_checkout_session(&self, session_id: String) -> PyResult<CheckoutSession> {
        let sessions = SESSIONS
            .read()
            .map_err(|_| PyRuntimeError::new_err("Failed to acquire lock"))?;

        sessions
            .get(&session_id)
            .cloned()
            .map(|s| s.into())
            .ok_or_else(|| PyValueError::new_err(format!("Session not found: {}", session_id)))
    }

    #[pyo3(signature = (session_id, items=None, customer=None))]
    fn update_checkout_session(
        &self,
        session_id: String,
        items: Option<Vec<RequestItem>>,
        customer: Option<Customer>,
    ) -> PyResult<CheckoutSession> {
        let mut sessions = SESSIONS
            .write()
            .map_err(|_| PyRuntimeError::new_err("Failed to acquire lock"))?;

        let session = sessions
            .get_mut(&session_id)
            .ok_or_else(|| PyValueError::new_err(format!("Session not found: {}", session_id)))?;

        if session.status == "completed" || session.status == "canceled" {
            return Err(PyRuntimeError::new_err(
                "Cannot update completed or canceled session",
            ));
        }

        // Update items if provided
        if let Some(items) = items {
            let mut line_items = Vec::new();
            for item in items {
                if let Some(mut product) = get_product(&item.id) {
                    product.quantity = item.quantity;
                    line_items.push(product);
                } else {
                    return Err(PyValueError::new_err(format!(
                        "Product not found: {}",
                        item.id
                    )));
                }
            }
            session.items = line_items;
            session.totals = calculate_totals(&session.items);
        }

        // Update customer if provided
        if customer.is_some() {
            session.customer = customer;
        }

        session.status = "ready_for_payment".to_string();
        session.updated_at = chrono::Utc::now().to_rfc3339();

        Ok(session.clone().into())
    }

    fn complete_checkout_session(
        &self,
        session_id: String,
        payment: PaymentRequest,
    ) -> PyResult<CheckoutSessionWithOrder> {
        let mut sessions = SESSIONS
            .write()
            .map_err(|_| PyRuntimeError::new_err("Failed to acquire lock"))?;

        let session = sessions
            .get_mut(&session_id)
            .ok_or_else(|| PyValueError::new_err(format!("Session not found: {}", session_id)))?;

        if session.status == "completed" {
            return Err(PyRuntimeError::new_err("Session already completed"));
        }

        if session.status == "canceled" {
            return Err(PyRuntimeError::new_err("Cannot complete canceled session"));
        }

        // Validate payment
        if payment.delegated_token.is_none() && payment.method.is_none() {
            return Err(PyValueError::new_err("Payment token or method required"));
        }

        session.status = "completed".to_string();
        session.updated_at = chrono::Utc::now().to_rfc3339();

        let order = Order {
            id: Uuid::new_v4().to_string(),
            checkout_session_id: session.id.clone(),
            status: "placed".to_string(),
            permalink_url: Some(format!("https://orders.example.com/{}", session.id)),
        };

        Ok(CheckoutSessionWithOrder {
            session: session.clone().into(),
            order,
        })
    }

    fn cancel_checkout_session(&self, session_id: String) -> PyResult<CheckoutSession> {
        let mut sessions = SESSIONS
            .write()
            .map_err(|_| PyRuntimeError::new_err("Failed to acquire lock"))?;

        let session = sessions
            .get_mut(&session_id)
            .ok_or_else(|| PyValueError::new_err(format!("Session not found: {}", session_id)))?;

        if session.status == "completed" {
            return Err(PyRuntimeError::new_err("Cannot cancel completed session"));
        }

        session.status = "canceled".to_string();
        session.updated_at = chrono::Utc::now().to_rfc3339();

        Ok(session.clone().into())
    }
}

/// Get library version
#[pyfunction]
fn version() -> String {
    "1.0.0".to_string()
}

/// Python module definition
#[pymodule]
fn stateset_acp_native(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<Money>()?;
    m.add_class::<Address>()?;
    m.add_class::<Customer>()?;
    m.add_class::<LineItem>()?;
    m.add_class::<Totals>()?;
    m.add_class::<CheckoutSession>()?;
    m.add_class::<Order>()?;
    m.add_class::<CheckoutSessionWithOrder>()?;
    m.add_class::<RequestItem>()?;
    m.add_class::<PaymentRequest>()?;
    m.add_class::<AcpClient>()?;
    m.add_function(wrap_pyfunction!(version, m)?)?;
    m.add("__version__", "1.0.0")?;
    Ok(())
}
