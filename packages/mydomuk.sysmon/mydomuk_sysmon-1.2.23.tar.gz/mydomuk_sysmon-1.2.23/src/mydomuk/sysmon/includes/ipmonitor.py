from .logger import debuglog, errorlog
import urllib.request
import urllib.error
import time
import threading

class IPMonitor:
    enabled = False
    enabledv6 = False
    check_interval = 300           # 5 minutes as default
    _thread: threading.Thread = None

    _sites = [
        "https://4.ident.me",
        "https://api.ipify.org",
        "https://ifconfig.me/ip",
        "https://icanhazip.com",
        "https://ipecho.net/plain"
    ]

    _sitesv6 = [
        "https://api6.ipify.org",
        "https://6.ident.me"
    ]
    _index = 0
    _indexv6 = 0
    _last_check = None
    _last_ip = None
    _last_ipv6 = None

    @classmethod
    def init(cls, sitelist: list[str]):
        cls._sites = []
        cls._sites.extend(sitelist)
        cls._index = 0
        cls._last_check = None

    @classmethod
    def initv6(cls, sitelist: list[str]):
        cls._sitesv6 = []
        cls._sitesv6.extend(sitelist)
        cls._indexv6 = 0
        cls._last_check = None

    @classmethod
    def _get_next_site(cls) -> str:
        site = cls._sites[cls._index]
        # Cycle index for the next call
        cls._index = (cls._index + 1) % len(cls._sites)
        return site

    @classmethod
    def _get_next_sitev6(cls) -> str:
        site = cls._sitesv6[cls._indexv6]
        # Cycle index for the next call
        cls._indexv6 = (cls._indexv6 + 1) % len(cls._sitesv6)
        return site

    @classmethod
    def fetch_ipv4(cls) -> str:
        return cls._last_ip
    
    @classmethod
    def fetch_ipv6(cls) -> str:
        return cls._last_ipv6

    @classmethod
    def start_ip_fetching(cls) -> None:
        cls._last_ip, cls._last_ipv6 = cls._fetch_ip_addresses()
        cls._thread = threading.Thread(target=cls.fetch_ip_loop, daemon=True)
        cls._thread.start()

    @classmethod
    def fetch_ip_loop(cls) -> None:
        while True:
            time.sleep(cls.check_interval)
            ipv4, ipv6 = cls._fetch_ip_addresses()
            debuglog(f"IPv4 : {ipv4}, IPv6 : {ipv6}")
            cls._last_ip = ipv4
            cls._last_ipv6 = ipv6

    @classmethod
    def _fetch_ip_addresses(cls):
        # Try up to the number of sites available in case of consecutive failures
        ipv4 = "Unknown"
        ipv6 = "Unknown"
        if cls.enabled:
            for _ in range(len(cls._sites)):
                url = cls._get_next_site()
                try:
                    # Short timeout (5s) so your monitor doesn't hang
                    with urllib.request.urlopen(url, timeout=5) as response:
                        ipv4 = response.read().decode('utf8').strip()
                        break
                except (urllib.error.URLError, Exception) as e:
                    errorlog(f"Error querying {url}: {e}")
                    continue  # Try the next site in the list
        if cls.enabledv6:
            for _ in range(len(cls._sitesv6)):
                url = cls._get_next_sitev6()
                try:
                    # Short timeout (5s) so your monitor doesn't hang
                    with urllib.request.urlopen(url, timeout=5) as response:
                        ipv6 = response.read().decode('utf8').strip()
                        break
                except (urllib.error.URLError, Exception) as e:
                    errorlog(f"Error querying {url}: {e}")
                    continue  # Try the next site in the list
        return ipv4, ipv6
