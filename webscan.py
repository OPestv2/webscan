#!/bin/python

import optparse
import sys

from resolver import Resolver
from scanner import Scanner

HELP = """
webscan is a simple port scanner

Syntax: webscan [-h | --help] -H hosts -P ports [-T time | --timeout=time] [-c | --show-closed] [-o | --hide-open]
"""

if __name__ == '__main__':
    # Resolver class is used to rewrite hosts and ports parameters on hosts and ports lists used in scan
    resolver = Resolver()

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

        # parse arguments
        (options, args) = parser.parse_args()

        # check if required parameters are set
        hosts = options.host
        ports = options.port
        timeout = options.timeout
        show_closed = options.show_closed
        hide_open = options.hide_open

        if hosts is None or ports is None:
            print("[!!!] Error. Required HOST and PORT parameters, usage: " + parser.usage)
            sys.exit(0)

        # cast timeout to int
        if timeout is not None:
            try:
                timeout = int(timeout)
            except ValueError:
                print("[!!!] Timeout value must be an integer. Abort")
                sys.exit(0)

        # resolve ports
        ports = resolver.resolve_ports(ports)
        # resolve hosts
        hosts = resolver.resolve_hosts(hosts)

        print("[i] Ports list contains %d element(s)" % len(ports))
        if len(ports) == 0:
            print("[!!!] No ports to scan. Abort")

        print("[i] Hosts list contains %d element(s)" % len(hosts))
        if len(hosts) == 0:
            print("[!!!] No hosts to scan. Abort")

        # run scanner
        scanner = Scanner(hosts, ports, timeout, show_closed, hide_open)
        scanner.scan()

    except KeyboardInterrupt as e:
        print("[i] Ctrl+C means Good Bye!")
        exit(0)
