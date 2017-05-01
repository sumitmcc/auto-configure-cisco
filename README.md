# Auto-configure Cisco routers from Python

The program mainly consists of 3 parts:
* Providing router IPs to be configured
* Providing Username and Password for SSH
* Providing commands to be executed
* Execution of the program

1. Providing IPs of routers to be configured: 
The user has a choice to provide IPs manually or parse from a file for larger number of IPs. The program checks for validity of IP addresses. If any of them is of invalid format, inform the user to correct the specific IP and restart the program. Once all the IPs are confirmed to be of valid format, they are pinged individually to check if they are reachable. Any unreable IP would be informed to the user to be corrected. Once all the IP addresses are confirmed to be reachable, the next step is:

2. Provide Username and Password:
This functionality is currently restricted to parsing from a text file only. *(I might, in future, add an option for user to manually type the username and password)* The user is prompted to enter the filename that contains the username and password. Note that the program requires the username and password to be formatted in the textfile as: ``` username,password ```
The program then checks if the given file exists. If not, the user is informed of the error. Once validated, the program proceeds to the next step. Note that the actual authentication of the username and password does not occur at this step.

3. Providing commands to be executed:
The program promps the user to enter the filename of the file that contains the commands to be executed in the router terminal. Note that the program requires that commands be written in a text file with one command per line and no indentation whatsoever. Also the last line needs to have a trailing newline. The existence of the file is validated and in case it is an invalid name, the user is informed of the invalidity. Once the filename is validated, the program continues to execute all the defined functions. Note again that, only the filename is validated at this step and not the actual commands in the file.

4. Execution of the commands:
The program opens an SSH connection for each IP address and executes the commands line-by-line. Invalid authentication is handld by the ``` paramiko.AuthenticationException: ``` exception handler. Any invalid syntax is detected by the search for the term ``` % Invalid input detected at``` in the terminal output using regular expressions.

## Getting Started

Download the program and place it into desired folder. 

If you're using Linux/MAC OS, open terminal and browse to the downloaded folder and run ``` python ssh_config.py ```.
if you're using windows, make sure you have Python2.7 set up (See [Python installation on windows](http://stackoverflow.com/a/21373411/7586417) ). Open command prompt and browse to the installed folder and run ``` python ssh_config.py ```

Make sure you have the following files:
* File containing the IP addresses (If you choose autoconfigure)
* File containing username and password
* File containing the commands

Furthermore, all the above files should be contained in the same folder as the code for the file detection.

### Prerequisites

This program requires you to install the paramiko module for Python. See [Paramiko Installation](http://www.paramiko.org/installing.html) for details on installation.

The inbuilt libraries used are: *os.path, subprocess, time, sys* and * re*

You should also make sure you have the connectivity to the router you wish to configure. Use ping to make sure you are connected.
In case you wish to test the program without using a physical router, you need to install GNS3 (See [GNS3 installation](https://www.gns3.com/support/docs/quick-start-guide-for-windows-us) for installation guide). Connect the routers in the GNS3 to a virtual machine and execute the following code in the virtual machine terminal.

Your configuration would look something like this:
![Alt GNS3 Configuration](https://image.ibb.co/cRKyOv/GNS3.png "GNS3 configuration")


## Running the program

When the program is run, the following prompt is obtained:

``` Do you want to configure manually or use auto-configuration file? Type:
 1 for Manual Configuration
 2 for auto-configuration 
 ```
If you choose 1, your next prompt should be: ``` Enter IP addresses of routers to configure. Enter 'done' when finished ```
Type the IP addresses with an Enter after every IP address and 'done' when finished.


If you choose 2, your next prompt would be: ``` Enter IP file name and extension: ```
Enter the filename of the file that contains the IP addresses


If all went well, your terminal should now display the success code: ``` [SUCCESS] All devices are reachable.```


Then there would be a prompt to enter the filename of the file that contains username and password: ``` Enter filename containing username and password: ```

After validation of this file, the program prompts for filename of file that contains the commands: ``` Enter filename of the file containing commands: ```

The program then opens an SSH connection to each IP address and executes the commands in the file.



### Example

A run of whole program looks like this:
```
Do you want to configure manually or use auto-configuration file? Type:
 1 for Manual Configuration
 2 for auto-configuration 
2
Enter IP file name and extension: ipaddress.txt
IP: 192.168.2.1 is valid
IP: 192.168.2.2 is valid
IP: 192.168.2.3 is valid
IP: 192.168.2.4 is valid
IP: 192.168.2.5 is valid

 Checking IP reachability...
PING 192.168.2.1
 (192.168.2.1) 56(84) bytes of data.

--- 192.168.2.1
 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 10.616/18.753/26.891/8.138 ms
PING 192.168.2.2
 (192.168.2.2) 56(84) bytes of data.

--- 192.168.2.2
 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 5.763/36.649/67.536/30.887 ms
PING 192.168.2.3
 (192.168.2.3) 56(84) bytes of data.

--- 192.168.2.3
 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 3.328/4.331/5.335/1.005 ms
PING 192.168.2.4
 (192.168.2.4) 56(84) bytes of data.

--- 192.168.2.4
 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 9.092/19.044/28.996/9.952 ms
PING 192.168.2.5
 (192.168.2.5) 56(84) bytes of data.

--- 192.168.2.5
 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 6.155/21.128/36.101/14.973 ms

[SUCCESS] All devices are reachable.
Enter filename containing username and password: userpass.txr

[FAIL] File userpass.txr does not exist! Please recheck file name
Enter filename containing username and password: userpass.txt

[SUCCESS] File existence validated
Enter filename of the file containing commands: commands.txt

[SUCCESS] Sending commands to device...

[SUCCESS] Configured device 192.168.2.1


[SUCCESS] Configured device 192.168.2.2


[SUCCESS] Configured device 192.168.2.3


[SUCCESS] Configured device 192.168.2.4


[SUCCESS] Configured device 192.168.2.5
```

## Configurable parameters:
* Incase your ping takes a longer time to respond then please increse the ping parameter '-w' to higher number so that the wait-time is increased.
* The line ```session.set_missing_host_key_policy(paramiko.AutoAddPolicy())``` automatically adds the host key. This is not recommended in the production environment and is usually considered a security threat.
* The command ```connection.send("terminal length 0\n")``` is given to avoid pagination in the router terminal which may cause unwanted errors in case the output is large.

## Author

* **Sumit Chachadi** -*sumitmal@buffalo.edu*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


