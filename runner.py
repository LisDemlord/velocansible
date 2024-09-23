#!/usr/bin/env python3

import subprocess

# ANSI escape codes for colors
class Colors:
    GREEN = "\033[92m"
    ORANGE = "\033[33m"
    RED = "\033[31m"
    RESET = "\033[0m"

def run_playbook(playbook):
    command = [
        'ansible-playbook',
        '-i', 'inventory/hosts.yml',
        playbook,
        '--vault-password-file=~/.vault_pass.txt'
    ]
    
    try:
        # Use Popen to run the command and stream the output
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
            for line in process.stdout:
                # Color the output based on the content
                if "ok:" in line and "playbook:" not in line:
                    print(Colors.GREEN + line.strip() + Colors.RESET)
                elif "changed:" in line:
                    print(Colors.ORANGE + line.strip() + Colors.RESET)
                elif "fatal:" in line or "ERROR" in line:
                    print(Colors.RED + line.strip() + Colors.RESET)
                elif "PLAY [" in line:
                    print(Colors.ORANGE + "=== Starting Play: " + line.strip().replace('*', '') + "===" + Colors.RESET)
                elif "TASK [" in line:
                    print(">>> " + line.strip().replace('*', ''))
                elif "PLAY RECAP" in line:
                    print(Colors.ORANGE + "=== " + line.strip().replace('*', '') + " ===" + Colors.RESET)
                else:
                    print(line.strip())
            process.wait()  # Wait for the process to complete
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)
        
        print(f"\n{Colors.GREEN}Successfully executed playbook: {playbook} {Colors.RESET}\n")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error executing playbook {playbook}: {e}{Colors.RESET}\n")
        if e.stdout:  # Проверяем, что e.stdout не None
            print(e.stdout)  # Print the error logs if needed

def install_velociraptor():
    playbooks = ['playbooks/install-host.yml', 'playbooks/install-clients.yml']
    
    for playbook in playbooks:
        run_playbook(playbook)
        
def rollback_velociraptor():
    playbooks = ['playbooks/rollback-host.yml', 'playbooks/rollback-clients.yml']
    
    for playbook in playbooks:
        run_playbook(playbook)

def main():
    choice = input("Do you want to (i)nstall or (r)ollback Velociraptor? (i/r): ").strip().lower()
    
    if choice == 'i':
        install_velociraptor()
    elif choice == 'r':
        rollback_velociraptor()
    else:
        print("Invalid choice. Please enter 'i' for install or 'r' for rollback.")

if __name__ == "__main__":
    main()