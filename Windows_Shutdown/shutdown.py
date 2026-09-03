import os
import sys
import platform

def execute_shutdown(seconds: int = 0, dry_run: bool = True) -> str:
    """Safely execute system shutdown or simulate in dry-run mode."""
    system_os = platform.system()
    print(f"Detected OS: {system_os}")

    if dry_run:
        cmd_sim = f"shutdown /s /t {seconds}" if system_os == "Windows" else f"shutdown -h +{seconds // 60}"
        msg = f"[DRY-RUN SIMULATION] Would execute command: '{cmd_sim}'"
        print(msg)
        return msg

    if system_os == "Windows":
        cmd = f"shutdown /s /t {seconds}"
    elif system_os in ["Linux", "Darwin"]:
        cmd = f"shutdown -h +{seconds // 60}" if seconds >= 60 else "shutdown -h now"
    else:
        print(f"Unsupported operating system: {system_os}")
        return ""

    print(f"Executing shutdown command: '{cmd}'")
    os.system(cmd)
    return cmd

def cancel_shutdown(dry_run: bool = True):
    """Cancel scheduled shutdown."""
    system_os = platform.system()
    if dry_run:
        print("[DRY-RUN SIMULATION] Would execute: shutdown /a")
        return

    if system_os == "Windows":
        os.system("shutdown /a")
        print("Scheduled Windows shutdown cancelled.")
    elif system_os in ["Linux", "Darwin"]:
        os.system("shutdown -c")
        print("Scheduled Unix shutdown cancelled.")

def main():
    print("=== Windows / Cross-Platform System Shutdown Utility ===")
    print("WARNING: This utility can shut down or restart your computer.")
    
    confirm = input("Do you want to proceed with shutdown menu? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Shutdown operation cancelled by user.")
        return

    print("\nOptions:")
    print("1. Simulate Shutdown (Dry-Run Mode)")
    print("2. Schedule System Shutdown")
    print("3. Abort/Cancel Scheduled Shutdown")

    choice = input("Enter choice (1-3, default 1): ").strip()

    if choice == '2':
        try:
            delay = int(input("Enter delay in seconds (e.g. 60): "))
        except ValueError:
            delay = 60
        confirm_live = input(f"ARE YOU SURE you want to shut down in {delay} seconds? (type 'YES'): ").strip()
        if confirm_live == 'YES':
            execute_shutdown(seconds=delay, dry_run=False)
        else:
            print("Live shutdown cancelled.")
    elif choice == '3':
        cancel_shutdown(dry_run=False)
    else:
        execute_shutdown(seconds=0, dry_run=True)

if __name__ == '__main__':
    main()

