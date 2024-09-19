import subprocess
import os
import sys
import time
import re
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        print("\n---- GET Request ----")
        print(f"Path: \033[32m{self.path}\033[0m")
        print(f"Query Parameters: \033[31m{query_params}\033[0m")

        self.send_response(200)

def strip_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def home_logo():
    print("""
        ####   ##     ##      ###        #####      #######     #######
         ##    ##     ##     ## ##      ##   ##    ##     ##   ##     ##
         ##    ##     ##    ##   ##    ##     ##   ##     ##   ##     ##
         ##    #########   ##     ##   ##     ##    #######     ########
         ##    ##     ##   #########   ##     ##   ##     ##          ##
         ##    ##     ##   ##     ##    ##   ##    ##     ##   ##     ##
        ####   ##     ##   ##     ##     #####      #######     #######

IHA089: Navigating the Digital Realm with Code and Security - Where Programming Insights Meet Cyber Vigilance.
    """)

def create_public_connection():
    file = "forward.txt"
    command = "ssh -R 80:0.0.0.0:4545 serveo.net -y > {} &".format(file)
    subprocess.Popen(command, shell=True)

def url_encode(text):
    return urllib.parse.quote(text)

def get_public_url():
    ffile = "forward.txt"
    file = open(ffile, 'r')
    read_data = file.read()
    #os.remove(ffile)
    file.close()
    new_data = read_data.replace("Forwarding HTTP traffic from", "")
    new_data = new_data.replace("\n","")
    new_data = new_data.replace("\r","")
    if new_data == "":
        print("Please restart.....")
        sys.exit()
    else:
        return new_data


def run(server_class=HTTPServer, handler_class=RequestHandler, port=4545):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    create_public_connection()
    time.sleep(7)
    k = get_public_url()
    if k!="0":
        k=k.replace(" ","")
        k = strip_ansi_escape_sequences(k).strip()
        print("Server public url ::: "+k)
    payload = input("Enter your payload :")
    encoded_payload = url_encode(payload)
    print(f"Encoded Payload:\033[31m{encoded_payload}\033[0m")
    print("Server running....")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Exiting....")
        sys.exit()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    home_logo()
    run()
