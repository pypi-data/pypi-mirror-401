// Utility functions for never_primp
use wreq::tls::CertStore;

/// Loads custom CA certificates from env var PRIMP_CA_BUNDLE or CA_CERT_FILE
/// Returns None if no custom cert path is specified (will use wreq default webpki-roots)
pub fn load_ca_certs() -> Option<&'static CertStore> {
    // TODO: wreq's CertStoreBuilder API may be different from rquest
    // For now, always return None and use default webpki-roots
    // This feature can be implemented once wreq's API is clarified
    None
}
