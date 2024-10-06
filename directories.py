import requests
import threading
import queue
import sys

TARGET_URL = "https://xyz.neocities.org"  # Target URL
WORDLIST_FILE = "wordlist.txt"
THREAD_COUNT = 10
TIMEOUT = 5
found_directories_list = []

dir_queue = queue.Queue()

def load_wordlist(wordlist_file):
    with open(wordlist_file, 'r') as f:
        for line in f:
            directory = line.strip()
            if directory:
                dir_queue.put(directory)

def brute_force_directory():
    while not dir_queue.empty():
        directory = dir_queue.get()
        url = f"{TARGET_URL}/{directory}"
        try:
            response = requests.get(url, timeout=TIMEOUT)
            if response.status_code == 200:
                print(f"[+] Found directory: {url}")
                found_directories_list.append(directory)
            elif response.status_code == 403:
                print(f"[-] Forbidden directory (403): {url}")
            elif response.status_code == 404:
                print(f"[-] Directory does not exist (404): {url}")
        except requests.RequestException as e:
            print(f"[!] Error accessing {url}: {e}")
        finally:
            dir_queue.task_done()
    print(found_directories_list)

def start_brute_forcing():
    print(f"Starting directory brute force attack on: {TARGET_URL}")
    load_wordlist(WORDLIST_FILE)

    threads = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=brute_force_directory)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    print("Brute force attack completed.")

if __name__ == "__main__":
    start_brute_forcing()
