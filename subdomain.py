import dns.resolver
import threading
import queue

TARGET_DOMAIN = "wikipedia.org"   # Target domain
WORDLIST_FILE = "subdomains.txt"
THREAD_COUNT = 2
TIMEOUT = 5

subdomain_queue = queue.Queue()

def load_wordlist(wordlist_file):
    with open(wordlist_file, 'r') as f:
        for line in f:
            subdomain = line.strip()
            if subdomain:
                subdomain_queue.put(subdomain)

def brute_force_subdomain():
    resolver = dns.resolver.Resolver()
    resolver.timeout = TIMEOUT
    resolver.lifetime = TIMEOUT
    while not subdomain_queue.empty():
        subdomain = subdomain_queue.get()
        full_domain = f"https://{subdomain}.{TARGET_DOMAIN}"
        
        try:
            answers = resolver.resolve(full_domain, 'A')
            print(f"[+] Found subdomain: {full_domain}")
            for rdata in answers:
                print(f"    IP: {rdata}")
        except dns.resolver.NXDOMAIN:
            print(f"[-] Subdomain does not exist: {full_domain}")
        except (dns.exception.Timeout, dns.resolver.NoNameservers) as e:
            print(f"[!] Error with {full_domain}: {e}")
        finally:
            subdomain_queue.task_done()

def start_brute_forcing():
    print(f"Starting subdomain brute force attack on: {TARGET_DOMAIN}")
    
    load_wordlist(WORDLIST_FILE)
    
    threads = []
    for _ in range(THREAD_COUNT):
        thread = threading.Thread(target=brute_force_subdomain)
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()

    print("Subdomain brute force attack completed.")

if __name__ == "__main__":
    start_brute_forcing()
