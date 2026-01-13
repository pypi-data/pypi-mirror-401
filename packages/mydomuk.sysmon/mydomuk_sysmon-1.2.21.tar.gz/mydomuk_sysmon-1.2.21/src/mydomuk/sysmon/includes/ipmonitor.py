from .logger import debuglog, errorlog
import urllib.request
import urllib.error
import time

class IPMonitor:
    enabled = False
    enabledv6 = False
    check_interval = 300           # 5 minutes as default

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
    def get_next_site(cls) -> str:
        site = cls._sites[cls._index]
        # Cycle index for the next call
        cls._index = (cls._index + 1) % len(cls._sites)
        return site

    @classmethod
    def get_next_sitev6(cls) -> str:
        site = cls._sitesv6[cls._indexv6]
        # Cycle index for the next call
        cls._indexv6 = (cls._indexv6 + 1) % len(cls._sitesv6)
        return site

    @classmethod
    def fetch_ipv4(cls):
        if cls.checknow():
            ipv4, _ = cls.fetch_ip()
            return ipv4
        return cls._last_ip
    
    @classmethod
    def fetch_ipv6(cls):
        if cls.checknow():
            _, ipv6 = cls.fetch_ip()
            return ipv6
        return cls._last_ipv6
    
    @classmethod
    def fetch_ip(cls):
        # Try up to the number of sites available in case of consecutive failures
        if cls.enabled:
            for _ in range(len(cls._sites)):
                url = cls.get_next_site()
                try:
                    # Short timeout (5s) so your monitor doesn't hang
                    with urllib.request.urlopen(url, timeout=5) as response:
                        ip = response.read().decode('utf8').strip()
                        if cls._last_ip is not None and cls._last_ip != ip:
                            debuglog(f"Got New IP {ip} from URL : {url}")
                        cls._last_ip = ip
                        break
                except (urllib.error.URLError, Exception) as e:
                    errorlog(f"Error querying {url}: {e}")
                    continue  # Try the next site in the list
        if cls.enabledv6:
            for _ in range(len(cls._sitesv6)):
                url = cls.get_next_sitev6()
                try:
                    # Short timeout (5s) so your monitor doesn't hang
                    with urllib.request.urlopen(url, timeout=5) as response:
                        ip = response.read().decode('utf8').strip()
                        if cls._last_ipv6 is not None and cls._last_ipv6 != ip:
                            debuglog(f"Got New IPV6 {ip} from URL : {url}")
                        cls._last_ipv6 = ip
                        break
                except (urllib.error.URLError, Exception) as e:
                    errorlog(f"Error querying {url}: {e}")
                    continue  # Try the next site in the list
        return cls._last_ip, cls._last_ipv6

    @classmethod
    def checknow(cls) -> bool:
        current_time = time.time()
        if cls._last_check is None:
            cls._last_check = current_time
            return True
        if cls.check_interval < 60:
            checker = 50
        else:
            checker = cls.check_interval - 10
        if current_time - cls._last_check >= checker :
            cls._last_check = current_time
            return True
        return False


# Example usage with your config-style list
##config_sites = [
#  #  'https://ident.me',
#    'https://api.ipify.org',
#    'https://ifconfig.me/ip'
#]

#monitor = IPMonitor(config_sites)

# This would be inside your 1-minute loop
#public_ip = monitor.fetch_ip()
#if public_ip:
#    print(f"Current Public IP: {public_ip}")
#    # Here you would publish to your MQTT broker