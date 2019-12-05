import paramiko
import logging
import time
import getpass
import os
import sys
host='somehost'
username='someuser'
password='somepassword'
port=22
keyfile_path = 'private_key_file'
#command={"RunVM1ORDGEN":"/users/gen/abpwrk1/RunJobs VM1ORDGEN BYREQ",
#          "pingABPServer":"/users/gen/abpwrk1/J2EEServer/config/ABP-FULL/ABPServer/scripts/pingABPServer.sh"}
#command="RunJobs VM1ORDGEN BYREQ"
chan =None
WAIT_TIME=20

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
            tran=ssh.get_transport()
            print type(tran),tran
            if ssh.get_transport().is_active():
                print "transport connection is ACtive"
                logging.info('transport connection is ACtive')

            print "Invoking shell"
            logging.info('Invoking shell')
            chan=ssh.invoke_shell()
            f = chan.makefile()
            #chan.get_pty()
            chan.settimeout(WAIT_TIME)
            print  ("Sending Unix command '%s' (via shell)" % command)
            time.sleep(2)
            logging.info('Sending unix command [%s] via shell',command)
            recv=chan.send(command+ os.linesep)# + ochannel.sends.linesep  send works send all doesn't work
            time.sleep(2)
            #print chan.recv_exit_status()
            """
            buf = ''
            while chan.recv_ready():
                buf += chan.recv(1024)
            print buf, type(buf)
            """
    finally:
        if ssh is not None:
            tran.atfork()
            logging.info('Closing transport')
            print 'Closing transport'
            chan.close()
            logging.info('Closing Channel')
            print 'Closing Channel'
            # Close client connection.
            ssh.close()
            logging.info("Close ssh conection to host:[%s] ,user: [%s] " ,host,username)
            print("Close ssh conection to host:%s  " % host)

#if __name__ == "__main__":
#    execute_ssh_command(host, port, username, password, None, None,command)
