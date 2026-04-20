#copyright = DDos Attack 
import os
import subprocess
import random
from datetime import datetime

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e.stderr}")
        return None

def generate_keys():
    print("🔐 Generating secure keys...")
    private_key = run_command("wg genkey")
    if not private_key:
        print("❌ Failed to generate private key. Install wireguard-tools first.")
        return None, None
    
    public_key = run_command(f"echo '{private_key}' | wg pubkey")
    if not public_key:
        print("❌ Failed to generate public key.")
        return None, None
    
    return private_key, public_key

def get_smart_endpoint():
    arvan_ips = [
        "5.23.100.1", "5.23.100.2", "5.23.101.1", "5.23.102.1",
        "185.143.223.1", "185.143.223.2", "185.143.224.1"
    ]
    cloudflare_ips = [
        "1.1.1.1", "1.0.0.1", "1.1.1.2", "1.0.0.2",
        "104.16.132.229", "104.16.133.229", "104.16.134.229"
    ]
    all_ips = arvan_ips + cloudflare_ips
    return random.choice(all_ips)

def ask_save_location():
    """Ask user where to save the config file."""
    print("\n📂 Where do you want to save the config file?")
    print("1. Save in current folder (Safe & Easy)")
    print("2. Save in Downloads folder (Requires permission)")
    
    while True:
        choice = input("Enter 1 or 2: ").strip()
        if choice == '1':
            return os.getcwd()
        elif choice == '2':
            # Check if storage permission is granted
            if os.path.exists("/sdcard"):
                return "/sdcard/Download"
            else:
                print("⚠️  Storage permission not granted! Please run 'termux-setup-storage' first.")
                print("   Or choose option 1 to save locally.")
                continue
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

def create_and_save_config(private_key, public_key, endpoint_ip, save_path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"WGAyhan_Config_{timestamp}.conf"
    full_path = os.path.join(save_path, filename)
    
    config = f"""[Interface]
PrivateKey = {private_key}
Address = 10.0.0.2/32
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = {public_key}
Endpoint = {endpoint_ip}:443
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
"""
    
    try:
        # Create directory if it doesn't exist (for Downloads)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        with open(full_path, 'w') as f:
            f.write(config)
        
        print(f"\n✅ Success! Config saved to:")
        print(f"📂 {full_path}")
        print(f"🔒 Endpoint masked as: {endpoint_ip}:443")
        print("📱 Import this file into your WireGuard app.")
        return full_path
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        print("   Make sure you have write permissions.")
        return None

def main():
    print("🚀 WGAyhan: Interactive Save Location Mode")
    print("-" * 40)
    
    if not run_command("wg --version"):
        print("⚠️  Error: 'wg' tool not found.")
        print("   Install: pkg install wireguard-tools")
        return

    private_key, public_key = generate_keys()
    if not private_key:
        return

    endpoint_ip = get_smart_endpoint()
    
    # Ask user for save location
    save_path = ask_save_location()
    
    create_and_save_config(private_key, public_key, endpoint_ip, save_path)

if __name__ == "__main__":
    main()
