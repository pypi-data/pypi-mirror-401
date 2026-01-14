// Error handling
use pyo3::exceptions::PyRuntimeError;
use pyo3::PyErr;

/// Convert anyhow::Error to PyErr
pub fn anyhow_to_pyerr(err: anyhow::Error) -> PyErr {
    PyErr::new::<PyRuntimeError, _>(err.to_string())
}

/// Result type alias using anyhow::Error
#[allow(dead_code)]
pub type Result<T> = std::result::Result<T, anyhow::Error>;
