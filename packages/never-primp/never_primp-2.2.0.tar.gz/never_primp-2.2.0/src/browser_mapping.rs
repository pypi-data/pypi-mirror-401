// Browser name mapping (Python → wreq_util::Emulation)
use anyhow::{anyhow, Result};
use wreq_util::{Emulation, EmulationOS};

/// Map Python browser name to wreq_util::Emulation enum
///
/// Supports specific versions (e.g., "chrome_131") and generic names (e.g., "chrome")
pub fn map_browser_to_emulation(name: &str) -> Result<Emulation> {
    match name.to_lowercase().as_str() {
        // Chrome versions
        "chrome_100" => Ok(Emulation::Chrome100),
        "chrome_101" => Ok(Emulation::Chrome101),
        "chrome_104" => Ok(Emulation::Chrome104),
        "chrome_105" => Ok(Emulation::Chrome105),
        "chrome_106" => Ok(Emulation::Chrome106),
        "chrome_107" => Ok(Emulation::Chrome107),
        "chrome_108" => Ok(Emulation::Chrome108),
        "chrome_109" => Ok(Emulation::Chrome109),
        "chrome_110" => Ok(Emulation::Chrome110),
        "chrome_114" => Ok(Emulation::Chrome114),
        "chrome_116" => Ok(Emulation::Chrome116),
        "chrome_117" => Ok(Emulation::Chrome117),
        "chrome_118" => Ok(Emulation::Chrome118),
        "chrome_119" => Ok(Emulation::Chrome119),
        "chrome_120" => Ok(Emulation::Chrome120),
        "chrome_123" => Ok(Emulation::Chrome123),
        "chrome_124" => Ok(Emulation::Chrome124),
        "chrome_126" => Ok(Emulation::Chrome126),
        "chrome_127" => Ok(Emulation::Chrome127),
        "chrome_128" => Ok(Emulation::Chrome128),
        "chrome_129" => Ok(Emulation::Chrome129),
        "chrome_130" => Ok(Emulation::Chrome130),
        "chrome_131" => Ok(Emulation::Chrome131),
        "chrome_132" => Ok(Emulation::Chrome132),
        "chrome_133" => Ok(Emulation::Chrome133),
        "chrome_134" => Ok(Emulation::Chrome134),
        "chrome_135" => Ok(Emulation::Chrome135),
        "chrome_136" => Ok(Emulation::Chrome136),
        "chrome_137" => Ok(Emulation::Chrome137),
        "chrome_138" => Ok(Emulation::Chrome138),
        "chrome_139" => Ok(Emulation::Chrome139),
        "chrome_140" => Ok(Emulation::Chrome140),
        "chrome_141" => Ok(Emulation::Chrome141),
        "chrome_142" => Ok(Emulation::Chrome142),
        "chrome_143" => Ok(Emulation::Chrome143),

        // Edge versions
        "edge_101" => Ok(Emulation::Edge101),
        "edge_122" => Ok(Emulation::Edge122),
        "edge_127" => Ok(Emulation::Edge127),
        "edge_131" => Ok(Emulation::Edge131),
        "edge_134" => Ok(Emulation::Edge134),
        "edge_135" => Ok(Emulation::Edge135),
        "edge_136" => Ok(Emulation::Edge136),
        "edge_137" => Ok(Emulation::Edge137),
        "edge_138" => Ok(Emulation::Edge138),
        "edge_139" => Ok(Emulation::Edge139),
        "edge_140" => Ok(Emulation::Edge140),
        "edge_141" => Ok(Emulation::Edge141),
        "edge_142" => Ok(Emulation::Edge142),

        // Opera versions
        "opera_116" => Ok(Emulation::Opera116),
        "opera_117" => Ok(Emulation::Opera117),
        "opera_118" => Ok(Emulation::Opera118),
        "opera_119" => Ok(Emulation::Opera119),

        // Safari versions
        "safari_15.3" | "safari_15_3" => Ok(Emulation::Safari15_3),
        "safari_15.5" | "safari_15_5" => Ok(Emulation::Safari15_5),
        "safari_15.6.1" | "safari_15_6_1" => Ok(Emulation::Safari15_6_1),
        "safari_16" => Ok(Emulation::Safari16),
        "safari_16.5" | "safari_16_5" => Ok(Emulation::Safari16_5),
        "safari_17.0" | "safari_17_0" => Ok(Emulation::Safari17_0),
        "safari_17.2.1" | "safari_17_2_1" => Ok(Emulation::Safari17_2_1),
        "safari_17.4.1" | "safari_17_4_1" => Ok(Emulation::Safari17_4_1),
        "safari_17.5" | "safari_17_5" => Ok(Emulation::Safari17_5),
        "safari_17.6" | "safari_17_6" => Ok(Emulation::Safari17_6),
        "safari_18" => Ok(Emulation::Safari18),
        "safari_18.2" | "safari_18_2" => Ok(Emulation::Safari18_2),
        "safari_18.3" | "safari_18_3" => Ok(Emulation::Safari18_3),
        "safari_18.3.1" | "safari_18_3_1" => Ok(Emulation::Safari18_3_1),
        "safari_18.5" | "safari_18_5" => Ok(Emulation::Safari18_5),
        "safari_26" => Ok(Emulation::Safari26),
        "safari_26.1" | "safari_26_1" => Ok(Emulation::Safari26_1),
        "safari_26.2" | "safari_26_2" => Ok(Emulation::Safari26_2),

        // Safari iOS versions
        "safari_ios_16.5" | "safari_ios_16_5" => Ok(Emulation::SafariIos16_5),
        "safari_ios_17.2" | "safari_ios_17_2" => Ok(Emulation::SafariIos17_2),
        "safari_ios_17.4.1" | "safari_ios_17_4_1" => Ok(Emulation::SafariIos17_4_1),
        "safari_ios_18.1.1" | "safari_ios_18_1_1" => Ok(Emulation::SafariIos18_1_1),
        "safari_ios_26" => Ok(Emulation::SafariIos26),
        "safari_ios_26.2" | "safari_ios_26_2" => Ok(Emulation::SafariIos26_2),

        // Safari iPad versions
        "safari_ipad_18" => Ok(Emulation::SafariIPad18),
        "safari_ipad_26" => Ok(Emulation::SafariIPad26),
        "safari_ipad_26.2" | "safari_ipad_26_2" => Ok(Emulation::SafariIpad26_2),

        // Firefox versions
        "firefox_109" => Ok(Emulation::Firefox109),
        "firefox_117" => Ok(Emulation::Firefox117),
        "firefox_128" => Ok(Emulation::Firefox128),
        "firefox_133" => Ok(Emulation::Firefox133),
        "firefox_135" => Ok(Emulation::Firefox135),
        "firefox_136" => Ok(Emulation::Firefox136),
        "firefox_139" => Ok(Emulation::Firefox139),
        "firefox_142" => Ok(Emulation::Firefox142),
        "firefox_143" => Ok(Emulation::Firefox143),
        "firefox_144" => Ok(Emulation::Firefox144),
        "firefox_145" => Ok(Emulation::Firefox145),
        "firefox_146" => Ok(Emulation::Firefox146),

        // Firefox Private/Android versions
        "firefox_private_135" => Ok(Emulation::FirefoxPrivate135),
        "firefox_private_136" => Ok(Emulation::FirefoxPrivate136),
        "firefox_android_135" => Ok(Emulation::FirefoxAndroid135),

        // OkHttp versions
        "okhttp_3.9" | "okhttp_3_9" => Ok(Emulation::OkHttp3_9),
        "okhttp_3.11" | "okhttp_3_11" => Ok(Emulation::OkHttp3_11),
        "okhttp_3.13" | "okhttp_3_13" => Ok(Emulation::OkHttp3_13),
        "okhttp_3.14" | "okhttp_3_14" => Ok(Emulation::OkHttp3_14),
        "okhttp_4.9" | "okhttp_4_9" => Ok(Emulation::OkHttp4_9),
        "okhttp_4.10" | "okhttp_4_10" => Ok(Emulation::OkHttp4_10),
        "okhttp_4.12" | "okhttp_4_12" => Ok(Emulation::OkHttp4_12),
        "okhttp_5" => Ok(Emulation::OkHttp5),

        // Generic browser names (map to latest stable versions)
        "chrome" => Ok(Emulation::Chrome143),  // Latest Chrome
        "edge" => Ok(Emulation::Edge142),      // Latest Edge
        "opera" => Ok(Emulation::Opera119),    // Latest Opera
        "safari" => Ok(Emulation::Safari26_2), // Latest Safari
        "firefox" => Ok(Emulation::Firefox146), // Latest Firefox
        "okhttp" => Ok(Emulation::OkHttp5),    // Latest OkHttp

        // Unsupported browser
        _ => Err(anyhow!("Unsupported browser: {}. Please use a specific browser version (e.g., 'chrome_143', 'firefox_146', 'safari_26.2') or a generic name ('chrome', 'firefox', 'safari', 'edge', 'opera', 'okhttp').", name))
    }
}

