import requests
import time
import random
import socket
import os
import sys
from concurrent.futures import ThreadPoolExecutor
import argparse
import dns.resolver
from urllib.parse import urlparse

def set_small_window():
    try:
        if os.name == 'nt':
            os.system('mode con: cols=70 lines=20')
        else:
            sys.stdout.write("\x1b[8;20;70t")
            sys.stdout.flush()
    except:
        pass

set_small_window()

try:
    from colorama import init, Fore, Style
    init()
    COLOR_SUPPORT = True
except ImportError:
    COLOR_SUPPORT = False
    class DummyFore:
        def __getattr__(self, name):
            return ""
    class DummyStyle:
        def __getattr__(self, name):
            return ""
    Fore = DummyFore()
    Style = DummyStyle()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.104 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.87 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0",
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"
]

def get_status_color(status_code):
    if status_code == 200:
        return Fore.YELLOW
    elif status_code == 404:
        return Fore.GREEN
    elif status_code == 429:
        return Fore.RED
    elif 200 <= status_code < 300:
        return Fore.CYAN
    elif 300 <= status_code < 400:
        return Fore.BLUE
    elif 400 <= status_code < 500:
        return Fore.MAGENTA
    elif 500 <= status_code < 600:
        return Fore.RED
    else:
        return Fore.WHITE

