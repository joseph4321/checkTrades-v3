# checkTrades-v3
Use the application api to search for the status of specific trades and find the matching counterparty trades if they exist.  A csv is output at the end for easier consumption

Example:
```text
root@30344c4e8208:/veris-support-scripts# python checkTrades-v3.py
[+] Looking for partyAtrade1 ...
[+] Trade partyAtrade1 is AutoPaired with partyBtrade1 with primary matching status Matched

[+] Looking for partyBtrade2 ...
[+] Trade partyBtrade2 is AutoPaired with partyAtrade2 with primary matching status Matched

[+] Looking for partyBtrade3 ...
[+] Trade partyBtrade3 is AutoPaired with partyAtrade3 with primary matching status Matched

[+] Looking for partyAtrade4 ...
[+] Trade partyAtrade4 is AutoPaired with partyBtrade4 with primary matching status Matched

[+] Looking for partyAtrade5 ...
[+] Trade partyAtrade5 is AutoPaired with partyBtrade5 with primary matching status Matched
```
