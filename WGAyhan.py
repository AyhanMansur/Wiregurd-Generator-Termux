#copyright = DDos Attack 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WGAyhan: Zero-Error WireGuard Config Generator
Features:
- No key generation (User provides keys)
- Pre-defined ArvanCloud IP ranges
- Clean, error-free output
"""

import os
from datetime import datetime

def get_user_input(prompt):
    """Get input from user with validation."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("❌ Input cannot be empty. Please try again.")

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
            if os.path.exists("/sdcard"):
                return "/sdcard/Download"
            else:
                print("⚠️  Storage permission not granted! Run 'termux-setup-storage' first.")
                print("   Or choose option 1 to save locally.")
                continue
        else:
            print("❌ Invalid choice. Please enter 1 or 2.")

def create_config(private_key, public_key):
    """Create a clean WireGuard config with ArvanCloud ranges."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"WGAyhan_Arvan_Config_{timestamp}.conf"
    
    # این دقیقاً همون فرمتیه که خواستی با رنج‌های آوان
    config = f"""[Interface]
PrivateKey = {private_key}
ListenPort = 443
Address = 185.10.104.0/22
DNS = 1.1.1.1, 9.9.9.9, 178.22.122.100, 178.22.122.101

[Peer]
PublicKey = {public_key}
AllowedIPs = 185.10.104.0/22, 185.10.108.0/22, 5.23.128.0/18
Endpoint = arvancloud.ir:443
PersistentKeepalive = 25
"""
    return filename, config

def save_config(filename, config, save_path):
    full_path = os.path.join(save_path, filename)
    
    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        with open(full_path, 'w') as f:
            f.write(config)
        
        print(f"\n✅ Success! Config saved to:")
        print(f"📂 {full_path}")
        print("🔒 Endpoint: arvancloud.ir:443")
        print("📱 Import this file into your WireGuard app.")
        return full_path
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        return None

def main():
    print("🚀 WGAyhan: Zero-Error ArvanCloud Config Generator")
    print("-" * 40)
    print("⚠️  This script does NOT generate keys.")
    print("   Please enter your own Private and Public keys below.")
    print("-" * 40)
    
    # Get keys from user
    private_key = get_user_input("🔑 Enter your WireGuard Private Key: ")
    public_key = get_user_input("🔑 Enter your WireGuard Public Key: ")
    
    # Validate keys (basic check)
    if len(private_key) < 20 or len(public_key) < 20:
        print("⚠️  Warning: Keys seem too short. Please check if they are correct.")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return

    filename, config = create_config(private_key, public_key)
    save_path = ask_save_location()
    save_config(filename, config, save_path)

if __name__ == "__main__":
    main()
