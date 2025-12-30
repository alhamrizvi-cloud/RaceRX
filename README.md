
# RaceRX ⚡ (RacerX)
### Race Condition Testing Tool for Bug Bounty & Security Research

RaceRX (also known as RacerX) is a lightweight CLI tool designed to test **race condition vulnerabilities** in web applications by sending **synchronized parallel HTTP requests** to a target endpoint.

It is built for **bug bounty hunters, penetration testers, and security researchers** who want a simple but effective way to validate race conditions beyond manual Burp testing.



## ✨ Features

- ⚡ High‑concurrency race testing
- 🧵 Multi‑threaded request execution
- 🧩 Accepts **raw HTTP requests** (Burp‑compatible)
- 🔁 Supports GET and POST methods
- 📊 Displays response status codes & sizes
- 🛡 Detects consistent vs inconsistent responses
- 🖥 Clean CLI interface with banner


## 🎯 What RaceRX Is Used For

RaceRX helps identify **business logic vulnerabilities caused by race conditions**, such as:

- Multiple coupon or promo redemptions
- Double spending / balance duplication
- Multiple order confirmations
- Concurrent refund abuse
- Email / account update race issues
- Wallet withdrawal duplication

⚠️ RaceRX focuses on **logic races**, not flooding or DoS attacks.


## 📦 Requirements

### System
- Linux (Parrot, Kali, Ubuntu recommended)
- Python **3.8+**

### Python Dependency
```bash
pip install requests
````


## 🚀 Installation

```bash
git clone https://github.com/alhamrizvi-cloud/RaceRX.git
cd Racerx
python3 racerx.py
```

## 🌍 Make RaceRX a Global Command (Recommended)

Run RaceRX from **any directory** like a real security tool.

### 1️⃣ Add a Shebang

Ensure the **first line** of the script is:

```python
#!/usr/bin/env python3
```

### 2️⃣ Rename the File

```bash
mv toolkit1.py racerx.py
mv racerx.py Racerx
```

### 3️⃣ Make It Executable

```bash
chmod +x Racerx
```

### 4️⃣ Move It to PATH

```bash
sudo mv Racerx /usr/local/bin/
```

### 5️⃣ Run Globally 🎉

```bash
Racerx
```

Verify installation:

```bash
which Racerx
```

Expected output:

```
/usr/local/bin/Racerx
```

## 🧪 Usage

Run the tool:

```bash
Racerx
```

You will be prompted for:

1. Target URL
2. HTTP Method (GET / POST)
3. Raw HTTP Request
4. Number of parallel requests

## 📝 Example Raw HTTP Request

```http
POST /cart/coupon HTTP/1.1
Host: example.com
Cookie: session=ABC123
Content-Type: application/x-www-form-urlencoded

csrf=TOKEN&coupon=PROMO20
```

## 📊 Sample Output

```
[+] Starting race condition test...

[1] 200 | 312 bytes
[2] 200 | 312 bytes
[3] 400 | 20 bytes

[✓] Completed in 2.04 seconds
[!] Inconsistent responses detected – potential race condition
```


## 🔍 How to Identify a Race Condition

Look for:

* Mixed response codes (200 + 400)
* Multiple successful responses for a single‑use action
* Incorrect cart totals or balance changes
* Duplicate confirmations or transactions

If all responses are identical, the endpoint is likely **race‑safe**.

---

## ⚠️ Important Notes

* Always use a **valid CSRF token**
* Ensure the **Host header matches the target URL**
* Do NOT hardcode `Content-Length`
* Avoid excessive threads — races require precision
* Many endpoints are intentionally protected


## 🧠 Best Targets for RaceRX

### ✅ Good

* `/checkout`
* `/confirm-order`
* `/wallet/withdraw`
* `/refund`
* `/change-email`

### ❌ Bad

* `/login`
* `/register`
* `/cart/coupon`
* Strict CSRF‑locked endpoints

## 🛑 Limitations

* HTTP/1.1 only
* No HTTP/2 support
* No automatic CSRF refresh
* No built‑in proxy (manual Burp integration only)

## ⚖️ Legal Disclaimer

This tool is intended **only for authorized security testing and educational purposes**.

You must have **explicit permission** before testing any target.
The author is **not responsible** for misuse or illegal activity.


## 👨‍💻 Author

**Alham Rizvi**
Bug Bounty Hunter | Security Researcher
Instagram: **@alhamrizvii**

## ⭐ Contributing

Pull requests, improvements, and feature ideas are welcome.
Fork it, improve it, and break things responsibly.


## 🔮 Future Improvements

* HTTP/2 support
* Barrier‑based thread synchronization
* Burp proxy integration
* Automatic CSRF extraction
* Response diffing & logic detection
* CLI flags (`--threads`, `--url`, `--raw`)


Happy Hunting ⚡

