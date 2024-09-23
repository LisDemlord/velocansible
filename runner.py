#!/usr/bin/env python3

import subprocess

# ANSI escape codes for colors
class Colors:
    GREEN = "\033[92m"  # Green color for successful messages
    ORANGE = "\033[33m"  # Orange color for warnings or changes
    RED = "\033[31m"  # Red color for errors
    RESET = "\033[0m"  # Reset color to default

def run_playbook(playbook):
    # Command to run the Ansible playbook
    command = [
        'ansible-playbook',
        '-i', 'inventory/hosts.yml',  # Inventory file
        playbook,  # Playbook to execute
        '--vault-password-file=~/.vault_pass.txt'  # Vault password file
    ]
    
    try:
        # Use Popen to run the command and stream the output
        with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
            for line in process.stdout:
                # Color the output based on the content
                if "ok:" in line and "playbook:" not in line:
                    print(Colors.GREEN + line.strip() + Colors.RESET)  # Print successful tasks in green
                elif "changed:" in line:
                    print(Colors.ORANGE + line.strip() + Colors.RESET)  # Print changed tasks in orange
                elif "fatal:" in line or "ERROR" in line:
                    print(Colors.RED + line.strip() + Colors.RESET)  # Print errors in red
                elif "PLAY [" in line:
                    print(Colors.ORANGE + "=== Starting Play: " + line.strip().replace('*', '') + " ===" + Colors.RESET)  # Indicate the start of a play
                elif "TASK [" in line:
                    print(">>> " + line.strip().replace('*', ''))  # Indicate the current task
                elif "PLAY RECAP" in line:
                    print(Colors.ORANGE + "=== " + line.strip().replace('*', '') + " ===" + Colors.RESET)  # Indicate the recap of the play
                else:
                    print(line.strip())  # Print other lines as they are
            process.wait()  # Wait for the process to complete
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, command)  # Raise an error if the playbook execution failed
        
        print(f"\n{Colors.GREEN}Successfully executed playbook: {playbook} {Colors.RESET}\n")  # Print success message
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}Error executing playbook {playbook}: {e}{Colors.RESET}\n")  # Print error message
        if e.stdout:  # Check if e.stdout is not None
            print(e.stdout)  # Print the error logs if needed

def install_velociraptor():
    # List of playbooks for installation
    playbooks = ['playbooks/install-host.yml', 'playbooks/install-clients.yml']
    
    for playbook in playbooks:
        run_playbook(playbook)  # Run each playbook

def rollback_velociraptor():
    # List of playbooks for rollback
    playbooks = ['playbooks/rollback-host.yml', 'playbooks/rollback-clients.yml']
    
    for playbook in playbooks:
        run_playbook(playbook)  # Run each playbook

def main():
    # Prompt user for action
    choice = input("Do you want to (i)nstall or (r)ollback Velociraptor? (i/r): ").strip().lower()
    
    if choice == 'i':
        install_velociraptor()  # Call install function
    elif choice == 'r':
        rollback_velociraptor()  # Call rollback function
    else:
        print("Invalid choice. Please enter 'i' for install or 'r' for rollback.")  # Handle invalid input

if __name__ == "__main__":
    main()  # Execute the main function