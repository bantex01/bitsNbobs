import time
import requests
from prometheus_client import start_http_server, Gauge

# Create a Prometheus gauge metric for response time
response_time_metric = Gauge('bbc_website_response_time_seconds', 'Response time of bbc.co.uk website')

# Function to ping the website and measure response time
def ping_website():
    try:
        start_time = time.time()
        response = requests.get('http://www.bbc.co.uk', timeout=5)
        end_time = time.time()

        response_time = end_time - start_time
        response_time_metric.set(response_time)

        print(f"Response time: {response_time} seconds")
    except requests.RequestException as e:
        print(f"Error: {e}")
        response_time_metric.set(0)

if __name__ == "__main__":
    # Start HTTP server for Prometheus metrics
    start_http_server(port=38080)

    # Run the cycle to ping the website and measure response time
    while True:
        ping_website()
        time.sleep(60)  # Adjust the interval as needed (e.g., 60 seconds)
