import socket
import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- KODY KOLORÓW ANSI DLA TERMINALA ---
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BOLD = "\033[1m"

# 1. Konfiguracja parsera argumentów z linii poleceń
parser = argparse.ArgumentParser(description="Zaawansowany Skaner Portów TCP - Projekt Portfolio")
parser.add_argument("-t", "--target", required=True, help="Adres IP lub domena docelowa do skanowania")
parser.add_argument("-p", "--ports", default="21,22,80,443,8080", help="Porty po przecinku lub zakres (np. 1-1024 lub 22,80,100-200)")
parser.add_argument("-o", "--output", help="Ścieżka do pliku raportu (np. scan_report.txt)")
parser.add_argument("-w", "--threads", type=int, default=100, help="Liczba wątków do jednoczesnego skanowania (domyślnie: 100)")

# Parsowanie argumentów
args = parser.parse_args()
target_host = args.target

# Zaawansowane parsowanie portów
ports_to_scan = []
try:
    for part in args.ports.split(","):
        if "-" in part:
            start_port, end_port = part.split("-")
            ports_to_scan.extend(range(int(start_port.strip()), int(end_port.strip()) + 1))
        else:
            ports_to_scan.append(int(part.strip()))
except ValueError:
    print(f"{RED}[!] Błąd: Nieprawidłowy format portów. Użyj liczb (np. 80) lub zakresów (np. 1-1024).{RESET}")
    exit(1)

# Listy na wyniki
results_log = []      # Czysty tekst do pliku
display_log = []      # Tekst z kolorami do terminala

header = "-" * 60
msg_target = f"Skanowanie celu: {target_host} (portów: {len(ports_to_scan)}, wątków: {args.threads})"
msg_start = f"Rozpoczęto o: {time.strftime('%H:%M:%S')}"

# Przygotowanie nagłówka
for line in [header, msg_target, msg_start, header]:
    results_log.append(line)
    display_log.append(f"{YELLOW}{BOLD}{line}{RESET}")

# Wyświetlenie nagłówka w terminalu
for line in display_log:
    print(line)

# Funkcja Banner Grabbingu z aktywnym sondowaniem
def grab_banner(target, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        
        result = s.connect_ex((target, port))
        if result == 0:
            banner = None
            try:
                if port in [80, 443, 8080, 5000, 8000]:
                    http_request = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
                    s.sendall(http_request.encode('utf-8'))
                
                banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
            except socket.timeout:
                pass
            
            s.close()
            return port, True, banner
        else:
            s.close()
            return port, False, None
            
    except socket.error:
        return port, False, None

# --- START TIMERA I WIELOWĄTKOWOŚCI ---
start_time = time.time()
open_ports_count = 0

try:
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_port = {executor.submit(grab_banner, target_host, port): port for port in ports_to_scan}
        
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                _, is_open, banner = future.result()
                if is_open:
                    open_ports_count += 1
                    if banner:
                        first_line_banner = banner.split('\n')[0]
                        clean_line = f"[+] Port {port}: OTWARTY | Usługa/Banner: {first_line_banner}"
                        colored_line = f"{GREEN}[+] Port {port}: OTWARTY{RESET} | {CYAN}Usługa: {first_line_banner}{RESET}"
                    else:
                        clean_line = f"[+] Port {port}: OTWARTY"
                        colored_line = f"{GREEN}[+] Port {port}: OTWARTY{RESET}"
                    
                    print(colored_line)
                    results_log.append(clean_line)
            except Exception:
                pass

except KeyboardInterrupt:
    interrupt_msg = "\n[!] Skanowanie przerwane przez użytkownika."
    print(f"{RED}{interrupt_msg}{RESET}")
    results_log.append(interrupt_msg)

# --- KONIEC TIMERA ---
end_time = time.time()
elapsed_time = end_time - start_time

footer1 = "-" * 60
summary_msg = f"Znaleziono otwartych portów: {open_ports_count}"
footer2 = f"Skanowanie zakończone w czasie: {elapsed_time:.2f} sekund"

# Przygotowanie stopki
for line in [footer1, summary_msg, footer2, footer1]:
    results_log.append(line)
    print(f"{YELLOW}{line}{RESET}")

# --- ZAPIS DO PLIKU (Czysty tekst bez kodów kolorów) ---
if args.output:
    try:
        with open(args.output, "w") as file:
            file.write("\n".join(results_log) + "\n")
        print(f"\n{GREEN}[+] Wyniki zostały pomyślnie zapisane do pliku: {args.output}{RESET}")
    except IOError:
        print(f"{RED}[!] Błąd: Nie udało się zapisać pliku {args.output}{RESET}")