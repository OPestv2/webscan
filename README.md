SimpleScanner is a python script used to scan given host's ports.<br> 
It returns ports state like open / closed.

Usage syntax:<br>
python webscan --help<br>
python webscan -h <i>host</i> -p <i>port</i>

Ports can be specified as single value, sequence, range, full range or combined.<br>
Examples:<br>
single value    "3"<br>
sequence        "20,21,80,88,139"<br>
range           "200-299"<br>
full range      "-"<br>
combined        "1,2,3,10-39,41,42,50-55"<br>

It is necessary to use " " to specify both host and ports parameters.

Script created using Python 3.9


Logging syntax:
[i]     - information
[?]     - question; answer using one of options in [ ]
[!]     - warning; it does not terminate the program
[!!!]   - critical; but it does