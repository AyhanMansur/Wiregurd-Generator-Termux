#Copyright  = Ban
import os
import subprocess
import random
from datetime import datetime

def run_command(cmd):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e.stderr}")
        return None

def generate_keys():
    """Generate WireGuard keys using system 'wg' tool."""
    print("🔐 Generating secure keys...")
    private_key = run_command("wg genkey")
    if not private_key:
        print("❌ Failed to generate private key. Is 'wireguard-tools' installed?")
        return None, None
    
    public_key = run_command(f"echo '{private_key}' | wg pubkey")
    if not public_key:
        print("❌ Failed to generate public key.")
        return None, None
    
    return private_key, public_key

def get_smart_endpoint():
    """Select a random, masked endpoint from ArvanCloud or Cloudflare."""
    # ArvanCloud IP ranges (Examples)
    arvan_ips = [
        "5.23.100.1", "5.23.100.2", "5.23.101.1", "5.23.102.1",
        "185.143.223.1", "185.143.223.2", "185.143.224.1"
    ]
    # Cloudflare IP ranges (Examples)
    cloudflare_ips = [
        "1.1.1.1", "1.0.0.1", "1.1.1.2", "1.0.0.2",
        "104.16.132.229", "104.16.133.229", "104.16.134.229"
    ]
    
    # Combine and pick one randomly
    all_ips = arvan_ips + cloudflare_ips
    return random.choice(all_ips)

def create_config(private_key, public_key, endpoint_ip):
    """Create the WireGuard configuration string."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"WGAyhan_Config_{timestamp}.conf"
    
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
        with open(filename, 'w') as f:
            f.write(config)
        print(f"\n✅ Success! Config saved to: {filename}")
        print(f"🔒 Endpoint masked as: {endpoint_ip}:443")
        print("📱 Import this file into your WireGuard app to start.")
        return filename
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

def main():
    print("🚀 WGAyhan: Advanced WireGuard Generator")
    print("-" * 40)
    
    # Check if wg is available
    if not run_command("wg --version"):
        print("⚠️  Error: 'wg' tool not found.")
        print("   Install it first:")
        print("   Termux: pkg install wireguard-tools")
        print("   Linux:  sudo apt install wireguard")
        return

    private_key, public_key = generate_keys()
    if not private_key:
        return

    endpoint_ip = get_smart_endpoint()
    create_config(private_key, public_key, endpoint_ip)

if __name__ == "__main__":
    main()

