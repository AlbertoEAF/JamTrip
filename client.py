import argparse
import subprocess
import time

def start_jacktrip_client(server_ip):
    print("Starting jacktrip client connection...")
    subprocess.check_call(f".\jacktrip.exe -C {server_ip} -V")
    print("jacktrip Session is over.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("server_ip", help="JackTrip Server IP")
    parser.add_argument("--retry", action="store_true", help="Try to start a new session if this one fails.")
    args = parser.parse_args()

    print("### Launching Jacktrip client ###")

    while True:
        start_jacktrip_client(args.server_ip)
        if not args.retry:
            break
        else:
            print("\n\nSession ended. Starting a new one...\n\n")
            time.sleep(2)




if __name__ == "__main__":
    main()