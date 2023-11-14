# pyippprinter
Implements enough of the IPP (internet printing protocol) to emulate a network printer.

IPP version supported is IPP Everywhere.

Based on guide https://www.pwg.org/ipp/ippguide.html and https://ftp.pwg.org/pub/pwg/candidates/cs-ippig20-20150821-5100.19.pdf, as well as the formal spec here: https://ftp.pwg.org/pub/pwg/candidates/cs-ippeve10-20130128-5100.14.pdf.

The IPP server is written using django. It includes both the emulation server itself as well as a webpage for  monitoring the current queue. The default IP address is localhost, while the default port is 631. The project is run via the  web server waitress and uses an  SQLite database to record e.g. when a print job was accepted by whom. Documents to be printed are stored in a separate folder under `/data`. 


Mostly an excuse to learn about the internet printing protocol. Tested on Fedora 29 and Windows 10.