/// Map Python OS name to wreq_util::EmulationOS enum
pub fn map_os_to_emulation_os(os: &str) -> Result<EmulationOS> {
    match os.to_lowercase().as_str() {
        "windows" => Ok(EmulationOS::Windows),
        "macos" | "mac" | "osx" => Ok(EmulationOS::MacOS),
        "linux" => Ok(EmulationOS::Linux),
        "android" => Ok(EmulationOS::Android),
        "ios" | "iphone" | "ipad" => Ok(EmulationOS::IOS),
        _ => Err(anyhow!("Unsupported OS: {}. Please use one of: 'windows', 'macos', 'linux', 'android', 'ios'.", os))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_chrome_mapping() {
        assert!(matches!(map_browser_to_emulation("chrome_143"), Ok(Emulation::Chrome143)));
        assert!(matches!(map_browser_to_emulation("chrome_131"), Ok(Emulation::Chrome131)));
        assert!(matches!(map_browser_to_emulation("chrome"), Ok(Emulation::Chrome143)));
    }

    #[test]
    fn test_firefox_mapping() {
        assert!(matches!(map_browser_to_emulation("firefox_146"), Ok(Emulation::Firefox146)));
        assert!(matches!(map_browser_to_emulation("firefox_136"), Ok(Emulation::Firefox136)));
        assert!(matches!(map_browser_to_emulation("firefox"), Ok(Emulation::Firefox146)));
    }

    #[test]
    fn test_safari_mapping() {
        assert!(matches!(map_browser_to_emulation("safari_26.2"), Ok(Emulation::Safari26_2)));
        assert!(matches!(map_browser_to_emulation("safari_18"), Ok(Emulation::Safari18)));
        assert!(matches!(map_browser_to_emulation("safari"), Ok(Emulation::Safari26_2)));
    }

    #[test]
    fn test_os_mapping() {
        assert!(matches!(map_os_to_emulation_os("windows"), Ok(EmulationOS::Windows)));
        assert!(matches!(map_os_to_emulation_os("macos"), Ok(EmulationOS::MacOS)));
        assert!(matches!(map_os_to_emulation_os("mac"), Ok(EmulationOS::MacOS)));
        assert!(matches!(map_os_to_emulation_os("linux"), Ok(EmulationOS::Linux)));
        assert!(matches!(map_os_to_emulation_os("android"), Ok(EmulationOS::Android)));
        assert!(matches!(map_os_to_emulation_os("ios"), Ok(EmulationOS::IOS)));
    }

    #[test]
    fn test_invalid_browser() {
        assert!(map_browser_to_emulation("invalid_browser").is_err());
    }

    #[test]
    fn test_invalid_os() {
        assert!(map_os_to_emulation_os("invalid_os").is_err());
    }
}
