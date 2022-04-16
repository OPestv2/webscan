import socket
import sys
from _socket import gethostbyname
import time
from threading import Thread


class Scanner:
    def __init__(self, hosts, ports):
        self.hosts = hosts
        self.ports = ports

        self.timeout = 1
        # dictionary for open and closed ports list assigned to specified host (later more hosts)
        self.result_array = {}
        for host in hosts:
            self.result_array[host] = ([], [])

    # public function used to start scan
    def scan(self):
        self.__scan_thread_dispatcher()

    # private function used to start separate threads for scanning
    def __scan_thread_dispatcher(self):
        # count full execution time
        start_time = time.time()

        for host in self.hosts:
            try:
                ip = gethostbyname(host)
                print("[i] Scanning host '%s' (%s)" % (host, ip))
            except:
                print("[!!!] Could not recognize host '%s'" % host)
                sys.exit(0)

            # create threads pool
            threads = []
            # create threads and start
            for port in self.ports:
                thread = Thread(target=self.__scan_port, args=(host, int(port)))
                threads.append(thread)
                thread.start()

            # wait for all threads finish their job
            for thread in threads:
                thread.join(self.timeout+1)

            # summarise results
            print("\n[i] Scanned %d ports" % len(self.ports))
            print("[i] Found %d open ports: " % len(self.result_array[host][0]))
            for msg in self.result_array[host][0]:
                print(msg)
            print("\n[i] Found %d closed ports: " % len(self.result_array[host][1]))
            for msg in self.result_array[host][1]:
                print(msg)

        end_time = time.time()

        print("\n[i] Script executed in %.2f seconds" % (end_time - start_time))

    def __scan_port(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(self.timeout)
            conn = s.connect((host, port))
            self.result_array[host][0].append(f"[+] Port {port} is open")
        except Exception as e:
            self.result_array[host][1].append(f"[-] Port {port} is closed. Reason: {e}")
        finally:
            s.close()



