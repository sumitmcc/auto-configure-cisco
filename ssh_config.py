import paramiko
import os.path
import subprocess
import time
import sys
import re


# Function to check IP address file and content validity
def ip_is_valid():
    global ip_list
    # Check if user wants to configure manually
    while True:
        decision = raw_input("Do you want to configure manually or use auto-configuration file? Type:"
                             "\n 1 for Manual Configuration"
                             "\n 2 for auto-configuration \n")

        # Auto Configuration
        if decision == "2":
            ip_file = raw_input("Enter IP file name and extension: ")

            try:
                with open(ip_file) as selected_ip_file:
                    selected_ip_file.seek(0)
                    ip_list = selected_ip_file.readlines()

            except IOError:
                print "\n[FAIL] File {} does not exist! Please check and try again!\n".format(ip_file)
                sys.exit(-1)

        # Manual Configuration
        elif decision == "1":
            ip_list = []
            print "Enter IP addresses of routers to configure. Enter 'done' when finished"
            while True:
                ip = raw_input()
                if ip == 'done':
                    break
                else:
                    ip_list.append(ip)
            if not ip_list:
                print "[FAIL] No IP addresses given, exiting..."
                sys.exit(-1)

        for ip in ip_list:
            a = ip.split('.')

            # IP Validation
            if (len(a) == 4) and \
                    (1 <= int(a[0]) <= 223) and \
                    (int(a[0]) != 127) and \
                    (int(a[0]) != 169 or int(a[1]) != 254) and \
                    (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
                print "IP: {} is valid".format(ip.strip('\n'))
                continue

            else:
                print '\n[FAIL] IP {} is INVALID. Please enter correct IPs and try again!'.format(ip)
                break

        # Go out of loop if no break statement occurred in above for loop
        # <Check Python documentation for 'for-else'>
        else:
            break
        continue

    # Checking IP reachability
    print "\n Checking IP reachability..."

    while True:
        for ip in ip_list:
            ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip])

            if ping_reply == 0:
                continue

            elif ping_reply == 2:
                print "\n [FAIL] No response from device {}.".format(ip)
                break

            else:
                print "\n[FAIL] Ping to the following device has FAILED:", ip
                break

        # Go out of loop if no break statement occurred in above for loop
        # <Check Python documentation for 'for-else'>
        else:
            print '\n[SUCCESS] All devices are reachable.'
            break
        print "[FAIL] Please re-check IP address list or device."
        ip_is_valid()
    return


# Checking user file validity
def user_is_valid():
    global user_file

    while True:

        user_file = raw_input("Enter filename containing username and password: ")

        if os.path.isfile(user_file):
            print "\n[SUCCESS] File existence validated"
            break

        else:
            print "\n[FAIL] File {} does not exist! Please recheck file name".format(user_file)
            continue


# Checking command file validity
def cmd_is_valid():
    global cmd_file

    while True:

        cmd_file = raw_input("Enter filename of the file containing commands: ")

        if os.path.isfile(cmd_file):
            print "\n[SUCCESS] Sending commands to device..."
            break

        else:
            print "\n[FAIL] File {} does not exist! Please check filename and try again!\n".format(cmd_file)
            continue


# Make sure SSHv2 is enabled on the routers
def open_ssh_conn(ip):
    try:
        with open(user_file, 'r') as selected_user_file:
            selected_user_file.seek(0)
            username = selected_user_file.readlines()[0].split(',')[0]
            selected_user_file.seek(0)
            password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")

        # Setup SSh session
        session = paramiko.SSHClient()

        # For project purpose only:
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        session.connect(ip, username=username, password=password)
        connection = session.invoke_shell()

        connection.send("terminal length 0\n")
        time.sleep(1)
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)

        with open(cmd_file, 'r') as selected_cmd_file:
            selected_cmd_file.seek(0)

            for each_line in selected_cmd_file.readlines():
                connection.send(each_line + '\n')
                time.sleep(2)

        # Checking SSH output for syntax errors
        router_output = connection.recv(65535)

        if re.search(r"% Invalid input detected at", router_output):
            print "[FAIL] There was at least one syntax error on device {}".format(ip)

        else:
            print "\n[SUCCESS] Configured device {}".format(ip)

        # Closing the connection
        session.close()

    except paramiko.AuthenticationException:
        print "[FAIL] Invalid username/password or configuration"
        print "Recheck and try again. Closing program...\n"


if __name__ == '__main__':
    try:
        ip_is_valid()
        user_is_valid()
        cmd_is_valid()
        for ip in ip_list:
            open_ssh_conn(ip)

    except KeyboardInterrupt:
        print "\n[FAIL] Program aborted by user. Exiting...\n"
        sys.exit()
