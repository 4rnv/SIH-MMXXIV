import requests
import threading
import queue

TARGET_URL = "https://threads.net"  # Target URL
WORDLIST_FILE = "apiendpoints.txt"  
THREAD_COUNT = 10                   
TIMEOUT = 5                         
VALID_STATUS_CODES = [200, 201, 204]

api_queue = queue.Queue()

def load_wordlist(wordlist_file):
    with open(wordlist_file, 'r') as f:
        for line in f:
            endpoint = line.strip()
            if endpoint:
                api_queue.put(endpoint)

def brute_force_api_endpoint():
    while not api_queue.empty():
        endpoint = api_queue.get()
        url = f"{TARGET_URL}/{endpoint}"
        
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code in VALID_STATUS_CODES:
                print(f"[+] Found API endpoint: {url} (Status: {response.status_code})")
            elif response.status_code == 403:
                print(f"[-] Forbidden endpoint (403): {url}")
            else:
                print(f"[-] Not valid: {url} (Status: {response.status_code})")
        except requests.RequestException as e:
            print(f"[!] Error accessing {url}: {e}")
        finally:
            api_queue.task_done()

def start_brute_forcing():
    print(f"Starting API endpoint brute force attack on: {TARGET_URL}")
    load_wordlist(WORDLIST_FILE)
    
    threads = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=brute_force_api_endpoint)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    print("API endpoint brute force attack completed.")

if __name__ == "__main__":
    start_brute_forcing()
