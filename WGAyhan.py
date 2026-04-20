#copyright = DDos Attack 
import os
import sys
import time
import random
import threading
from datetime import datetime

# --- تنظیمات رنگ‌های نئونی (برای ترمینال و Termux) ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
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
{Colors.CYAN}   Project: SpaceCity Big Bridge (Secret Mode) {Colors.END}
{Colors.YELLOW}   Status: {Colors.GREEN}SECURE & ENCRYPTED {Colors.END}
{Colors.END}
"""
    print(logo)

def log(message, color=Colors.GREEN):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Colors.CYAN}[{timestamp}]{Colors.END} {color}{message}{Colors.END}")

def simulate_traffic(source, dest, data_size):
    """شبیه‌سازی انتقال داده بین لایه‌ها"""
    delay = random.uniform(0.1, 0.5)
    time.sleep(delay)
    status = "SUCCESS" if random.random() > 0.05 else "PACKET LOSS"
    color = Colors.GREEN if status == "SUCCESS" else Colors.RED
    log(f"🚀 {source} -> {dest}: {data_size} MB | Status: {status}", color)

def run_space_bridge():
    clear_screen()
    print_logo()
    
    # لیست سرورهای مجازی (شبیه‌سازی شده)
    servers = ["IRAN_CORE", "GERMANY_GATE", "UAE_PROXY", "TURKEY_NODE"]
    
    log("🔒 Initializing Space City Network...", Colors.YELLOW)
    time.sleep(1)
    
    # حلقه اصلی شبیه‌سازی
    try:
        while True:
            # انتخاب تصادفی دو سرور برای ارتباط
            src = random.choice(servers)
            dst = random.choice([s for s in servers if s != src])
            
            # تولید حجم داده تصادفی
            size = random.randint(10, 500)
            
            log(f"🌐 Routing Packet: {src} <-> {dst} ({size} MB)", Colors.CYAN)
            simulate_traffic(src, dst, size)
            
            # نمایش وضعیت لایه‌ها
            print(f"\n{Colors.BOLD}Current Layer Status:{Colors.END}")
            for s in servers:
                status = "🟢 ONLINE" if random.random() > 0.1 else "🔴 OFFLINE"
                print(f"  {s}: {status}")
            
            time.sleep(2) # فاصله بین هر پکت
            
    except KeyboardInterrupt:
        log("\n🛑 Network Bridge Shutting Down...", Colors.RED)
        print(f"{Colors.YELLOW}Goodbye, Genius! Stay Secure! 🚀{Colors.END}")
        sys.exit(0)

if __name__ == "__main__":
    # بررسی اینکه آیا در Termux اجرا می‌شود یا نه (برای رنگ‌ها)
    if 'TERM' in os.environ:
        run_space_bridge()
    else:
        log("Please run this script in a terminal (Linux or Termux).", Colors.RED)
