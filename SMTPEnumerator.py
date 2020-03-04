#!/usr/bin/python3
import socket
import sys

class SmtpUserEnum():

    def __init__(self, input):
        self.usernames = []

        self.address = input.get("address", None)
        self.port = input.get("port", 25)
        username = input.get("username", None)
        if username != None:
            self.usernames.append(username)
        wordlist = input.get("wordlist", None)
        if wordlist != None:
            with open(wordlist) as f:
                self.usernames.extend(f.readlines())
        self.verbose = input.get("verbose", False)

    def main(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))
        banner = s.recv(1024)
        if self.verbose:
            print(banner.decode())
        for user in self.usernames:
            result = ""
            err_code = ""
            username = user.rstrip('\n')
            send_content = bytearray('VRFY ' + username + '\r\n', 'utf-8', 'ignore')
            try:
                s.send(send_content)
                result = s.recv(1024).decode('utf-8')
            except ConnectionResetError as ex:
                if self.verbose:
                    print(ex.strerror + "\nReconnecting...")
                s.close()
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.address, self.port))
                s.recv(1024) # banner
                s.send(send_content)
                result = s.recv(1024).decode('utf-8')

            err_code = result.split(' ')[0]    
            if err_code[0] == "2":
                if self.verbose:
                    print("\033[32m[+] " + username + " - " + result.rstrip('\n') + "\033[0m")
                else:
                    print(username)
            elif err_code[0] == "4":
                self.usernames.append(username)
            elif self.verbose:
                print("[-] " + username + " - " + result.rstrip('\n'))
        s.close()

def print_help():
    print("Usage: python3 smtpuserenum.py ip [-p] [-u] [-w] [-v]")
    print("\n\tip: ip address")
    print("\t-p: port")
    print("\t-u: username")
    print("\t-w: user wordlist")
    print("\t-v: verbose - print out failed attempts")

def parse_input(input):
    input_dict = {}
    try:
        address = input[1]
        input_dict["address"] = address
        if "-p" in input:
            input_dict["port"] = input[input.index("-p") + 1]
        if "-u" in input:
            input_dict["username"] = input[input.index("-u") + 1]
        if "-w" in input:
            input_dict["wordlist"] = input[input.index("-w") + 1]
        if "-v" in input:
            input_dict["verbose"] = True
        else:
            input_dict["verbose"] = False
    except Exception as ex:
        print("Unable to parse input: " + ex)
        print_help()
        sys.exit(0)
    return input_dict

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print_help()
        sys.exit(0)
    else:
        input = parse_input(sys.argv)
        ObjName = SmtpUserEnum(input)
        ObjName.main()
