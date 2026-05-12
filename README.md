# 🔪 SharpLoader - C# Payload Builder for Windows Red Teaming

**Cross-platform payload generator that compiles XOR-obfuscated C# stagers directly on Kali Linux - no Windows required.**

[![License](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-blue)](https://www.kali.org/)
[![Language](https://img.shields.io/badge/Python-3.x-green)](https://www.python.org/)
[![Build](https://img.shields.io/badge/Compiler-Mono-purple)](https://www.mono-project.com/)

---

## 📋 Table of Contents
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Attack Flow Diagram](#attack-flow-diagram)
- [Windows Defender Bypass Techniques](#windows-defender-bypass-techniques)
- [Installation](#installation)
- [Usage](#usage)
- [Technical Deep Dive](#technical-deep-dive)
- [OPSEC Considerations](#opsec-considerations)
- [Troubleshooting](#troubleshooting)
- [Legal Disclaimer](#legal-disclaimer)

---

## 🎯 Overview

SharpLoader is a Python-based tool that converts raw shellcode from C2 frameworks (Havoc, Adaptix, Cobalt Strike, msfvenom) into fully functional Windows executables. It uses **XOR-obfuscated C# stagers** compiled on Kali Linux via Mono - eliminating the need for a Windows build environment.

### Key Features

| Feature | Description |
|---------|-------------|
| 🌐 **Cross-Platform** | Compiles Windows EXEs directly on Kali Linux |
| 🔐 **XOR Obfuscation** | Encrypts C2 indicators (IP, Port, URL) at rest |
| 📡 **HTTP Stager** | Downloads shellcode from remote C2 server |
| 💾 **Registry Persistence** | Auto-adds to HKCU Run on execution |
| 🪟 **Hidden Console** | Runs silently without popup windows |
| 🔄 **PowerShell Fallback** | Generates alternative loader |
| 🛡️ **AV Bypass** | Static detection evasion via string obfuscation |

---

## ⚙️ How It Works
    ● Cross-platform compilation (Kali → Windows EXE)
    ● XOR encryption of C2 indicators (IP, Port, URL)
    ● HTTP stager with remote payload delivery
    ● Registry persistence (HKCU\Software\Microsoft\Windows\CurrentVersion\Run)
    ● Hidden console execution (no popup windows)
    ● PowerShell fallback generator
    ● Windows Defender static bypass via string obfuscation




[+] Key Features:
    ● Cross-platform compilation (Kali → Windows EXE)
    ● XOR encryption of C2 indicators (IP, Port, URL)
    ● HTTP stager with remote payload delivery
    ● Registry persistence (HKCU\Software\Microsoft\Windows\CurrentVersion\Run)
    ● Hidden console execution (no popup windows)
    ● PowerShell fallback generator
    ● Windows Defender static bypass via string obfuscation

[+] Attack Workflow Diagram:

    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                                                                             │
    │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
    │  │ 1. Generate  │     │ 2. Convert   │     │ 3. XOR-      │               │
    │  │ Shellcode    │────▶│ to C# Stager │────▶│ Encrypt C2   │               │
    │  │ (Havoc/      │     │ (HTTP Loader)│     │ Strings      │               │
    │  │ msfvenom)    │     │              │     │              │               │
    │  └──────────────┘     └──────────────┘     └──────────────┘               │
    │         │                    │                    │                       │
    │         ▼                    ▼                    ▼                       │
    │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐               │
    │  │ demon.x64.bin│     │ payload.cs   │     │ XOR Key:0xAA │               │
    │  │ (Raw Binary) │     │ (C# Source)  │     │ Obfuscation  │               │
    │  └──────────────┘     └──────────────┘     └──────────────┘               │
    │                              │                    │                       │
    │                              ▼                    ▼                       │
    │                       ┌──────────────┐     ┌──────────────┐               │
    │                       │ 4. Compile   │     │ 5. HTTP      │               │
    │                       │ with Mono    │────▶│ Server       │               │
    │                       │ (mcs)        │     │ Port 8443    │               │
    │                       └──────────────┘     └──────────────┘               │
    │                              │                    │                       │
    │                              ▼                    │                       │
    │                       ┌──────────────┐            │                       │
    │                       │ 6. svcc.exe  │            │                       │
    │                       │ (Windows     │            │                       │
    │                       │  Executable) │            │                       │
    │                       └──────────────┘            │                       │
    │                              │                    │                       │
    │                              ▼                    ▼                       │
    │  ┌────────────────────────────────────────────────────────────────────┐  │
    │  │                         WINDOWS TARGET                             │  │
    │  │  ┌─────────────────────────────────────────────────────────────┐  │  │
    │  │  │ 7. Execute svcc.exe                                          │  │  │
    │  │  │         │                                                    │  │  │
    │  │  │         ▼                                                    │  │  │
    │  │  │ 8. Decrypt XOR strings (IP:Port:URL)                         │  │  │
    │  │  │         │                                                    │  │  │
    │  │  │         ▼                                                    │  │  │
    │  │  │ 9. HTTP GET request to http://KALI_IP:8443/demon.x64.bin    │  │  │
    │  │  │         │                                                    │  │  │
    │  │  │         ▼                                                    │  │  │
    │  │  │ 10. VirtualAlloc → RWX memory                                │  │  │
    │  │  │         │                                                    │  │  │
    │  │  │         ▼                                                    │  │  │
    │  │  │ 11. CreateThread → Execute shellcode                         │  │  │
    │  │  │         │                                                    │  │  │
    │  │  │         ▼                                                    │  │  │
    │  │  │ 12. Callback to C2 Server                                    │  │  │
    │  │  └─────────────────────────────────────────────────────────────┘  │  │
    │  └────────────────────────────────────────────────────────────────────┘  │
    │                                                                             │
    └─────────────────────────────────────────────────────────────────────────────┘

[+] How It Bypasses Windows Defender:

    Technique                          |  Why It Works
    ──────────────────────────────────┼───────────────────────────────────────────
    XOR String Obfuscation             │  No hardcoded IPs/URLs in the binary
    ──────────────────────────────────┼───────────────────────────────────────────
    Runtime String Decryption          │  Indicators only visible in memory
    ──────────────────────────────────┼───────────────────────────────────────────
    No Embedded Shellcode              │  Payload downloaded after execution
    ──────────────────────────────────┼───────────────────────────────────────────
    Custom C# Stager                   │  Not signatured like known loaders
    ──────────────────────────────────┼───────────────────────────────────────────
    Hidden Console (ShowWindow)        │  No suspicious window appearing
    ──────────────────────────────────┼───────────────────────────────────────────
    Registry Persistence              │  Blends with legitimate software
    ──────────────────────────────────┼───────────────────────────────────────────

[+] Technical Details:

    [*] XOR Encryption Scheme:
        - Key: 0xAA (hardcoded in both builder and stager)
        - Encrypts: C2 IP address, Port number, Download URL
        - Decryption happens at runtime before any network request

    [*] API Calls Used:
        - VirtualAlloc (PAGE_EXECUTE_READWRITE) - Memory allocation
        - CreateThread - Payload execution
        - WaitForSingleObject - Synchronization
        - GetConsoleWindow + ShowWindow - Window hiding
        - WebClient.DownloadData - Remote shellcode retrieval

    [*] Memory Protection:
        - Initial allocation: RW (Read-Write)
        - Shellcode written to allocated memory
        - Execution via thread creation (no VirtualProtect needed)

    [*] Persistence Mechanism:
        - Registry Key: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
        - Value Name: "WindowsUpdate"
        - Value Data: Full path to executable

[+] File Structure After Generation:

    ├── PyCrypt.py          # Main builder script
    ├── demon.x64.bin       # Raw shellcode (your payload)
    ├── svcc.exe            # Compiled Windows executable
    ├── loader.bat          # PowerShell fallback loader
    └── payload.cs          # Temporary C# source (deleted)

[+] Requirements (Kali Linux):

    $ sudo apt update
    $ sudo apt install mono-mcs python3 -y
    $ pip3 install requests  # Optional, for extended features

[+] Usage Examples:

    # Basic usage with default Havoc C2 shellcode
    $ python3 PyCrypt.py

    # Custom configuration (edit inside script)
    LHOST = "10.10.10.100"     # Your Kali IP
    LPORT = "443"               # HTTP server port
    C2_FILE = "beacon.bin"     # Your shellcode file
    OUTPUT_EXE = "update.exe"  # Output filename

[+] Detection Evasion Analysis:

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Static Analysis (File Scan)                                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │  Q: Can AV see the C2 IP/URL?                                           │
    │  A: NO - All strings are XOR encrypted with 0xAA at rest                │
    │                                                                         │
    │  Q: Can AV detect shellcode signature?                                  │
    │  A: NO - Shellcode is downloaded, not embedded in the EXE              │
    │                                                                         │
    │  Q: Is the C# stager signatured?                                        │
    │  A: UNLIKELY - Custom code not in AV databases                          │
    └─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │  Dynamic Analysis (Runtime Detection)                                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │  Q: Does it create suspicious processes?                                │
    │  A: Runs in same process - no child process spawning                    │
    │                                                                         │
    │  Q: Does it have unusual memory allocation?                             │
    │  A: Uses VirtualAlloc (common for legitimate apps)                      │
    │                                                                         │
    │  Q: Can behavioral detection stop it?                                   │
    │  A: MAYBE - Download + execute pattern could trigger some EDRs         │
    └─────────────────────────────────────────────────────────────────────────┘

[+] Limitations & Considerations:

    [!] HTTP staging requires outbound port 8443 (or your configured port)
    [!] Mono-compiled EXEs are larger than Visual Studio builds (~200KB)
    [!] XOR key (0xAA) is static - consider modifying for better OPSEC
    [!] No AMSI bypass included - runs in current context only
    [!] Does not evade EDRs with memory scanning (RWX pages)

[+] OPSEC Improvements (Recommendations):

    1. Change XOR key from default 0xAA to random byte
    2. Add anti-sandbox checks (RAM, uptime, disk size)
    3. Implement process injection instead of self-execution
    4. Add delay loops before downloading shellcode
    5. Use HTTPS instead of HTTP (modify WebClient)
    6. Add AMSI patching before payload execution

[+] Troubleshooting:

    [Problem] Mono compilation fails
    [Solution] $ sudo apt install mono-mcs mono-complete

    [Problem] Shellcode doesn't execute
    [Solution] Test with messagebox shellcode first:
               $ msfvenom -p windows/x64/messagebox -f raw -o demon.x64.bin

    [Problem] Windows Defender blocks execution
    [Solution] Modify XOR key and recompile

[+] Legal Disclaimer:

    This tool is for educational purposes and authorized security testing only.
    Users are responsible for compliance with all applicable laws. Unauthorized
    access to computer systems is illegal.

[+] Credits:

    Built for use with Havoc C2 Framework & Adaptix C2
    Inspired by various C2 stager implementations
