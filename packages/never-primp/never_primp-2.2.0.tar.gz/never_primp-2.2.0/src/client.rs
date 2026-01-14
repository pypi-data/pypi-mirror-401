// RClient (synchronous client) implementation
use std::sync::{Arc, Mutex};
use std::time::Duration;

use pyo3::prelude::*;
use pyo3::types::PyAny;
use pythonize::depythonize;
use serde_json::Value;
use wreq::{EmulationFactory, Method};
use wreq::cookie::CookieStore;

use crate::browser_mapping::{map_browser_to_emulation, map_os_to_emulation_os};
use crate::error::anyhow_to_pyerr;
use crate::response::Response;
use crate::runtime::RUNTIME;
use crate::types::IndexMapSSR;

#[pyclass(subclass)]
/// HTTP client with browser impersonation support
pub struct RClient {
    client: Arc<Mutex<wreq::Client>>,
    // Store the cookie jar separately for Python-side cookie management
    cookie_jar: Option<Arc<wreq::cookie::Jar>>,

    // Client-level configuration (exposed to Python)
    #[pyo3(get, set)]
    pub auth: Option<(String, Option<String>)>,

    #[pyo3(get, set)]
    pub auth_bearer: Option<String>,

    #[pyo3(get, set)]
    pub params: Option<IndexMapSSR>,

    #[pyo3(get, set)]
    pub proxy: Option<String>,

    #[pyo3(get, set)]
    pub timeout: Option<f64>,

    #[pyo3(get)]
    pub impersonate: Option<String>,

    #[pyo3(get)]
    pub impersonate_os: Option<String>,

    // Internal configuration (not exposed)
    headers: Option<IndexMapSSR>,
    cookie_store: Option<bool>,
    referer: Option<bool>,
    follow_redirects: Option<bool>,
    max_redirects: Option<usize>,
    verify: Option<bool>,
    ca_cert_file: Option<String>,
    https_only: Option<bool>,
    http1_only: Option<bool>,
    http2_only: Option<bool>,
    #[pyo3(get, set)]
    split_cookies: Option<bool>,
}

#[pymethods]
impl RClient {
    /// Create a new HTTP client with default settings (for convenience functions)
    #[staticmethod]
    pub(crate) fn new_default() -> PyResult<Self> {
        Self::new(
            None,
            None,
            None,
            None,
            Some(true),
            Some(true),
            None,
            None,
            None,
            None,
            Some(true),
            Some(20),
            Some(true),
            None,
            Some(false),
            Some(false),
            Some(false),
            None,
        )
    }

