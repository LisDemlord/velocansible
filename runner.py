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
        '--vault-password-file=/etc/.vault_pass.txt'  # Vault password file
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

def install_velociraptor(role):
    # Select the appropriate playbook based on role
    if role == "host":
        playbook = 'playbooks/install-host.yml'
    else:
        playbook = 'playbooks/install-clients.yml'
    
    run_playbook(playbook)  # Run the selected playbook

def rollback_velociraptor(role):
    # Select the appropriate playbook based on role
    if role == "host":
        playbook = 'playbooks/rollback-host.yml'
    else:
        playbook = 'playbooks/rollback-clients.yml'
    
    run_playbook(playbook)  # Run the selected playbook

def get_user_choice(prompt, choices):
    # Get user input with validation loop
    while True:
        choice = input(prompt).strip().lower()
        if choice in choices:
            return choice
        else:
            print(f"\n{Colors.ORANGE}Invalid choice. Please select from {' or '.join(choices)}.{Colors.RESET}")

def main():
    # Mapping from short action codes to full action names
    action_map = {'i': 'install', 'r': 'rollback'}
    
    # Prompt user for install or rollback
    action = get_user_choice("\n>>> Do you want to (i)nstall or (r)ollback Velociraptor? (i/r): ", ['i', 'r'])
    
    # Prompt user for host or client
    role = get_user_choice("\n>>> Is this for (h)ost or (c)lient? (h/c): ", ['h', 'c'])
    
    # Perform the action based on user input
    if action == 'i':
        install_velociraptor('host' if role == 'h' else 'client')
    else:
        rollback_velociraptor('host' if role == 'h' else 'client')
    
    # Allow to continue only if the first role is host
    if role == 'h':
        action_full = action_map[action]
        continue_same_action = get_user_choice(f"\n>>> Do you want to {action_full} the client as well? (y/n): ", ['y', 'n'])
        if continue_same_action == 'y':
            if action == 'i':
                install_velociraptor('client')
            else:
                rollback_velociraptor('client')

if __name__ == "__main__":
    main()  # Execute the main function