Webscan is a python script used to scan ports of given host. 
It returns ports states like **open** / **closed** / **filtered** (like Nmap does).

Usage syntax:
python webscan -h
python webscan -H host -P port

Logging syntax:
[i]     - information
[?]     - question, answer using one of the options in [ ]
[!]     - warning; it does not terminate the program
[!!!]   - critical; but it does

Script created using Python 3.9
