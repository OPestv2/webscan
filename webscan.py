#!/bin/python

import optparse
import sys
import time

from resolver import Resolver
from scanner import Scanner

NAME = """
 __       __          __        ______                             
|  \  _  |  \        |  \      /      \                            
| ▓▓ / \ | ▓▓ ______ | ▓▓____ |  ▓▓▓▓▓▓\ _______  ______  _______  
| ▓▓/  ▓\| ▓▓/      \| ▓▓    \| ▓▓___\▓▓/       \|      \|       \ 
| ▓▓  ▓▓▓\ ▓▓  ▓▓▓▓▓▓\ ▓▓▓▓▓▓▓\\▓▓    \|  ▓▓▓▓▓▓▓ \▓▓▓▓▓▓\ ▓▓▓▓▓▓▓\ 
| ▓▓ ▓▓\▓▓\▓▓ ▓▓    ▓▓ ▓▓  | ▓▓_\▓▓▓▓▓▓\ ▓▓      /      ▓▓ ▓▓  | ▓▓
| ▓▓▓▓  \▓▓▓▓ ▓▓▓▓▓▓▓▓ ▓▓__/ ▓▓  \__| ▓▓ ▓▓_____|  ▓▓▓▓▓▓▓ ▓▓  | ▓▓
| ▓▓▓    \▓▓▓\▓▓     \ ▓▓    ▓▓\▓▓    ▓▓\▓▓    \ \ ▓▓   ▓▓ ▓▓  | ▓▓
 \▓▓      \▓▓ \▓▓▓▓▓▓▓\▓▓▓▓▓▓▓  \▓▓▓▓▓▓  \▓▓▓▓▓▓▓ \▓▓▓▓▓▓▓\▓▓   \▓▓ v1.0
                                                                   
    by OPest 
"""


HELP = """
Webscan is a simple port scanner used to scan single or multiple hosts 

Syntax: webscan [-h | --help] -H hosts -P ports [-T time | --timeout=time] 
                [-c | --show-closed] [-o | --hide-open]
                [[-y | --err_continue] | [-n | --err_stop]]
"""

if __name__ == '__main__':
    print(NAME+"\n")

    try:
        # constructor argument is usage hint
        parser = optparse.OptionParser(HELP)
        # set HOST option
        parser.add_option('-H', '--host', dest='host', type='string', help='Target host(s)')
        # set PORT option
        parser.add_option('-P', '--port', dest='port', type='string', help='Target port(s)')
        # set TIMEOUT option
        parser.add_option('-T', '--timeout', dest='timeout', type='int', help='Single connection timeout')
        # toggle SHOW CLOSED ports
        parser.add_option('-c', '--show-closed', action="store_true", dest='show_closed', help="Show list of closed "
                                                                                               "ports", default=False)
        # toggle HIDE OPEN ports
        parser.add_option('-o', '--hide-open', action="store_true", dest='hide_open', help="Hide list of open ports",
                          default=False)
        # set onerror CONTINUE
        parser.add_option('-y', '--err-continue', action="store_true", dest='err_continue',
                          help="Continue script execution if error occurs")
        # set onerror STOP
        parser.add_option('-n', '--err-stop', action="store_true", dest='err_stop',
                          help="Abort script execution if error occurs")

        # parse arguments
        (options, args) = parser.parse_args()

        # start counting time
        start_time = time.time()
        localtime = time.asctime(time.localtime(start_time))
        print("[i] Script started at %s\n" % localtime)

        # check if required parameters are set
        hosts = options.host
        ports = options.port
        timeout = options.timeout
        show_closed = options.show_closed
        hide_open = options.hide_open
        err_continue = options.err_continue
        err_stop = options.err_stop

        # check if hosts and ports are non empty
        if hosts is None or ports is None:
            print("[!!!] Error. Required HOST and PORT parameters, usage: " + parser.usage, file=sys.stderr)
            sys.exit(0)

        # check if woman is running script (choice confusion)
        if err_continue is True and err_stop is True:
            print("[!!!] You can not force to continue and abort execution at the same time! Idk what to do...",
                  file=sys.stderr)
            sys.exit(0)

        # cast timeout to int
        if timeout is not None:
            try:
                timeout = int(timeout)
                # and check if it is positive value
                if timeout < 1:
                    raise ValueError("Timeout must be integer and >= 1")
            except ValueError as e:
                print("[!!!] %s. Abort" % e, file=sys.stderr)
                sys.exit(0)

        # Resolver class is used to rewrite hosts and ports parameters on hosts and ports lists used in scan
        resolver = Resolver(err_continue, err_stop)

        # resolve ports
        ports = resolver.resolve_ports(ports)

        if ports is None or len(ports) == 0:
            print("[!!!] No ports to scan. Abort", file=sys.stderr)
            sys.exit(0)
        print("[i] Ports list contains %d element(s)" % len(ports))

        # resolve hosts
        hosts = resolver.resolve_hosts(hosts)

        if hosts is None or len(hosts) == 0:
            print("[!!!] No hosts to scan. Abort", file=sys.stderr)
            sys.exit(0)
        print("[i] Hosts list contains %d element(s)" % len(hosts))

        # run scanner
        scanner = Scanner(hosts, ports, timeout, show_closed, hide_open)
        scanner.scan()

        # count execution time
        end_time = time.time()
        localtime = time.asctime(time.localtime(end_time))
        print("\n[i] Script finished at %s and executed in %.2f seconds" % (localtime, (end_time - start_time)))

    except KeyboardInterrupt as e:
        print("\n[!] Ctrl+C means Good Bye!", file=sys.stderr)
        exit(0)
