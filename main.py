import requests
from bs4 import BeautifulSoup
import re
import os
import time
from colorama import Fore, Style, init
import sys

init(autoreset=True)

ascii_art = r'''
 █    ██  ██▓  ▄▄▄█████▓ ██▓ ███▄ ▄███▓ ▄▄▄     ▄▄▄█████▓▓█████
 ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██▒▓██▒▀█▀ ██▒▒████▄   ▓  ██▒ ▓▒▓█   ▀
▓██  ▒██░▒██░  ▒ ▓██░ ▒░▒██▒▓██    ▓██░▒██  ▀█▄ ▒ ▓██░ ▒░▒███
▓▓█  ░██░▒██░  ░ ▓██▓ ░ ░██░▒██    ▒██ ░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄
▒▒█████▓ ░██████▒▒██▒ ░ ░██░▒██▒   ░██▒ ▓█   ▓██▒ ▒██▒ ░ ░▒████▒
░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░▓  ░ ▒░   ░  ░ ▒▒   ▓▒█░ ▒ ░░   ░░ ▒░ ░
░░▒░ ░ ░ ░ ░ ░  ░  ░     ▒ ░░  ░      ░  ▒   ▒▒ ░   ░     ░ ░  ░
 ░░░ ░ ░   ░ ░   ░       ▒ ░░      ░     ░   ▒    ░         ░
   ░         ░  ░        ░         ░         ░  ░           ░  ░
'''

CREDITS = Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "\nMade by @balrampreet1\n"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

proxy_sources = {
    'http': [
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all',
        'https://spys.me/proxy.txt',
        'https://free-proxy-list.net/?c=HTTP',
        'https://www.proxy-list.download/api/v1/get?type=http',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt'
    ],
    'https': [
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
        'https://www.proxy-list.download/api/v1/get?type=https',
        'https://free-proxy-list.net/?c=HTTPS',
    ],
    'socks4': [
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=10000&country=all',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt',
        'https://www.socks-proxy.net/#get',
        'https://www.proxy-list.download/api/v1/get?type=socks4',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt'
    ],
    'socks5': [
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks5&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks5.txt',
        'https://www.socks-proxy.net/',
        'https://www.proxy-list.download/api/v1/get?type=socks5',
        'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt'
    ]
}

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def color_cycle(text):
    # Green gradient: dark green, light green, yellow-green, light green, dark green
    colors = [Fore.GREEN, Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.GREEN]
    result = ""
    for i, char in enumerate(text):
        result += colors[i % len(colors)] + char
    return result + Fore.RESET
def print_banner_animated():
    clear_console()
    for line in ascii_art.splitlines():
        print(color_cycle(line))
        time.sleep(0.03)
    print(CREDITS)


def print_menu():
    print(Fore.YELLOW + Style.BRIGHT + "╔══════════════════════════════════════════════════════════════╗")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.LIGHTBLUE_EX + "      Universal Public Proxy Fetcher                          " + Fore.YELLOW +   "║")
    print(Fore.YELLOW + Style.BRIGHT + "╠══════════════════════════════════════════════════════════════╣")
    print(Fore.YELLOW + Style.BRIGHT + "║" + Fore.LIGHTGREEN_EX + "  [1] HTTP   " + Fore.LIGHTCYAN_EX + "  [2] HTTPS  " + Fore.LIGHTMAGENTA_EX + "  [3] SOCKS4  " + Fore.LIGHTYELLOW_EX + "  [4] SOCKS5          " + Fore.YELLOW + "║")
    print(Fore.YELLOW + Style.BRIGHT + "╚══════════════════════════════════════════════════════════════╝")
    print(Fore.LIGHTBLACK_EX + "Tip: Fetches from multiple public sources and saves to a .txt file.\n")

def progress_bar(current, total, bar_length=32):
    percent = float(current) / total
    arrow = '█' * int(round(percent * bar_length))
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(Fore.LIGHTBLUE_EX + f"\r    Fetching... [{arrow}{spaces}] {int(percent*100)}%")
    sys.stdout.flush()