    /// Create a new HTTP client
    ///
    /// # Arguments
    ///
    /// * `auth` - Basic authentication (username, password)
    /// * `auth_bearer` - Bearer token authentication
    /// * `params` - Default query parameters
    /// * `headers` - Default headers
    /// * `cookie_store` - Enable cookie persistence (default: true)
    /// * `referer` - Auto-set Referer header (default: true)
    /// * `proxy` - Proxy URL
    /// * `timeout` - Request timeout in seconds
    /// * `impersonate` - Browser to impersonate (e.g., "chrome_143", "firefox_146")
    /// * `impersonate_os` - OS to impersonate (e.g., "windows", "macos")
    /// * `follow_redirects` - Follow redirects (default: true)
    /// * `max_redirects` - Maximum redirects (default: 20)
    /// * `verify` - Verify SSL certificates (default: true)
    /// * `ca_cert_file` - Path to CA certificate file
    /// * `https_only` - Restrict to HTTPS only (default: false)
    /// * `http1_only` - Use HTTP/1.1 only (default: false)
    /// * `http2_only` - Use HTTP/2 only (default: false)
    /// * `split_cookies` - Send cookies in separate headers (HTTP/2 style, default: None)
    #[new]
    #[pyo3(signature = (
        auth=None, auth_bearer=None, params=None, headers=None, cookie_store=Some(true),
        referer=Some(true), proxy=None, timeout=None, impersonate=None, impersonate_os=None,
        follow_redirects=Some(true), max_redirects=Some(20), verify=Some(true), ca_cert_file=None,
        https_only=Some(false), http1_only=Some(false), http2_only=Some(false), split_cookies=None
    ))]
    fn new(
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        params: Option<IndexMapSSR>,
        headers: Option<IndexMapSSR>,
        cookie_store: Option<bool>,
        referer: Option<bool>,
        proxy: Option<String>,
        timeout: Option<f64>,
        impersonate: Option<String>,
        impersonate_os: Option<String>,
        follow_redirects: Option<bool>,
        max_redirects: Option<usize>,
        verify: Option<bool>,
        ca_cert_file: Option<String>,
        https_only: Option<bool>,
        http1_only: Option<bool>,
        http2_only: Option<bool>,
        split_cookies: Option<bool>,
    ) -> PyResult<Self> {
        let mut client_builder = wreq::Client::builder();

        // Browser impersonation
        if let Some(browser) = &impersonate {
            let emulation = map_browser_to_emulation(browser).map_err(anyhow_to_pyerr)?;

            // If OS is specified, use EmulationOption
            if let Some(os) = &impersonate_os {
                let emulation_os = map_os_to_emulation_os(os).map_err(anyhow_to_pyerr)?;
                let emulation_option = wreq_util::EmulationOption::builder()
                    .emulation(emulation)
                    .emulation_os(emulation_os)
                    .build();
                client_builder = client_builder.emulation(emulation_option.emulation());
            } else {
                // Use EmulationFactory trait
                client_builder = client_builder.emulation(emulation);
            }
        }

        // Connection pool optimization for high concurrency
        client_builder = client_builder
            .pool_max_idle_per_host(512)
            .pool_idle_timeout(Duration::from_secs(90));

        // Cookie store - create Jar and pass to client
        let cookie_jar = if cookie_store.unwrap_or(true) {
            let jar = Arc::new(wreq::cookie::Jar::new(true)); // compressed by default
            client_builder = client_builder.cookie_provider(jar.clone());
            Some(jar)
        } else {
            None
        };

        // Referer
        if referer.unwrap_or(true) {
            client_builder = client_builder.referer(true);
        }

        // Proxy
        let proxy = proxy.or_else(|| std::env::var("PRIMP_PROXY").ok());
        if let Some(proxy_url) = &proxy {
            let proxy = wreq::Proxy::all(proxy_url)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
            client_builder = client_builder.proxy(proxy);
        }

        // Timeout
        if let Some(seconds) = timeout {
            client_builder = client_builder.timeout(Duration::from_secs_f64(seconds));
        }

        // Redirects
        if follow_redirects.unwrap_or(true) {
            client_builder = client_builder
                .redirect(wreq::redirect::Policy::limited(max_redirects.unwrap_or(20)));
        } else {
            client_builder = client_builder.redirect(wreq::redirect::Policy::none());
        }

        // Ca_cert_file. Set env var before calling load_ca_certs
        if let Some(ca_bundle_path) = &ca_cert_file {
            unsafe {
                std::env::set_var("PRIMP_CA_BUNDLE", ca_bundle_path);
            }
        }

        // SSL verification
        if !verify.unwrap_or(true) {
            client_builder = client_builder.cert_verification(false);
        } else if let Some(cert_store) = crate::utils::load_ca_certs() {
            client_builder = client_builder.cert_store(cert_store.clone());
        }

        // HTTPS only
        if https_only.unwrap_or(false) {
            client_builder = client_builder.https_only(true);
        }

        // HTTP version control
        // Note: wreq API may differ from rquest, check wreq documentation
        // For now, prioritize http1_only > http2_only
        if http1_only.unwrap_or(false) {
            // Force HTTP/1.1 only (if wreq supports this API)
            // client_builder = client_builder.http1_only();
        } else if http2_only.unwrap_or(false) {
            // Force HTTP/2 only
            client_builder = client_builder.http2_only();
        }

        // Build client
        let client = client_builder
            .build()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        Ok(RClient {
            client: Arc::new(Mutex::new(client)),
            cookie_jar,
            auth,
            auth_bearer,
            params,
            proxy,
            timeout,
            impersonate,
            impersonate_os,
            headers,
            cookie_store,
            referer,
            follow_redirects,
            max_redirects,
            verify,
            ca_cert_file,
            https_only,
            http1_only,
            http2_only,
            split_cookies,
        })
    }

    /// Get a specific cookie by name for a URL
    ///
    /// # Arguments
    /// * `name` - Cookie name
    /// * `url` - URL to get cookie for
    ///
    /// # Returns
    /// Cookie value as string, or None if not found
    #[pyo3(signature = (name, url))]
    pub fn get_cookie(&self, name: &str, url: &str) -> PyResult<Option<String>> {
        if let Some(jar) = &self.cookie_jar {
            if let Some(cookie) = jar.get(name, url) {
                return Ok(Some(cookie.value().to_string()));
            }
        }
        Ok(None)
    }

    /// Get all cookies for a specific URL
    ///
    /// # Arguments
    /// * `url` - URL to get cookies for
    ///
    /// # Returns
    /// Dictionary of cookie name-value pairs
    #[pyo3(signature = (url))]
    pub fn get_cookies(&self, url: &str) -> PyResult<IndexMapSSR> {
        let mut cookies = IndexMapSSR::default();

        if let Some(jar) = &self.cookie_jar {
            // Parse URL - use wreq::IntoUri or http::Uri
            let uri: http::Uri = url.parse()
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("Invalid URL: {}", e)
                ))?;

            // Get cookies using CookieStore trait
            match jar.cookies(&uri) {
                wreq::cookie::Cookies::Compressed(header) => {
                    // Parse compressed cookie header: "name1=value1; name2=value2"
                    if let Ok(cookie_str) = header.to_str() {
                        for pair in cookie_str.split(';') {
                            let pair = pair.trim();
                            if let Some((name, value)) = pair.split_once('=') {
                                cookies.insert(name.to_string(), value.to_string());
                            }
                        }
                    }
                }
                wreq::cookie::Cookies::Uncompressed(headers) => {
                    // Parse uncompressed cookie headers: multiple "name=value" headers
                    for header in headers {
                        if let Ok(cookie_str) = header.to_str() {
                            if let Some((name, value)) = cookie_str.split_once('=') {
                                cookies.insert(name.to_string(), value.to_string());
                            }
                        }
                    }
                }
                wreq::cookie::Cookies::Empty | _ => {
                    // No cookies or unknown variant
                }
            }
        }

        Ok(cookies)
    }

    /// Set a cookie for a specific URL
    ///
    /// # Arguments
    /// * `name` - Cookie name
    /// * `value` - Cookie value
    /// * `url` - URL to set cookie for
    /// * `domain` - Optional domain attribute
    /// * `path` - Optional path attribute
    #[pyo3(signature = (name, value, url, domain=None, path=None))]
    pub fn set_cookie(
        &self,
        name: &str,
        value: &str,
        url: &str,
        domain: Option<&str>,
        path: Option<&str>,
    ) -> PyResult<()> {
        if let Some(jar) = &self.cookie_jar {
            // Build cookie string
            let mut cookie_str = format!("{}={}", name, value);
            if let Some(d) = domain {
                cookie_str.push_str(&format!("; Domain={}", d));
            }
            if let Some(p) = path {
                cookie_str.push_str(&format!("; Path={}", p));
            }

            jar.add_cookie_str(&cookie_str, url);
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Cookie store is disabled. Enable it by setting cookie_store=True"
            ))
        }
    }

    /// Set multiple cookies for a specific URL
    ///
    /// # Arguments
    /// * `url` - URL to set cookies for
    /// * `cookies` - Dictionary of cookie name-value pairs
    #[pyo3(signature = (url, cookies))]
    pub fn set_cookies(&self, url: &str, cookies: IndexMapSSR) -> PyResult<()> {
        if let Some(jar) = &self.cookie_jar {
            for (name, value) in cookies {
                jar.add_cookie_str(&format!("{}={}", name, value), url);
            }
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Cookie store is disabled. Enable it by setting cookie_store=True"
            ))
        }
    }

    /// Remove a cookie by name for a specific URL
    ///
    /// # Arguments
    /// * `name` - Cookie name to remove
    /// * `url` - URL to remove cookie for
    #[pyo3(signature = (name, url))]
    pub fn remove_cookie(&self, name: &str, url: &str) -> PyResult<()> {
        if let Some(jar) = &self.cookie_jar {
            // Create a cookie to remove using the cookie crate's API
            let raw_cookie = cookie::Cookie::build((name.to_string(), String::new())).build();
            jar.remove(raw_cookie, url);
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Cookie store is disabled"
            ))
        }
    }

    /// Clear all cookies
    #[pyo3(signature = ())]
    pub fn clear_cookies(&self) -> PyResult<()> {
        if let Some(jar) = &self.cookie_jar {
            jar.clear();
            Ok(())
        } else {
            Err(PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(
                "Cookie store is disabled"
            ))
        }
    }

    /// Get all cookies in the jar (across all domains)
    ///
    /// # Returns
    /// List of tuples (name, value, domain, path)
    #[pyo3(signature = ())]
    pub fn get_all_cookies(&self) -> PyResult<Vec<(String, String)>> {
        if let Some(jar) = &self.cookie_jar {
            let cookies: Vec<(String, String)> = jar
                .get_all()
                .map(|cookie| (cookie.name().to_string(), cookie.value().to_string()))
                .collect();
            Ok(cookies)
        } else {
            Ok(Vec::new())
        }
    }

    /// Get client-level headers
    ///
    /// # Returns
    /// Dictionary of header name-value pairs
    #[pyo3(signature = ())]
    pub fn get_headers(&self) -> PyResult<IndexMapSSR> {
        Ok(self.headers.clone().unwrap_or_default())
    }

    /// Set client-level headers (replaces all existing headers)
    ///
    /// # Arguments
    /// * `headers` - Dictionary of header name-value pairs
    #[pyo3(signature = (headers))]
    pub fn set_headers(&mut self, headers: Option<IndexMapSSR>) -> PyResult<()> {
        self.headers = headers;
        Ok(())
    }

    /// Update client-level headers (merges with existing headers)
    ///
    /// # Arguments
    /// * `headers` - Dictionary of header name-value pairs to add/update
    #[pyo3(signature = (headers))]
    pub fn headers_update(&mut self, headers: IndexMapSSR) -> PyResult<()> {
        if let Some(ref mut existing_headers) = self.headers {
            // Update existing headers (preserves insertion order)
            for (key, value) in headers {
                existing_headers.insert(key, value);
            }
        } else {
            // No existing headers, set new ones
            self.headers = Some(headers);
        }
        Ok(())
    }

    /// Set a single header
    ///
    /// # Arguments
    /// * `name` - Header name
    /// * `value` - Header value
    #[pyo3(signature = (name, value))]
    pub fn set_header(&mut self, name: String, value: String) -> PyResult<()> {
        if let Some(ref mut existing_headers) = self.headers {
            existing_headers.insert(name, value);
        } else {
            let mut new_headers = IndexMapSSR::default();
            new_headers.insert(name, value);
            self.headers = Some(new_headers);
        }
        Ok(())
    }

    /// Get a single header value by name
    ///
    /// # Arguments
    /// * `name` - Header name
    ///
    /// # Returns
    /// Header value as string, or None if not found
    #[pyo3(signature = (name))]
    pub fn get_header(&self, name: String) -> PyResult<Option<String>> {
        if let Some(ref headers) = self.headers {
            return Ok(headers.get(&name).cloned());
        }
        Ok(None)
    }

    /// Delete a single header by name
    ///
    /// # Arguments
    /// * `name` - Header name to remove
    #[pyo3(signature = (name))]
    pub fn delete_header(&mut self, name: String) -> PyResult<()> {
        if let Some(ref mut headers) = self.headers {
            headers.shift_remove(&name);
        }
        Ok(())
    }

    /// Clear all client-level headers
    #[pyo3(signature = ())]
    pub fn clear_headers(&mut self) -> PyResult<()> {
        self.headers = None;
        Ok(())
    }

    /// Generic request method with full parameter support
    ///
    /// # Arguments
    ///
    /// * `method` - HTTP method (GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS)
    /// * `url` - URL to request
    /// * `params` - Query parameters
    /// * `headers` - HTTP headers
    /// * `cookies` - Cookies to send
    /// * `content` - Raw bytes content
    /// * `data` - Form data (dict/bytes/string)
    /// * `json` - JSON data
    /// * `files` - Files for multipart upload
    /// * `auth` - Basic authentication
    /// * `auth_bearer` - Bearer token authentication
    /// * `timeout` - Request timeout
    /// * `read_timeout` - Read timeout
    /// * `proxy` - Proxy URL
    /// * `impersonate` - Browser to impersonate
    /// * `impersonate_os` - OS to impersonate
    /// * `verify` - Verify SSL certificates
    /// * `ca_cert_file` - CA certificate file
    /// * `follow_redirects` - Follow redirects
    /// * `max_redirects` - Maximum redirects
    /// * `https_only` - HTTPS only
    /// * `http1_only` - HTTP/1.1 only
    /// * `http2_only` - HTTP/2 only
    /// * `split_cookies` - Split cookies into separate headers
    #[pyo3(signature = (method, url, params=None, headers=None, cookies=None, content=None,
        data=None, json=None, files=None, auth=None, auth_bearer=None, timeout=None,
        read_timeout=None, proxy=None, impersonate=None, impersonate_os=None, verify=None,
        ca_cert_file=None, _follow_redirects=None, _max_redirects=None, https_only=None,
        http1_only=None, http2_only=None, split_cookies=None))]
    #[allow(clippy::too_many_arguments)]
    pub fn request(
        &self,
        py: Python,
        method: &str,
        url: &str,
        params: Option<IndexMapSSR>,
        headers: Option<IndexMapSSR>,
        cookies: Option<IndexMapSSR>,
        content: Option<Vec<u8>>,
        data: Option<&Bound<'_, PyAny>>,
        json: Option<&Bound<'_, PyAny>>,
        files: Option<IndexMapSSR>,
        auth: Option<(String, Option<String>)>,
        auth_bearer: Option<String>,
        timeout: Option<f64>,
        read_timeout: Option<f64>,
        proxy: Option<String>,
        impersonate: Option<String>,
        impersonate_os: Option<String>,
        verify: Option<bool>,
        ca_cert_file: Option<String>,
        _follow_redirects: Option<bool>,
        _max_redirects: Option<usize>,
        https_only: Option<bool>,
        http1_only: Option<bool>,
        http2_only: Option<bool>,
        split_cookies: Option<bool>,
    ) -> PyResult<Response> {
        // Parse method
        let method = match method.to_uppercase().as_str() {
            "GET" => Method::GET,
            "POST" => Method::POST,
            "PUT" => Method::PUT,
            "DELETE" => Method::DELETE,
            "PATCH" => Method::PATCH,
            "HEAD" => Method::HEAD,
            "OPTIONS" => Method::OPTIONS,
            _ => {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("Invalid HTTP method: {}", method)
                ))
            }
        };

        let is_post_put_patch = matches!(method, Method::POST | Method::PUT | Method::PATCH);

        // Determine if we need a temporary client
        let need_temp_client = impersonate.is_some()
            || impersonate_os.is_some()
            || verify.is_some()
            || ca_cert_file.is_some()
            || https_only.is_some()
            || http1_only.is_some()
            || http2_only.is_some();

        // Handle data parameter - support bytes, dict/json types, and strings
        let mut data_bytes: Option<Vec<u8>> = None;
        let mut data_value: Option<Value> = None;

        if let Some(data_param) = data {
            // Check if data is bytes
            if let Ok(bytes) = data_param.extract::<Vec<u8>>() {
                data_bytes = Some(bytes);
            }
            // Check if data is a string (send as-is, don't parse)
            else if let Ok(string_data) = data_param.extract::<String>() {
                data_bytes = Some(string_data.into_bytes());
            }
            // Otherwise try to deserialize as JSON value (dict, list, etc.)
            else {
                data_value = Some(depythonize(data_param)
                    .map_err(|e| PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                        format!("Failed to parse data: {}", e)
                    ))?);
            }
        }

        let json_value: Option<Value> = json.map(depythonize).transpose()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyTypeError, _>(
                format!("Failed to parse json: {}", e)
            ))?;

        let params = params.or_else(|| self.params.clone());
        let auth = auth.or(self.auth.clone());
        let auth_bearer = auth_bearer.or(self.auth_bearer.clone());

        // Determine effective settings
        let effective_split_cookies = split_cookies.or(self.split_cookies);
        let effective_timeout = timeout.or(self.timeout);
        let effective_proxy = if !need_temp_client {
            proxy.as_ref().cloned().or_else(|| self.proxy.clone())
        } else {
            None
        };

        // Clone client or create temporary one
        let client = if need_temp_client {
            self.create_temp_client(
                impersonate,
                impersonate_os,
                verify,
                ca_cert_file,
                https_only,
                http1_only,
                http2_only,
                proxy,
                timeout,
            )?
        } else {
            Arc::clone(&self.client)
        };

        // Check if user explicitly set Content-Type to application/json
        let content_type_is_json = headers.as_ref()
            .and_then(|h| h.get("content-type"))
            .or_else(|| headers.as_ref().and_then(|h| h.get("Content-Type")))
            .map(|s| s.to_lowercase().contains("application/json"))
            .unwrap_or(false);

        // Clone client-level headers for use in async block
        let client_headers = self.headers.clone();

        // Execute request asynchronously with GIL release
        let future = async move {
            // Create request builder
            let mut request_builder = client.lock().unwrap().request(method, url);

            // Params
            if let Some(params) = params {
                request_builder = request_builder.query(&params);
            }

            // ===== Enhanced Header Processing with Order Control =====
            // Using OrigHeaderMap for precise header ordering (anti-detection)
            // Using HeaderMap for efficient header storage with insert (override) behavior

            use wreq::header::{HeaderMap, HeaderValue, OrigHeaderMap};

            // Step 1: Collect all user headers into a HeaderMap (insert = override, not append)
            let mut user_headermap = HeaderMap::new();

            // Apply client-level headers first
            if let Some(ref client_hdrs) = client_headers {
                for (key, value) in client_hdrs.iter() {
                    if let (Ok(header_name), Ok(header_value)) = (
                        key.parse::<wreq::header::HeaderName>(),
                        value.parse::<HeaderValue>()
                    ) {
                        user_headermap.insert(header_name, header_value);  // insert = override
                    }
                }
            }

            // Step 2: Apply request-level headers (override client headers)
            if let Some(ref request_headers) = headers {
                for (key, value) in request_headers.iter() {
                    if let (Ok(header_name), Ok(header_value)) = (
                        key.parse::<wreq::header::HeaderName>(),
                        value.parse::<HeaderValue>()
                    ) {
                        user_headermap.insert(header_name, header_value);  // insert = override
                    }
                }
            }

            // Step 3: Build OrigHeaderMap from user headers order (anti-detection)
            // The order of headers in the user's IndexMap determines the sending order
            // This is critical for evading bot detection that analyzes header ordering
            let mut orig_headers = OrigHeaderMap::new();

            // First add client-level headers in their order
            if let Some(ref client_hdrs) = client_headers {
                for (key, _) in client_hdrs.iter() {
                    orig_headers.insert(key.clone());
                }
            }

            // Then add request-level headers (may override order for duplicates)
            if let Some(ref request_headers) = headers {
                for (key, _) in request_headers.iter() {
                    orig_headers.insert(key.clone());
                }
            }

            // Add cookie at the end if present
            if cookies.is_some() {
                orig_headers.insert("cookie".to_string());
            }

            // Step 4: Apply all user headers at once using insert (override) behavior
            // This ensures user headers completely replace emulation defaults for same names
            request_builder = request_builder.headers(user_headermap);

            // Step 5: Apply header ordering (critical for anti-detection)
            request_builder = request_builder.orig_headers(orig_headers);

            // Step 6: Apply cookies based on split_cookies option
            // HTTP/2 style: multiple separate "cookie" headers (split_cookies=true)
            // HTTP/1.1 style: single merged "Cookie" header (split_cookies=false, default)
            if let Some(cookies_map) = cookies {
                match effective_split_cookies {
                    Some(true) => {
                        // Split mode: add each cookie as separate header (HTTP/2 browser behavior)
                        // Use multiple .header() calls - some implementations allow this for same header name
                        for (key, value) in cookies_map.iter() {
                            let cookie_string = format!("{}={}", key, value);
                            // Note: wreq may internally append headers with the same name
                            request_builder = request_builder.header("cookie", cookie_string.as_str());
                        }
                    }
                    Some(false) | None => {
                        // Merged mode: single Cookie header (HTTP/1.1 standard)
                        let cookie_string: String = cookies_map
                            .iter()
                            .map(|(k, v)| format!("{}={}", k, v))
                            .collect::<Vec<_>>()
                            .join("; ");
                        request_builder = request_builder.header(wreq::header::COOKIE, cookie_string);
                    }
                }
            }

            // Body data (only for POST/PUT/PATCH)
            if is_post_put_patch {
                // Content (raw bytes from content parameter)
                if let Some(content) = content {
                    request_builder = request_builder.body(content);
                }
                // Data as bytes (raw bytes from data parameter)
                else if let Some(data_bytes) = data_bytes {
                    request_builder = request_builder.body(data_bytes);
                }
                // Smart handling of data and json parameters
                else if content_type_is_json {
                    // When Content-Type is application/json, prefer json parameter, fallback to data
                    if let Some(json_data) = json_value {
                        request_builder = request_builder.json(&json_data);
                    } else if let Some(form_data) = data_value {
                        request_builder = request_builder.json(&form_data);
                    }
                } else {
                    // No explicit Content-Type: application/json header
                    // json parameter -> JSON encoding
                    // data parameter -> form encoding (or JSON if contains complex types)
                    if let Some(json_data) = json_value {
                        request_builder = request_builder.json(&json_data);
                    } else if let Some(form_data) = data_value {
                        // Check if data contains complex types (arrays/objects) that can't be form-encoded
                        let has_complex_type = form_data.as_object().map_or(false, |obj| {
                            obj.values().any(|v| v.is_array() || v.is_object())
                        });

                        if has_complex_type {
                            // Use JSON encoding for complex types
                            request_builder = request_builder.json(&form_data);
                        } else {
                            // Use form encoding for simple key-value pairs
                            request_builder = request_builder.form(&form_data);
                        }
                    }
                }

                // Files (multipart upload)
                if let Some(_files) = files {
                    // TODO: Implement multipart file upload
                    // This requires tokio::fs and multipart support
                    return Err(anyhow::anyhow!("File upload not yet implemented"));
                }
            }

            // Auth
            if let Some((username, password)) = auth {
                request_builder = request_builder.basic_auth(&username, password.as_deref());
            } else if let Some(token) = auth_bearer {
                request_builder = request_builder.bearer_auth(&token);
            }

            // Timeout (request-level override)
            if let Some(seconds) = effective_timeout {
                request_builder = request_builder.timeout(Duration::from_secs_f64(seconds));
            }

            // Read timeout (request-level)
            if let Some(seconds) = read_timeout {
                request_builder = request_builder.read_timeout(Duration::from_secs_f64(seconds));
            }

            // Proxy (request-level override for non-temp clients)
            if let Some(prx) = effective_proxy {
                request_builder = request_builder.proxy(wreq::Proxy::all(&prx)?);
            }

            // Send the request and await the response
            let resp = request_builder.send().await?;
            Ok::<wreq::Response, anyhow::Error>(resp)
        };

        // Execute async future, releasing the Python GIL for concurrency
        let wreq_response = py.detach(|| RUNTIME.block_on(future))
            .map_err(anyhow_to_pyerr)?;

        // Convert to Python Response
        Ok(Response::from_wreq_response(wreq_response))
    }
}

