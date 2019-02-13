
import argparse
from generated.slave_python3.spacecommands import SlaveBase

b = 0

class Slave(SlaveBase):
    def send_byte_cb(self, in_b):
        print("Received byte!")
        print(in_b)
        global b
        b = in_b

    def recv_byte_cb(self):
        print("Sending byte!")
        return b

    def echo_cb(self, in_send_string):
        print("Echoing")
        print(in_send_string)
        return in_send_string

def main(port):
    slave = Slave(port, 1)
    slave.begin()
    while True:
        slave.process_commands()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    args = parser.parse_args()
    main(args.port)

