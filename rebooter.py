"""
                           REBOOTER

    Reboots the machine when a card is marked as sick or dead
"""

import CGMinerClient
from time import sleep
import datetime, os, sys

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")

HOST = '127.0.0.1'
PORT = 4028
LOG_FILE = "rebooter_log.txt"
SECONDS_DELAY_BEFORE_STARTING = 90
SECONDS_BETWEEN_CHECKS = 30

#Incase of defunc cgminer prevents reboot, set this true
FORCE_REBOOT = 'false'

def send_command(command, parameter):
    client = CGMinerClient.CGMinerClient()
    return client.command(HOST, PORT, command, parameter)

def blind_command(command, parameter):
    client = CGMinerClient.CGMinerClient()
    client.blind_command(HOST, PORT, command, parameter)

def log(to_log):
    log_string = (datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S") +
                 ": " + str(to_log))
    print log_string
    try:
        log_file = open(LOG_FILE, "a")
        log_file.write(log_string + "\n")
        log_file.close()
    except IOError as e:
        print "!!!!!!ERROR ACCESSING LOG FILE!!!!"

def do_reboot(gpu_number, gpu_status):
    """
    One of more GPUs is sick/dead. Log it, close cgminer gracefully, then
      reboot
    """
    log("GPU {} is {}".format(gpu_number, gpu_status))
    if not FORCE_REBOOT:
        os.system("reboot")
    else:
        os.system("echo 1 > /proc/sys/kernel/sysrq; echo b > /proc/sysrq-trigger")
    log("Shutting down cgminer now and rebooting machine in 30 seconds...")
    blind_command('quit', '')
    sleep(5)
    sys.exit(0)

#Give cgminer time to start
sleep(SECONDS_DELAY_BEFORE_STARTING)

log("---------SESSION START----------")

while True:
    result = send_command('devs', '')
    gpunum = 0
    print ""
    for dev in result['DEVS']:
        print "{}: {} - {}".format(
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            gpunum, dev['Status'])
        if dev['Status'] != 'Alive':
            do_reboot(gpunum, dev['Status'])
            break
        gpunum += 1
    sleep(SECONDS_BETWEEN_CHECKS)
