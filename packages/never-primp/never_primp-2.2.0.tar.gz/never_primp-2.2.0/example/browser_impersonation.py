"""Browser impersonation examples"""
import never_primp

# Test different browsers
browsers = ["chrome", "firefox", "safari", "edge"]

print("Testing browser impersonation:\n")

for browser in browsers:
    try:
        client = never_primp.Client(impersonate=browser)
        response = client.get("https://httpbin.org/headers")
        user_agent = response.json()['headers'].get('User-Agent', 'Unknown')
        print(f"{browser:10} -> {user_agent[:60]}...")
    except Exception as e:
        print(f"{browser:10} -> Error: {e}")

# Test specific versions
print("\n\nTesting specific browser versions:\n")

versions = ["chrome_143", "firefox_146", "safari_26.2", "edge_142"]

for version in versions:
    try:
        client = never_primp.Client(impersonate=version)
        response = client.get("https://httpbin.org/headers")
        user_agent = response.json()['headers'].get('User-Agent', 'Unknown')
        print(f"{version:15} -> {user_agent[:55]}...")
    except Exception as e:
        print(f"{version:15} -> Error: {e}")