def validate_url(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
    
    try:
        parsed = urlparse(url)
        if not parsed.netloc:
            return None, "Invalid URL: No domain specified"
        
        if len(parsed.netloc) <= 1:
            return None, "Invalid URL: Domain too short"
            
        return url, None
    except Exception as e:
        return None, f"URL parsing error: {str(e)}"

def check_dns(domain):
    try:
        socket.gethostbyname(domain)
        return True, f"{Fore.GREEN}Domain resolved successfully using system DNS{Style.RESET_ALL}"
    except socket.gaierror:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = ['8.8.8.8', '8.8.4.4']
            resolver.resolve(domain, 'A')
            return True, f"{Fore.YELLOW}Domain resolved using Google DNS (but not system DNS){Style.RESET_ALL}"
        except Exception as e:
            return False, f"{Fore.RED}DNS resolution failed: {str(e)}{Style.RESET_ALL}"

def send_request(url, request_num, total_requests):
    try:
        valid_url, error = validate_url(url)
        if not valid_url:
            print(f"{Fore.RED}Request {request_num}/{total_requests} failed: Invalid URL - {error}{Style.RESET_ALL}")
            return False, None
            
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(valid_url, headers=headers, timeout=10, allow_redirects=True)
        
        status_color = get_status_color(response.status_code)
        
        print(f"Request {request_num}/{total_requests} sent! Status code: {status_color}{response.status_code}{Style.RESET_ALL}")
        return True, response.status_code
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Request {request_num}/{total_requests} failed: {str(e)}{Style.RESET_ALL}")
        return False, None

def get_valid_int_input(prompt, min_val, max_val, default_val):
    while True:
        try:
            user_input = input(f"{prompt} [{default_val}]: ").strip()
            if not user_input:
                return default_val
            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"{Fore.YELLOW}Please enter a value between {min_val} and {max_val}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    parser = argparse.ArgumentParser(description="Send multiple requests to a URL (especially grabify links)")
    parser.add_argument("--url", help="Target URL (if not provided, will prompt for input)")
    parser.add_argument("--count", type=int, help="Number of requests to send")
    parser.add_argument("--threads", type=int, help="Number of concurrent threads")
    parser.add_argument("--delay", type=float, help="Delay between requests in seconds")
    
    args = parser.parse_args()
    
    clear_screen()
    
    if not COLOR_SUPPORT:
        print("Note: Install 'colorama' package for colored output (pip install colorama)")
    
    print(f"{Fore.RED}=" * 60)
    print(f"{Fore.RED}G R A B I F Y   F U C K E R{Style.RESET_ALL}")
    print(f"{Fore.RED}=" * 60 + f"{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Flood IP grabbers and tracking links with fake requests{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Supports: grabify.link, iplogger.org, screensnaps.top, etc.{Style.RESET_ALL}")
    print()
    
    target_url = args.url
    if not target_url:
        target_url = input(f"{Fore.CYAN}Enter the grabify/tracking URL: {Style.RESET_ALL}")
    
    valid_url, error_message = validate_url(target_url)
    if not valid_url:
        print(f"{Fore.RED}Error: {error_message}{Style.RESET_ALL}")
        return
        
    target_url = valid_url
    print(f"Target URL: {Fore.CYAN}{target_url}{Style.RESET_ALL}")
    
    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc
    
    print(f"\nChecking DNS resolution for {Fore.CYAN}{domain}{Style.RESET_ALL}...")
    can_resolve, dns_message = check_dns(domain)
    print(dns_message)
    
    if not can_resolve:
        print(f"\n{Fore.RED}WARNING: The domain cannot be resolved. The requests will likely fail.{Style.RESET_ALL}")
        proceed = input("Do you want to proceed anyway? (y/n): ").lower()
        if proceed != 'y':
            print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
            return
    
    MAX_REQUESTS = 70
    if args.count is not None:
        num_requests = min(args.count, MAX_REQUESTS)
        if args.count > MAX_REQUESTS:
            print(f"{Fore.YELLOW}Request count limited to maximum of {MAX_REQUESTS}{Style.RESET_ALL}")
    else:
        num_requests = get_valid_int_input(
            f"How many requests would you like to send? (MAX {MAX_REQUESTS})",
            1, MAX_REQUESTS, 20
        )
    
    if args.threads is not None:
        num_threads = min(args.threads, num_requests)
    else:
        max_threads = min(20, num_requests)
        num_threads = get_valid_int_input(
            f"How many concurrent threads? (1-{max_threads})",
            1, max_threads, min(5, num_requests)
        )
    
    if args.delay is not None:
        delay = args.delay
    else:
        delay = get_valid_int_input(
            "Delay between requests in milliseconds (0-1000)",
            0, 1000, 200
        ) / 1000.0
    
    clear_screen()
    
    print(f"{Fore.RED}=" * 60)
    print(f"{Fore.RED}ATTACK CONFIGURATION:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Target URL: {Style.RESET_ALL}{target_url}")
    print(f"{Fore.CYAN}Number of requests: {Style.RESET_ALL}{num_requests}")
    print(f"{Fore.CYAN}Concurrent threads: {Style.RESET_ALL}{num_threads}")
    print(f"{Fore.CYAN}Delay between requests: {Style.RESET_ALL}{delay:.3f} seconds")
    print(f"{Fore.CYAN}Status code colors:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}200 OK{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}404 Not Found{Style.RESET_ALL}")
    print(f"  {Fore.RED}429 Too Many Requests{Style.RESET_ALL}")
    print(f"{Fore.RED}=" * 60 + f"{Style.RESET_ALL}")
    
    confirm = input(f"\n{Fore.YELLOW}Ready to start flooding the target. Continue? (y/n): {Style.RESET_ALL}").lower()
    if confirm != 'y':
        print(f"{Fore.YELLOW}Operation cancelled.{Style.RESET_ALL}")
        return
    
    clear_screen()
    
    print(f"{Fore.RED}=" * 60)
    print(f"{Fore.RED}G R A B I F Y   F U C K E R{Style.RESET_ALL}")
    print(f"{Fore.RED}=" * 60 + f"{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Starting attack... Press {Fore.YELLOW}Ctrl+C{Style.RESET_ALL}{Fore.GREEN} to stop at any time{Style.RESET_ALL}\n")
    
    successful_requests = 0
    status_counts = {}
    start_time = time.time()
    
    try:
        url_list = [target_url] * num_requests
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = []
            for i in range(1, num_requests + 1):
                future = executor.submit(send_request, url_list[i-1], i, num_requests)
                futures.append(future)
                time.sleep(delay)
            
            for future in futures:
                result, status_code = future.result()
                if result:
                    successful_requests += 1
                    if status_code:
                        status_counts[status_code] = status_counts.get(status_code, 0) + 1
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{Fore.RED}=" * 60)
        print(f"{Fore.GREEN}ATTACK COMPLETED!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target: {Style.RESET_ALL}{target_url}")
        print(f"{Fore.CYAN}Successful requests: {Style.RESET_ALL}{successful_requests}/{num_requests} ({successful_requests/num_requests*100:.1f}%)")
        
        if status_counts:
            print(f"{Fore.CYAN}Status code distribution:{Style.RESET_ALL}")
            for status, count in sorted(status_counts.items()):
                status_color = get_status_color(status)
                print(f"  {status_color}{status}{Style.RESET_ALL}: {count} requests")
        
        print(f"{Fore.CYAN}Total time: {Style.RESET_ALL}{elapsed_time:.2f} seconds")
        print(f"{Fore.CYAN}Average rate: {Style.RESET_ALL}{num_requests/elapsed_time:.2f} requests/second")
        print(f"{Fore.RED}=" * 60 + f"{Style.RESET_ALL}")
        
    except KeyboardInterrupt:
        elapsed_time = time.time() - start_time
        print(f"\n{Fore.RED}=" * 60)
        print(f"\n{Fore.YELLOW}Attack interrupted by user.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Sent approximately {successful_requests} successful requests{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Elapsed time: {Style.RESET_ALL}{elapsed_time:.2f} seconds")
        print(f"{Fore.RED}=" * 60 + f"{Style.RESET_ALL}")
    
if __name__ == "__main__":
    main()
