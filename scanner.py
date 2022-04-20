import socket
import sys
from _socket import gethostbyname, gethostbyaddr
import time
from datetime import datetime
from threading import Thread


class Scanner:
    def __init__(self, hosts, ports, timeout, show_closed=False, hide_open=False):
        # list of strings
        self.hosts = hosts
        # list of strings
        self.ports = ports
        self.timeout = 1
        if timeout is not None: self.timeout = timeout
        self.show_closed = show_closed
        self.hide_open = hide_open

        # dictionary for open and closed ports list assigned to specified host (later more hosts)
        self.result_array = {}
        for host in hosts:
            self.result_array[host] = ([], [])

    # public function used to start scan
    def scan(self):
        self.__scan_thread_dispatcher()

    # private function used to start separate threads for scanning
    def __scan_thread_dispatcher(self):
        for host in self.hosts:
            try:
                ip = gethostbyname(host)
                # if given host is IP address find its Domain Name
                if ip == host:
                    dn = gethostbyaddr(host)
                    print("[i] Scanning host '%s' (DN: %s)" % (host, dn[0]))
                    if len(dn[1]) > 0:
                        print("[i] Host aliases: " + str(dn[1]))
                else:
                    print("[i] Scanning host '%s' (IP: %s)" % (host, ip))
            except:
                print("[-] Could not connect or recognize host '%s'" % host)
                return

            # create threads pool
            threads = []
            # create threads and start
            for port in self.ports:
                thread = Thread(target=self.__scan_port, args=(host, int(port)))
                threads.append(thread)
                thread.start()

            # wait for all threads finish their job
            for thread in threads:
                thread.join(self.timeout + 1)

            # summarise results
            print("\n[i] Scanned %d port(s)" % len(self.ports))
            print("[i] Found %d open port(s): " % len(self.result_array[host][0]))
            if self.hide_open is False:
                for msg in self.result_array[host][0]:
                    print(msg)
            print("[i] Found %d closed port(s): " % len(self.result_array[host][1]))
            if self.show_closed is True:
                for msg in self.result_array[host][1]:
                    print(msg)

    def __scan_port(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(self.timeout)
            conn = s.connect((host, port))
            self.result_array[host][0].append(f"\t[+] Port {port} is open")
        except Exception as e:
            self.result_array[host][1].append(f"\t[+] Port {port} is closed. Reason: {e}")
        finally:
            s.close()
