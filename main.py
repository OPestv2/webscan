#!/bin/python

import optparse
import os
import sys

from scanner import Scanner

MAX_PORT = 65536
MIN_PORT = 0

HELP = """
webscan is a simple port scanner

Set port / ports using syntax: exact value(s) 4,5,6,7 OR range 4-7 OR combined 4,6,8-20 OR - for 0-65535 (full range)
Additionally you can specify a part of full range e.g. 10000- means 10000-65535
1,2,3-5,100- is equal to [1,2,3,4,5,100,101,102,...,65535]

Examples:
python webscan -h
python webscan -H 127.0.0.1 -P 10
python webscan -H localhost -P 80
python webscan -H www.google.com -P 80,443


Scanner proceeds only one host per run.

=====================================
Not added yet

-t, --timeout       Timeout


"""

"""
resolve_ports rewrites port sequences and ranges to port list used in scan
"""


def resolve_ports(ports):
    # divide PORT string to
    port_packets = ports.split(",")
    # initialize array of ports and set them 'not used'
    result = [False] * MAX_PORT

    # if port number occurs more than once raise overwrite warning
    overwrite_warning = False
    overwrite_occurrences = 0

    for port_packet in port_packets:
        try:
            # look for range
            if port_packet.__contains__("-"):
                range_bounds = port_packet.split("-")
                # possible AttributeError occurrence (range can have maximum 2 bounds)
                if len(range_bounds) > 2:
                    raise AttributeError("Maximum one '-' per port range allowed")

                # possible TypeError occurrence while casting to integer
                start = MIN_PORT
                if range_bounds[0] != "":
                    start = int(range_bounds[0])
                    if start > MAX_PORT or start < MIN_PORT:
                        raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
                end = MAX_PORT
                if range_bounds[1] != "":
                    end = int(range_bounds[1]) + 1
                    if end > MAX_PORT or end < MIN_PORT:
                        raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))

                for i in range(start, end):
                    if result[i] is True:
                        overwrite_warning = True
                        overwrite_occurrences += 1
                    result[i] = True

            else:
                # possible TypeError occurrence while casting to integer
                specified_port = int(port_packet)
                if specified_port > MAX_PORT or specified_port < MIN_PORT:
                    raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))

                if result[specified_port] is True:
                    overwrite_warning = True
                    overwrite_occurrences += 1
                result[specified_port] = True

        except (AttributeError, ValueError) as e:
            print("[!] There is an error in port: '%s'. %s" % (port_packet, e))
            choice = input("[?] Do you want to skip this element and continue? [y/N] ")
            if choice == 'n' or choice == 'N' or choice == "":
                return None

    if overwrite_warning is True:
        print("[!] %d port numbers occurred more than once while resolving port ranges" % overwrite_occurrences)

    # rewrite result array to exact values list

    result_array = []
    for i in range(MIN_PORT, MAX_PORT):
        if result[i] is True:
            result_array.append(i)

    return result_array

def resolve_hosts(hosts):
    # divide PORT string to
    host_packets = hosts.split(",")
    # initialize array of ports and set them 'not used'
    result = []

    result.append(hosts)
    return result

    # # if port number occurs more than once raise overwrite warning
    # overwrite_warning = False
    # overwrite_occurrences = 0
    #
    # for port_packet in port_packets:
    #     try:
    #         # look for range
    #         if port_packet.__contains__("-"):
    #             range_bounds = port_packet.split("-")
    #             # possible AttributeError occurrence (range can have maximum 2 bounds)
    #             if len(range_bounds) > 2:
    #                 raise AttributeError("Maximum one '-' per port range allowed")
    #
    #             # possible TypeError occurrence while casting to integer
    #             start = MIN_PORT
    #             if range_bounds[0] != "":
    #                 start = int(range_bounds[0])
    #                 if start > MAX_PORT or start < MIN_PORT:
    #                     raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
    #             end = MAX_PORT
    #             if range_bounds[1] != "":
    #                 end = int(range_bounds[1]) + 1
    #                 if end > MAX_PORT or end < MIN_PORT:
    #                     raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
    #
    #             for i in range(start, end):
    #                 if result[i] is True:
    #                     overwrite_warning = True
    #                     overwrite_occurrences += 1
    #                 result[i] = True
    #
    #         else:
    #             # possible TypeError occurrence while casting to integer
    #             specified_port = int(port_packet)
    #             if specified_port > MAX_PORT or specified_port < MIN_PORT:
    #                 raise AttributeError("Values in range %d - %d allowed" % (MIN_PORT, MAX_PORT))
    #
    #             if result[specified_port] is True:
    #                 overwrite_warning = True
    #                 overwrite_occurrences += 1
    #             result[specified_port] = True
    #
    #     except (AttributeError, ValueError) as e:
    #         print("[!] There is an error in port: '%s'. %s" % (port_packet, e))
    #         choice = input("[?] Do you want to skip this element and continue? [y/N] ")
    #         if choice == 'n' or choice == 'N' or choice == "":
    #             return None
    #
    # if overwrite_warning is True:
    #     print("[!] %d port numbers occurred more than once while resolving port ranges" % overwrite_occurrences)
    #
    # # rewrite result array to exact values list
    #
    # result_array = []
    # for i in range(MIN_PORT, MAX_PORT):
    #     if result[i] is True:
    #         result_array.append(i)

if __name__ == '__main__':
    try:
        # constructor argument is usage hint
        parser = optparse.OptionParser("python webscan -H <host> -P <port>" + HELP)
        # set HOST option
        parser.add_option('-H', '--host', dest='host', type='string', help='Target host')
        # set PORT option
        parser.add_option('-P', '--port', dest='port', type='string', help='Target port(s)')
        # set TIMEOUT option
        parser.add_option('-T', '--timeout', dest='timeout', type='int', help='Single connection timeout')
        # toggle HIDE CLOSED ports

        # toggle HI

        # parse arguments
        (options, args) = parser.parse_args()

        # check if required parameters are set
        hosts = options.host
        ports = options.port


        if hosts is None or ports is None:
            print("[!!!] Error. Required 2 parameters, usage: " + parser.usage)
            sys.exit(0)

        # resolve ports
        ports = resolve_ports(ports)
        # resolve hosts
        hosts = resolve_hosts(hosts)

        print("[i] Port list contains %d element(s)" % len(ports))
        if len(ports) == 0:
            print("[!!!] No ports to scan. Abort")

        # run scanner
        scanner = Scanner(hosts, ports)
        scanner.scan()

    except KeyboardInterrupt as e:
        print("[i] Ctrl+C means Good Bye!")
        exit(0)
