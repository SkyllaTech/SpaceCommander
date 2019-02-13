
import argparse
from generated.master_python3.spacecommands import MasterBase


class Master(MasterBase):
    def p(self):
        pass
    
def main(port):
    master = Master(port)
    master.begin()
    input()
    print("Starting recv")
    print(master.recv_byte())
    input()
    print("Starting send")
    master.send_byte(10)
    input()
    print("Starting recv")
    print(master.recv_byte())
    input()
    print("Starting echo")
    print(master.echo('c').decode())
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("port")
    args = parser.parse_args()
    main(args.port)
