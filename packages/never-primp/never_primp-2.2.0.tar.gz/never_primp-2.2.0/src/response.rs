// Response class implementation
use encoding_rs::{Encoding, UTF_8};
use mime::Mime;
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyDict, PyString};
use std::sync::{Arc, Mutex};

use crate::runtime::RUNTIME;

/// Python Response class
///
/// Wraps wreq::Response and provides lazy-loaded properties for content, text, json, etc.
#[pyclass]
pub struct Response {
    // Wrapped wreq::Response (Option because bytes()/text()/json() consume it)
    inner: Arc<Mutex<Option<wreq::Response>>>,

    // Cached values (lazy-loaded)
    _content: Arc<Mutex<Option<Vec<u8>>>>,
    _text: Arc<Mutex<Option<String>>>,
    _encoding: Arc<Mutex<Option<String>>>,
    _headers: Arc<Mutex<Option<Py<PyDict>>>>,
    _cookies: Arc<Mutex<Option<Py<PyDict>>>>,

    // Immutable fields (extracted on creation)
    #[pyo3(get)]
    pub url: String,

    #[pyo3(get)]
    pub status_code: u16,
}

#[pymethods]
impl Response {
    /// Get response content as bytes (lazy-loaded)
    #[getter]
    fn content<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyBytes>> {
        // Check cache first
        {
            let cache = self._content.lock().unwrap();
            if let Some(bytes) = &*cache {
                return Ok(PyBytes::new(py, bytes));
            }
        }

        // Before consuming the response, extract metadata that requires headers
        // This ensures we can still access encoding, headers, cookies after getting content
        self.ensure_metadata_extracted(py)?;

        // Not cached - need to fetch
        let bytes = {
            let mut inner_lock = self.inner.lock().unwrap();
            let response = inner_lock.take()
                .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err(
                    "Response body already consumed"
                ))?;

            // Fetch bytes asynchronously (releasing GIL)
            py.detach(|| {
                RUNTIME.block_on(async {
                    response.bytes().await
                })
            }).map_err(|e| pyo3::exceptions::PyRuntimeError::new_err(e.to_string()))?
        };

        // Convert to Vec<u8> for caching
        let vec_bytes = bytes.to_vec();

        // Cache the result
        {
            let mut cache = self._content.lock().unwrap();
            *cache = Some(vec_bytes.clone());
        }

        Ok(PyBytes::new(py, &vec_bytes))
    }

    /// Get response text with automatic encoding detection (lazy-loaded)
    #[getter]
    fn text<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyString>> {
        // Check cache first
        {
            let cache = self._text.lock().unwrap();
            if let Some(text) = &*cache {
                return Ok(PyString::new(py, text));
            }
        }

        // Get content bytes
        let content = self.content(py)?;
        let raw_bytes = content.as_bytes();

        // Detect encoding
        let encoding_name = self.get_encoding(py)?;

        // Decode bytes
        let text = {
            let encoding = Encoding::for_label(encoding_name.as_bytes()).unwrap_or(UTF_8);
            let (decoded, _, _) = encoding.decode(raw_bytes);
            decoded.into_owned()
        };

        // Cache the result
        {
            let mut cache = self._text.lock().unwrap();
            *cache = Some(text.clone());
        }

        Ok(PyString::new(py, &text))
    }

    /// Parse response as JSON
    fn json(&self, py: Python) -> PyResult<Py<PyAny>> {
        let content = self.content(py)?;
        let raw_bytes = content.as_bytes();

        let json_value: serde_json::Value = serde_json::from_slice(raw_bytes)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(
                format!("Failed to parse JSON: {}", e)
            ))?;

        pythonize::pythonize(py, &json_value)
            .map(|bound| bound.unbind())
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(
                format!("Failed to convert JSON to Python: {}", e)
            ))
    }

    /// Get response headers as dict (lazy-loaded)
    #[getter]
    fn headers(&self, py: Python) -> PyResult<Py<PyDict>> {
        // Check cache first
        {
            let cache = self._headers.lock().unwrap();
            if let Some(headers) = &*cache {
                return Ok(headers.clone_ref(py));
            }
        }

        // Need to extract headers from original response
        // Since we might have consumed the response, we need to store headers separately
        // This is a limitation - we'll need to change our approach

        // For now, return an error if response was consumed
        let inner_lock = self.inner.lock().unwrap();
        if inner_lock.is_none() {
            // If consumed, we should have cached headers during creation
            // Return cached version or error
            return Err(pyo3::exceptions::PyRuntimeError::new_err(
                "Headers not available - response was consumed before headers were accessed"
            ));
        }

        drop(inner_lock);

        // Extract headers without consuming response
        let dict = self.extract_headers(py)?;

        // Cache the result
        {
            let mut cache = self._headers.lock().unwrap();
            *cache = Some(dict.clone_ref(py));
        }

        Ok(dict)
    }

    /// Get cookies from Set-Cookie headers (lazy-loaded)
    #[getter]
    fn cookies(&self, py: Python) -> PyResult<Py<PyDict>> {
        // Check cache first
        {
            let cache = self._cookies.lock().unwrap();
            if let Some(cookies) = &*cache {
                return Ok(cookies.clone_ref(py));
            }
        }

        // Extract cookies from headers
        let dict = self.extract_cookies(py)?;

        // Cache the result
        {
            let mut cache = self._cookies.lock().unwrap();
            *cache = Some(dict.clone_ref(py));
        }

        Ok(dict)
    }

    /// Get encoding from Content-Type header (lazy-loaded)
    #[getter]
    fn encoding(&self, py: Python) -> PyResult<Option<String>> {
        // Check cache first
        {
            let cache = self._encoding.lock().unwrap();
            if let Some(encoding) = &*cache {
                return Ok(Some(encoding.clone()));
            }
        }

        // Try to extract from Content-Type header
        let encoding = match self.extract_encoding(py) {
            Ok(enc) => enc,
            Err(_) => return Ok(None),  // Return None if extraction fails
        };

        // Cache the result
        {
            let mut cache = self._encoding.lock().unwrap();
            *cache = Some(encoding.clone());
        }

        Ok(Some(encoding))
    }
}

