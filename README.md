# SMTPEnumerator
Gather usernames against a remote SMTP service.

Only use if given explicit permission to test against target host.

Usage: python3 smtpuserenum.py ip [-p] [-u] [-w] [-v]

	ip: ip address (required, no flag)
	-p: port
	-u: username
	-w: user wordlist
	-v: verbose - print out failed attempts