impl RClient {
    /// Create a temporary client with request-specific settings
    fn create_temp_client(
        &self,
        impersonate: Option<String>,
        impersonate_os: Option<String>,
        verify: Option<bool>,
        ca_cert_file: Option<String>,
        https_only: Option<bool>,
        http1_only: Option<bool>,
        http2_only: Option<bool>,
        proxy: Option<String>,
        timeout: Option<f64>,
    ) -> PyResult<Arc<Mutex<wreq::Client>>> {
        let mut client_builder = wreq::Client::builder();

        // Browser impersonation
        let imp = impersonate.or_else(|| self.impersonate.clone());
        if let Some(browser) = &imp {
            let emulation = map_browser_to_emulation(browser).map_err(anyhow_to_pyerr)?;

            let imp_os = impersonate_os.or_else(|| self.impersonate_os.clone());
            if let Some(os) = &imp_os {
                let emulation_os = map_os_to_emulation_os(os).map_err(anyhow_to_pyerr)?;
                let emulation_option = wreq_util::EmulationOption::builder()
                    .emulation(emulation)
                    .emulation_os(emulation_os)
                    .build();
                client_builder = client_builder.emulation(emulation_option.emulation());
            } else {
                client_builder = client_builder.emulation(emulation);
            }
        }

        // Cookie store
        if self.cookie_store.unwrap_or(true) {
            client_builder = client_builder.cookie_store(true);
        }

        // Referer
        if self.referer.unwrap_or(true) {
            client_builder = client_builder.referer(true);
        }

        // Proxy
        let req_proxy = proxy.or_else(|| self.proxy.clone())
            .or_else(|| std::env::var("PRIMP_PROXY").ok());
        if let Some(proxy_url) = &req_proxy {
            let proxy = wreq::Proxy::all(proxy_url)
                .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(e.to_string()))?;
            client_builder = client_builder.proxy(proxy);
        }

