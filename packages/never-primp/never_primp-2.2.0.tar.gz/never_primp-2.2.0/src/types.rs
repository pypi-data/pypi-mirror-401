// Type definitions
use foldhash::fast::RandomState;
use indexmap::IndexMap;

/// IndexMap with String keys and values using fast hash
pub type IndexMapSSR = IndexMap<String, String, RandomState>;