def fetch_proxies_from_url(url, proxy_type):
    proxies = set()
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            return proxies
        text = resp.text
        # spys.me
        if 'spys.me' in url:
            for line in text.splitlines():
                if re.match(r"^\d+\.\d+\.\d+\.\d+:\d+", line):
                    proxies.add(line.strip())
        # free-proxy-list.net
        elif 'free-proxy-list.net' in url:
            soup = BeautifulSoup(text, 'html.parser')
            table = soup.find('table', {'id': 'proxylisttable'})
            if table:
                for row in table.find_all('tr')[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        ip = cols[0].get_text(strip=True)
                        port = cols[1].get_text(strip=True)
                        if re.match(r"^\d+\.\d+\.\d+\.\d+$", ip) and port.isdigit():
                            proxies.add(f"{ip}:{port}")
        # socks-proxy.net
        elif 'socks-proxy.net' in url:
            soup = BeautifulSoup(text, 'html.parser')
            table = soup.find('table', {'id': 'proxylisttable'})
            if table:
                for row in table.find_all('tr')[1:]:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        ip = cols[0].get_text(strip=True)
                        port = cols[1].get_text(strip=True)
                        if re.match(r"^\d+\.\d+\.\d+\.\d+$", ip) and port.isdigit():
                            proxies.add(f"{ip}:{port}")
        else:
            for line in text.splitlines():
                line = line.strip()
                if line and ':' in line and re.match(r"^\d+\.\d+\.\d+\.\d+:\d+", line):
                    proxies.add(line)
    except Exception as e:
        print(Fore.RED + f"\n    [!] Error fetching from {url}: {e}")
    return proxies

def fetch_all_proxies(proxy_type):
    all_proxies = set()
    sources = proxy_sources.get(proxy_type, [])
    print(Fore.LIGHTYELLOW_EX + f"\nFetching {proxy_type.upper()} proxies from {len(sources)} sources...\n")
    for idx, url in enumerate(sources, 1):
        print(Fore.LIGHTBLUE_EX + f"  [{idx}/{len(sources)}] {url}")
        proxies = fetch_proxies_from_url(url, proxy_type)
        print(Fore.GREEN + f"      {len(proxies)} proxies fetched.")
        all_proxies.update(proxies)
        progress_bar(idx, len(sources))
        time.sleep(0.7)
    print()
    return all_proxies

def print_summary(proxy_type, proxies, filename):
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n╔══════════════════════════════════════════════╗")
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"║  {proxy_type.upper()} proxies fetched: {len(proxies):<24}║")
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"║  Saved to: {filename:<36}║")
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "╚══════════════════════════════════════════════╝\n")

def exit_screen():
    print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "\nThank you for using Universal Public Proxy Fetcher!")
    print(Fore.LIGHTGREEN_EX + "Connect with @balrampreet1 for more cool tools.\n")
    input(Fore.LIGHTBLACK_EX + "Press Enter to exit...")

def main():
    print_banner_animated()
    print_menu()
    choice_map = {'1': 'http', '2': 'https', '3': 'socks4', '4': 'socks5'}
    choice = ''
    while choice not in choice_map:
        choice = input(Fore.CYAN + Style.BRIGHT + "Select proxy type (1-4): ").strip()
        if choice not in choice_map:
            print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, or 4.")
    proxy_type = choice_map[choice]
    proxies = fetch_all_proxies(proxy_type)
    filename = f"{proxy_type}.txt"
    if proxies:
        with open(filename, 'w', encoding='utf-8') as f:
            for proxy in sorted(proxies):
                f.write(proxy + '\n')
        print_summary(proxy_type, proxies, filename)
    else:
        print(Fore.RED + "\n[!] No proxies fetched. Try again later or check your internet connection.\n")
    exit_screen()

if __name__ == '__main__':
    main()
