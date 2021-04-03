import argparse
import subprocess

def start_jacktrip_client(server_ip):
    print("Starting jacktrip client connection...")
    subprocess.check_call(f".\jacktrip.exe -C {server_ip} -v")
    print("jacktrip Session is over.")

def main():
    print("### Launching Jacktrip client ###")
    parser = argparse.ArgumentParser()
    parser.add_argument("server_ip", help="JackTrip Server IP")
    parser.add_argument("--retry", action="store_true", help="Try to start a new session if this one fails.")
    args = parser.parse_args()

    while True:
        start_jacktrip_client(args.server_ip)
        if not args.retry:
            break