impl Response {
    /// Create Response from wreq::Response
    pub fn from_wreq_response(wreq_resp: wreq::Response) -> Self {
        let url = wreq_resp.uri().to_string();
        let status_code = wreq_resp.status().as_u16();

        Response {
            inner: Arc::new(Mutex::new(Some(wreq_resp))),
            _content: Arc::new(Mutex::new(None)),
            _text: Arc::new(Mutex::new(None)),
            _encoding: Arc::new(Mutex::new(None)),
            _headers: Arc::new(Mutex::new(None)),
            _cookies: Arc::new(Mutex::new(None)),
            url,
            status_code,
        }
    }

    /// Internal method to get encoding (returns error if not found)
    fn get_encoding(&self, py: Python) -> PyResult<String> {
        self.encoding(py)?.ok_or_else(|| {
            pyo3::exceptions::PyValueError::new_err("Could not detect encoding")
        })
    }

    /// Ensure all metadata (headers, encoding, cookies) is extracted before consuming response body
    /// This prevents "Response already consumed" errors when accessing multiple properties
    fn ensure_metadata_extracted(&self, py: Python) -> PyResult<()> {
        // Extract headers first (required by encoding and cookies extraction)
        {
            let cache = self._headers.lock().unwrap();
            if cache.is_none() {
                drop(cache);  // Release lock
                let _ = self.extract_headers(py)?;
                // Cache it
                let headers = self.extract_headers(py)?;
                let mut cache = self._headers.lock().unwrap();
                *cache = Some(headers);
            }
        }

        // Extract encoding (depends on headers)
        {
            let cache = self._encoding.lock().unwrap();
            if cache.is_none() {
                drop(cache);  // Release lock
                match self.extract_encoding(py) {
                    Ok(encoding) => {
                        let mut cache = self._encoding.lock().unwrap();
                        *cache = Some(encoding);
                    }
                    Err(_) => {
                        // Encoding extraction failed, set to utf-8 as default
                        let mut cache = self._encoding.lock().unwrap();
                        *cache = Some("utf-8".to_string());
                    }
                }
            }
        }

        // Extract cookies (depends on headers)
        {
            let cache = self._cookies.lock().unwrap();
            if cache.is_none() {
                drop(cache);  // Release lock
                let cookies = self.extract_cookies(py)?;
                let mut cache = self._cookies.lock().unwrap();
                *cache = Some(cookies);
            }
        }

        Ok(())
    }

    /// Extract headers from response without consuming it
    fn extract_headers(&self, py: Python) -> PyResult<Py<PyDict>> {
        let inner_lock = self.inner.lock().unwrap();
        let response = inner_lock.as_ref()
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err(
                "Response already consumed"
            ))?;

        let dict = PyDict::new(py);
        for (key, value) in response.headers() {
            let value_str = value.to_str()
                .map_err(|e| pyo3::exceptions::PyValueError::new_err(
                    format!("Invalid header value: {}", e)
                ))?;
            dict.set_item(key.as_str(), value_str)?;
        }
        Ok(dict.unbind())
    }

    /// Extract cookies from Set-Cookie headers
    fn extract_cookies(&self, py: Python) -> PyResult<Py<PyDict>> {
        let inner_lock = self.inner.lock().unwrap();
        let response = inner_lock.as_ref()
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err(
                "Response already consumed"
            ))?;

        let dict = PyDict::new(py);
        let set_cookie_headers = response.headers().get_all(http::header::SET_COOKIE);

        for cookie_header in set_cookie_headers.iter() {
            if let Ok(cookie_str) = cookie_header.to_str() {
                // Simple cookie parsing (name=value;...)
                if let Some((name, rest)) = cookie_str.split_once('=') {
                    let value = rest.split(';').next().unwrap_or("").trim();
                    dict.set_item(name.trim(), value)?;
                }
            }
        }
        Ok(dict.unbind())
    }

    /// Extract encoding from Content-Type header
    fn extract_encoding(&self, _py: Python) -> PyResult<String> {
        let inner_lock = self.inner.lock().unwrap();
        let response = inner_lock.as_ref()
            .ok_or_else(|| pyo3::exceptions::PyRuntimeError::new_err(
                "Response already consumed"
            ))?;

        let encoding = response.headers()
            .get(http::header::CONTENT_TYPE)
            .and_then(|v| v.to_str().ok())
            .and_then(|v| v.parse::<Mime>().ok())
            .and_then(|m| m.get_param("charset").map(|c| c.to_string()))
            .unwrap_or_else(|| "utf-8".to_string());

        Ok(encoding)
    }
}
