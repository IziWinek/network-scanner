import socket
import time
import argparse

# 1. Konfiguracja parsera argumentów z linii poleceń
parser = argparse.ArgumentParser(description="Prosty Skaner Portów TCP - Projekt Portfolio")
parser.add_argument("-t", "--target", required=True, help="Adres IP lub domena docelowa do skanowania")
parser.add_argument("-p", "--ports", default="21,22,80,443,8080", help="Porty do skanowania po przecinku (domyślnie: popularne porty)")

# Parsowanie argumentów podanych przez użytkownika
args = parser.parse_args()

target_host = args.target

# Przekształcenie stringa z portami (np. "80,443,8080") na listę liczb całkowitych [80, 443, 8080]
try:
    ports_to_scan = [int(port.strip()) for port in args.ports.split(",")]
except ValueError:
    print("[!] Błąd: Porty muszą być liczbami rozdzielonymi przecinkami.")
    exit(1)

print("-" * 50)
print(f"Skanowanie celu: {target_host}")
print(f"Rozpoczęto o: {time.strftime('%H:%M:%S')}")
print("-" * 50)

try:
    for port in ports_to_scan:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        
        result = s.connect_ex((target_host, port))
        
        if result == 0:
            print(f"[+] Port {port}: OTWARTY")
        
        s.close()

except KeyboardInterrupt:
    print("\n[!] Skanowanie przerwane przez użytkownika.")
except socket.gaierror:
    print("\n[!] Błąd: Nie udało się rozwiązać nazwy hosta (błędny adres?).")
except socket.error:
    print("\n[!] Błąd: Brak połączenia z serwerem.")

print("-" * 50)
print("Skanowanie zakończone.")