        // Timeout
        let req_timeout = timeout.or(self.timeout);
        if let Some(seconds) = req_timeout {
            client_builder = client_builder.timeout(Duration::from_secs_f64(seconds));
        }

        // Verify
        let req_verify = verify.or(self.verify);
        if let Some(req_ca_cert_file) = &ca_cert_file {
            unsafe {
                std::env::set_var("PRIMP_CA_BUNDLE", req_ca_cert_file);
            }
        }
        if !req_verify.unwrap_or(true) {
            client_builder = client_builder.cert_verification(false);
        } else if let Some(cert_store) = crate::utils::load_ca_certs() {
            client_builder = client_builder.cert_store(cert_store.clone());
        }

        // HTTPS only
        let req_https_only = https_only.or(self.https_only);
        if req_https_only.unwrap_or(false) {
            client_builder = client_builder.https_only(true);
        }

        // HTTP version control
        let req_http1_only = http1_only.or(self.http1_only);
        let req_http2_only = http2_only.or(self.http2_only);
        if req_http1_only.unwrap_or(false) {
            // Force HTTP/1.1 only (if wreq supports this API)
            // client_builder = client_builder.http1_only();
        } else if req_http2_only.unwrap_or(false) {
            client_builder = client_builder.http2_only();
        }

        // Redirect settings
        if self.follow_redirects.unwrap_or(true) {
            client_builder = client_builder
                .redirect(wreq::redirect::Policy::limited(self.max_redirects.unwrap_or(20)));
        } else {
            client_builder = client_builder.redirect(wreq::redirect::Policy::none());
        }

        // Build client
        let client = client_builder
            .build()
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string()))?;

        Ok(Arc::new(Mutex::new(client)))
    }
}
