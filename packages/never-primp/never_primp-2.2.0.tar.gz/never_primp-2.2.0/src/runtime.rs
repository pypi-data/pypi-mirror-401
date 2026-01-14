// Global Tokio runtime management
use std::sync::LazyLock;
use tokio::runtime::Runtime;

/// Global multi-threaded Tokio runtime for handling async operations
/// Uses 4 worker threads to support better concurrency for large-scale crawling
pub static RUNTIME: LazyLock<Runtime> = LazyLock::new(|| {
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .worker_threads(4)
        .thread_name("never-primp-worker")
        .build()
        .expect("Failed to create Tokio runtime")
});
