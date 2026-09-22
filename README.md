# 🛡️ Advanced TCP Port Scanner & Banner Grabber

> A professional, multi-threaded network utility written in pure Python, built as a portfolio project for software engineering and pentesting enthusiasts.

---

## 🚀 About the Project

**Advanced TCP Port Scanner** is a fast, lightweight, and highly configurable TCP port scanning tool built entirely with Python's built-in standard libraries. It leverages multithreading to check hundreds of ports concurrently in a fraction of a second and performs active service probing (Banner Grabbing) to identify the software running behind the open ports.

The project is designed with clean architecture, zero external dependencies, and a polished, color-coded command-line interface (CLI).

---

## ✨ Key Features (v1.0)

* **Multithreading:** Utilizes `ThreadPoolExecutor` for high-performance, parallel port scanning.
* **Flexible Port Parsing:** Supports individual ports separated by commas (e.g., `22,80,443`) and continuous ranges using hyphens (e.g., `1-1024`).
* **Advanced Banner Grabbing:** Automatic greeting banner collection for services like SSH or FTP, plus active HTTP probing (sending a `GET` request to force web servers to respond).
* **Color-Coded CLI (ANSI):** Dynamic terminal coloring without the need for external packages (green for open ports, cyan for banners, yellow/red for status messages).
* **Clean Reporting:** Automatically exports clean, ANSI-free logs to a designated text report file using the `-o` flag.

---

## 🛠️ Technical Requirements

* **Python 3.x** (No external `pip` packages required!)
* Operating System: macOS, Linux, or Windows.

---

## ⚙️ Usage

Clone the repository and run the script from your terminal using the available configuration flags:

```bash
python3 scanner.py -t <TARGET_IP_OR_DOMAIN> [OPTIONS]
```

### Available Arguments:
* `-t`, `--target` *(required)*: Target IP address or domain name (e.g., `127.0.0.1` or `scanme.nmap.org`).
* `-p`, `--ports`: Ports to scan. Can be individual ports or ranges (default: `21,22,80,443,8080`).
* `-w`, `--threads`: Number of concurrent worker threads (default: `100`).
* `-o`, `--output`: Path to the text report file (e.g., `scan_report.txt`).

### Examples:
Scan the first 1024 ports of localhost using 200 threads and save the output to a file:
```bash
python3 scanner.py -t 127.0.0.1 -p 1-1024 -w 200 -o scan_report.txt
```

---

## 🗺️ Roadmap

This project is actively developed using an iterative approach. Future versions will include:

- [ ] **Version 1.1:** Export results to structured formats (**JSON** and **CSV**).
- [ ] **Version 1.2:** Real-time interactive **Progress Bar** for large port ranges.
- [ ] **Version 1.3:** Advanced *Service Fingerprinting* (accurate software version detection based on signature databases).
- [ ] **Version 2.0:** Support for **UDP** port scanning.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE). Feel free to modify and use it for educational or commercial purposes.