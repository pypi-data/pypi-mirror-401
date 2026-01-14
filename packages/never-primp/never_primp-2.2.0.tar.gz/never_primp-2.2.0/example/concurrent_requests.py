"""High concurrency example using ThreadPoolExecutor"""
import never_primp
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Create client with optimized connection pool
client = never_primp.Client(
    impersonate="chrome",
    timeout=30.0
)

urls = [f"https://www.baidu.com" for _ in range(50)]

def fetch(url):
    """Fetch a single URL"""
    start = time.time()
    try:
        response = client.get(url)
        elapsed = time.time() - start
        return {"status": response.status_code, "time": elapsed}
    except Exception as e:
        elapsed = time.time() - start
        return {"status": "error", "error": str(e), "time": elapsed}

print(f"Fetching {len(urls)} URLs with 25 concurrent workers...")
print("This demonstrates the optimized connection pool (512 connections/host)\n")

start_time = time.time()

with ThreadPoolExecutor(max_workers=25) as executor:
    futures = {executor.submit(fetch, url): url for url in urls}

    results = []
    for future in as_completed(futures):
        result = future.result()
        results.append(result)
        if len(results) % 10 == 0:
            print(f"Completed: {len(results)}/{len(urls)}")

total_time = time.time() - start_time

# Statistics
success_count = sum(1 for r in results if r["status"] == 200)
avg_time = sum(r["time"] for r in results) / len(results)

print(f"\nResults:")
print(f"  Total time: {total_time:.2f}s")
print(f"  Success rate: {success_count}/{len(results)} ({success_count/len(results)*100:.1f}%)")
print(f"  Average request time: {avg_time:.2f}s")
print(f"  Requests/second: {len(results)/total_time:.2f}")
