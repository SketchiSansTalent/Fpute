import requests
import time
from concurrent.futures import ThreadPoolExecutor
import string
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    print(rf"""{Fore.MAGENTA}
▀█████████▄  ▄██   ▄           ▄████████    ▄█   ▄█▄    ▄████████     ███      ▄████████    ▄█    █▄     ▄█  
  ███    ███ ███   ██▄        ███    ███   ███ ▄███▀   ███    ███ ▀█████████▄ ███    ███   ███    ███   ███  
  ███    ███ ███▄▄▄███        ███    █▀    ███▐██▀     ███    █▀     ▀███▀▀██ ███    █▀    ███    ███   ███▌ 
 ▄███▄▄▄██▀  ▀▀▀▀▀▀███        ███         ▄█████▀     ▄███▄▄▄         ███   ▀ ███         ▄███▄▄▄▄███▄▄ ███▌ 
▀▀███▀▀▀██▄  ▄██   ███      ▀███████████ ▀▀█████▄    ▀▀███▀▀▀         ███     ███        ▀▀███▀▀▀▀███▀  ███▌ 
  ███    ██▄ ███   ███               ███   ███▐██▄     ███    █▄      ███     ███    █▄    ███    ███   ███  
  ███    ███ ███   ███         ▄█    ███   ███ ▀███▄   ███    ███     ███     ███    ███   ███    ███   ███  
▄█████████▀   ▀█████▀        ▄████████▀    ███   ▀█▀   ██████████    ▄████▀   ████████▀    ███    █▀    █▀   
                                           ▀                                                                 
        {Style.RESET_ALL}""")
    print(f"{Fore.CYAN}[ + ]If you need help or have a question (add me on discord)-> sketchi_i{Style.RESET_ALL}")
    print(f"       {Fore.YELLOW}v1.0.1-dev{Style.RESET_ALL}")
    print(f"{Fore.GREEN}_" * 50)
    print(f"\n {Fore.BLUE}:: Method           : GET")
    print(f" {Fore.BLUE}:: Follow redirects : false")
    print(f" {Fore.BLUE}:: Timeout          : 10")
    print(f" {Fore.BLUE}:: Threads          : 40")
    print(f" {Fore.BLUE}:: Matcher          : Response status: 200-299,301,302,307,401,403,405,500")
    print(f"{Fore.GREEN}_" * 50)
    print()

def test_url(base_url, word, status_codes):
    url = f"{base_url}/{word}"
    try:
        response = requests.get(url, timeout=10, allow_redirects=False)
        if response.status_code in status_codes:
            size = len(response.content)
            words = len(response.text.split())
            lines = response.text.count('\n')
            print(f"{Fore.GREEN}[Status: {response.status_code}, Size: {size}, Words: {words}, Lines: {lines}] {url}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[Error] {url}: {e}{Style.RESET_ALL}")

def generate_wordlist():
    chars = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    return [char for char in chars]

def main():
    banner()
    base_url = input(f"{Fore.CYAN}Enter the basic URL (ex: https://example.com): {Style.RESET_ALL}").strip()
    wordlist_choice = input(f"{Fore.CYAN}Do you want to use a already existing wordlists (O/N) ? {Style.RESET_ALL}").strip().lower()
    threads = int(input(f"{Fore.CYAN}Number of threads (ex: 40): {Style.RESET_ALL}").strip())
    status_codes = {200, 301, 302, 307, 401, 403, 405, 500}

    if wordlist_choice == 'o':
        wordlist_path = input(f"{Fore.CYAN}Enther the PATH to the wordlist (ex: wordlist.txt): {Style.RESET_ALL}").strip()
        try:
            with open(wordlist_path, 'r', encoding='utf-8') as file:
                words = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"{Fore.RED}Erreur: File '{wordlist_path}' not found.{Style.RESET_ALL}")
            return
        except UnicodeDecodeError:
            print(f"{Fore.RED}Erreur: The file '{wordlist_path}' contain invalid character.{Style.RESET_ALL}")
            return
    else:
        words = generate_wordlist()

    print(f"\n{Fore.CYAN}:: Starting the scan with {len(words)} words in the wordlist...\n{Style.RESET_ALL}")

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(test_url, base_url, word, status_codes) for word in words]

    for future in futures:
        future.result()

    duration = time.time() - start_time
    print(f"\n{Fore.CYAN}:: Scan ended in {duration:.2f} secondes.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
