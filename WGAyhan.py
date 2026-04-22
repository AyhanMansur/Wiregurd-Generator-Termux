# CopyRight = DDos Atack
import os
import sys
import random
import subprocess
import re
from datetime import datetime

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_logo():
    logo = f"""
{Colors.HEADER}{Colors.BOLD}
   _____  _   _  _____  _____  _____  _____  _____ 
  / ____|| | | ||  __ \|  __ \|  __ \|  __ \|  __ \\
 | |    | | | || |  | | |  | | |  | | |  | | |  | |
 | |    | | | || |  | | |  | | |  | | |  | | |  | |
 | |____| |_| || |__| | |__| | |__| | |__| | |__| |
  \_____| \___/ |_____/|_____/|_____/|_____/|_____/ 
{Colors.END}
{Colors.CYAN}   Project: Secret WireGuard Config Generator {Colors.END}
{Colors.YELLOW}   Mode: ArvanCloud & Cloudflare IP Masking {Colors.END}
{Colors.END}
"""
    print(logo)

def get_random_ip_from_ranges():
    """
    انتخاب تصادفی IP از رنج‌های ArvanCloud و Cloudflare
    برای مخفی کردن ترافیک
    """
    arvan_ranges = [
        "185.143.232.0/22", "5.23.1.0/24", "5.23.2.0/24",
        "37.32.0.0/16", "37.32.1.0/24"
    ]
    cloudflare_ranges = [
        "1.1.1.0/24", "1.0.0.0/24", "104.16.0.0/12", "172.64.0.0/13"
    ]
    
    all_ranges = arvan_ranges + cloudflare_ranges
    selected_range = random.choice(all_ranges)
    
    if "1.1.1" in selected_range or "1.0.0" in selected_range:
        ip = f"1.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
    elif "5.23" in selected_range or "37.32" in selected_range:
        ip = f"5.23.{random.randint(1, 254)}.{random.randint(1, 254)}"
    else:
        ip = f"{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
        
    return ip

def get_keys_auto():
    """Generate keys using 'wg' command."""
    try:
        private_key = subprocess.check_output(['wg', 'genkey']).decode().strip()
        # Correct way to get public key from private key
        public_key = subprocess.check_output(['wg', 'pubkey'], input=private_key.encode()).decode().strip()
        return private_key, public_key
    except Exception:
        return None, None

def get_keys_manual():
    """Ask user to input keys manually."""
    print(f"\n{Colors.YELLOW}⚠️ 'wg' tool not found. Please enter your keys manually.{Colors.END}")
    print(f"{Colors.CYAN}   (Make sure there are no spaces at the start or end){Colors.END}")
    
    while True:
        private_key = input(f"{Colors.CYAN}🔑 Enter Private Key: {Colors.END}").strip()
        if private_key and len(private_key) > 20:
            break
        print(f"{Colors.RED}❌ Invalid Private Key. Try again.{Colors.END}")
    
    while True:
        public_key = input(f"{Colors.CYAN}🔑 Enter Public Key: {Colors.END}").strip()
        if public_key and len(public_key) > 20:
            break
        print(f"{Colors.RED}❌ Invalid Public Key. Try again.{Colors.END}")
        
    return private_key, public_key

def ask_save_location():
    """Ask user where to save the config file."""
    print(f"\n{Colors.BOLD}📂 Where do you want to save the config file?{Colors.END}")
    print("1. Save in current folder (Safe & Easy)")
    print("2. Save in Downloads folder (Requires permission)")
    
    while True:
        choice = input(f"{Colors.CYAN}Enter 1 or 2: {Colors.END}").strip()
        if choice == '1':
            return os.getcwd()
        elif choice == '2':
            if os.path.exists("/sdcard"):
                return "/sdcard/Download"
            else:
                print(f"{Colors.RED}⚠️ Storage permission not granted! Run 'termux-setup-storage' first.{Colors.END}")
                print(f"{Colors.YELLOW}   Or choose option 1 to save locally.{Colors.END}")
                continue
        else:
            print(f"{Colors.RED}❌ Invalid choice. Please enter 1 or 2.{Colors.END}")

def create_config(private_key, public_key):
    """Create a clean WireGuard config with ArvanCloud ranges."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"WGAyhan_Arvan_Config_{timestamp}.conf"
    
    config_content = f"""[Interface]
PrivateKey = {private_key}
ListenPort = 443
Address = 185.10.104.0/22
DNS = 1.1.1.1, 9.9.9.9, 178.22.122.100, 178.22.122.101

[Peer]
PublicKey = {public_key}
AllowedIPs = 185.10.104.0/22, 185.10.108.0/22, 5.23.128.0/18
Endpoint = arvancloud.ir:443
PersistentKeepalive = 1
"""
    return filename, config_content

def generate_wireguard_config():
    clear_screen()
    print_logo()
    
    log = lambda msg, color=Colors.GREEN: print(f"{Colors.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {color}{msg}{Colors.END}")
    
    log("🔒 Checking WireGuard tools...", Colors.YELLOW)
    
    # Check if wg is installed
    wg_installed = False
    try:
        subprocess.check_output(['wg', '--version'])
        wg_installed = True
    except (FileNotFoundError, subprocess.CalledProcessError):
        wg_installed = False

    private_key = None
    public_key = None

    if wg_installed:
        log("✅ 'wg' tool found. Generating keys automatically...", Colors.GREEN)
        private_key, public_key = get_keys_auto()
        
        if not private_key:
            log("❌ Failed to generate keys automatically. Switching to manual mode.", Colors.YELLOW)
            private_key, public_key = get_keys_manual()
    else:
        log("⚠️ 'wg' tool NOT found. Switching to manual key input mode...", Colors.YELLOW)
        private_key, public_key = get_keys_manual()

    if not private_key or not public_key:
        log("❌ Critical Error: Could not obtain keys. Exiting.", Colors.RED)
        return

    log("🔒 Generating Secure WireGuard Config...", Colors.YELLOW)
    
    # Get random IP for display (optional, but keeps the logic from your script)
    server_ip = get_random_ip_from_ranges()
    server_port = random.choice([443, 80, 8443])
    
    filename, config_content = create_config(private_key, public_key)
    
    save_path = ask_save_location()
    
    try:
        full_path = os.path.join(save_path, filename)
        
        # Create directory if needed
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        with open(full_path, 'w') as f:
            f.write(config_content)
        
        log(f"✅ Config generated successfully: {filename}", Colors.GREEN)
        log(f"📂 File saved to: {full_path}", Colors.CYAN)
        log(f"🔑 Private Key: {private_key[:10]}...", Colors.YELLOW)
        log(f"🔒 Endpoint: arvancloud.ir:443", Colors.GREEN)
        
        print(f"\n{Colors.BOLD}--- Content of {filename} ---{Colors.END}")
        print(config_content)
        
    except Exception as e:
        log(f"❌ Error saving file: {e}", Colors.RED)

if __name__ == "__main__":
    try:
        generate_wireguard_config()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Script interrupted by user.{Colors.END}")
        sys.exit(0)
