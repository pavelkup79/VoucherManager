import paramiko
import time
import logging
import getpass
import sys
host='somehost'
username='someuser'
password='Usomepassword'
port=22
keyfile_path = 'private_key_file'
#command={"RunVM1ORDGEN":"/users/gen/abpwrk1/RunJobs VM1ORDGEN BYREQ",
 #          "pingABPServer":"/users/gen/abpwrk1/J2EEServer/config/ABP-FULL/ABPServer/scripts/pingABPServer.sh"}
command="/users/gen/abpwrk1/J2EEServer/config/ABP-FULL/ABPServer/scripts/pingABPServer.sh"
logging.basicConfig(filename='unixConnector.log',level=logging.DEBUG)


def execute_ssh_command(host, port, username, password, keyfilepath, keyfiletype, command):
    ssh = None
    key = None
    try:
        if keyfilepath is not None:
            # Get private key used to authenticate user.
            if keyfiletype == 'DSA':
                # The private key is a DSA type key.
                key = paramiko.DSSKey.from_private_key_file(keyfilepath)
            else:
                # The private key is a RSA type key.
                key = paramiko.RSAKey.from_private_key(keyfilepath)

        # Create the SSH client.
        ssh = paramiko.SSHClient()

        # Setting the missing host key policy to AutoAddPolicy will silently add any missing host keys.
        # Using WarningPolicy, a warning message will be logged if the host key is not previously known
        # but all host keys will still be accepted.
        # Finally, RejectPolicy will reject all hosts which key is not previously known.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the host.
        if key is not None:
            # Authenticate with a username and a private key located in a file.
            ssh.connect(host, port, username, None, key)
        else:
            # Authenticate with a username and a password.
            print "Creating ssh connection"
            ssh.connect(host, port, username, password)
            print "Invoking shell"
            ssh.invoke_shell()


        # Send the command (non-blocking)
        time.sleep(1)
        print "Executing unix command" +command
        stdin, stdout, stderr = ssh.exec_command(command)


        # Wait for the command to terminate
        while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
            time.sleep(1)
            print  "Wait for channel to be ready"
            print "stdout.channel.recv_ready() "+ str(stdout.channel.recv_ready())
            print "stdout.channel.exit_status_ready() " + str(stdout.channel.exit_status_ready())
        print "Ready to read output!!"
        print "stdout.channel.recv_ready() " + str(stdout.channel.recv_ready())
        print "stdout.channel.exit_status_ready() " + str(stdout.channel.exit_status_ready())
        stdoutstring = stdout.readlines()
        stderrstring = stderr.readlines()
        return stdoutstring, stderrstring
    finally:
        if ssh is not None:
            # Close client connection.
            ssh.close()
            print("Close ssh conection")



if __name__ == "__main__":
 (stdoutstring, stderrstring) = execute_ssh_command(host, port, username, password, None, None, command)
 for stdoutrow in stdoutstring:
   print stdoutrow
   status = str(stdoutstring[0][0:len(stdoutstring[0])-1])
   if status=="UP":
    print "ABP Server is UP"
 if  status == "DOWN" :
    print "ABP Server is DOWN"

 else :
    print stdoutstring[0]
"""
"""
if stdoutstring:
  status = str(stdoutstring[0][0:len(stdoutstring[0])-1])
  if status=="UP":
    print "ABP Server is UP"
  if  status == "DOWN" :
    print "ABP Server is DOWN"
  else :
    print stdoutstring[0]
#print stderrstring
if stderrstring:
   status = str(stderrstring[0][0:len(stderrstring[0])-1])
   print "Error returned from Unix: " + (stderrstring[0])

