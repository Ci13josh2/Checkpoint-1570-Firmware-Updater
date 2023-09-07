import paramiko
import time
import csv

# Define the SSH parameters
port = 22
Command1 = "upgrade from tftp server IP filename firmwareimagefilename.img"
Command2 = "yes"  # Command to confirm upgrade

# Open the CSV file containing firewall settings
with open('///filepath to csv file///', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        hostname = row['Hostname']
        username = row['Username']
        password = row['Password']
        device_prompt = row['device_prompt']

        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Connect to the firewall
            ssh.connect(hostname, port, username, password, timeout=10)

            # Start an SSH shell session
            shell = ssh.invoke_shell()

            # Wait for the firewall prompt
            while True:
                output = shell.recv(1000).decode("utf-8")
                if device_prompt in output:
                    break

            #Send the update command
            shell.send(Command1 + "\n")
            time.sleep(1)
            #confirm the update
            shell.send(Command2 + "\n")
            time.sleep(1)

            # Read and print the command output
            while True:
                output = shell.recv(1000).decode("utf-8")
                print(output, end="")
                if device_prompt in output:
                    break

            # Disconnect the SSH session
            ssh.close()

        except paramiko.AuthenticationException:
            print(f"Authentication failed for {hostname}. Check your username and password.")
        except paramiko.SSHException as e:
            print(f"SSH error for {hostname}: {str(e)}")
        except Exception as e:
            print(f"An error occurred for {hostname}: {str(e)}")
        finally:
            ssh.close()
