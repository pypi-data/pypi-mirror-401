// never_primp: High-performance Python HTTP client with browser impersonation
use pyo3::prelude::*;

mod browser_mapping;
mod client;
mod error;
mod response;
mod runtime;
mod types;
mod utils;

use client::RClient;
use response::Response;

/// Convenience function: HTTP GET
#[pyfunction]
fn get(py: Python, url: String) -> PyResult<Response> {
    let client = RClient::new_default()?;
    client.request(
        py,
        "GET",
        &url,
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None,
    )
}

/// Convenience function: HTTP POST
#[pyfunction]
fn post(py: Python, url: String) -> PyResult<Response> {
    let client = RClient::new_default()?;
    client.request(
        py,
        "POST",
        &url,
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None,
    )
}

/// Convenience function: HTTP PUT
#[pyfunction]
fn put(py: Python, url: String) -> PyResult<Response> {
    let client = RClient::new_default()?;
    client.request(
        py,
        "PUT",
        &url,
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None,
    )
}

/// Convenience function: HTTP DELETE
#[pyfunction]
fn delete(py: Python, url: String) -> PyResult<Response> {
    let client = RClient::new_default()?;
    client.request(
        py,
        "DELETE",
        &url,
        None, None, None, None, None, None, None, None, None, None, None, None,
        None, None, None, None, None, None, None, None, None, None,
    )
}

/// never_primp Python module
#[pymodule]
fn never_primp(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Register classes
    m.add_class::<RClient>()?;
    m.add_class::<Response>()?;

    // Register convenience functions
    m.add_function(wrap_pyfunction!(get, m)?)?;
    m.add_function(wrap_pyfunction!(post, m)?)?;
    m.add_function(wrap_pyfunction!(put, m)?)?;
    m.add_function(wrap_pyfunction!(delete, m)?)?;

    Ok(())
}
