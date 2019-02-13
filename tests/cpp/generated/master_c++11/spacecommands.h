'''
 WARNING: This file is autogenerated by SpaceCommander

 Any changes will be overwritten!
'''

import struct
import serial
import time
from enum import Enum


class COMMANDS(Enum):
    SPCMD_HEARTBEAT = 0
    SPCMD_HASH = 1
    SPCMD_COMMAND_SEND_BYTE = 2
    SPCMD_COMMAND_RECV_BYTE = 3
    SPCMD_COMMAND_ECHO = 4
    SPCMD_COMMAND_BIGTEST = 5

    
class MasterBase:
    def __init__(self, port):
        self._ser = serial.serial_for_url(port,
                                          baudrate=9600,
                                          parity=serial.PARITY_NONE,
                                          do_not_open=True)

    
    # User functions
    # --------------------------------------------------
    def begin(self):
        self._ser.open()
        if not self.test_hash():
            self._ser.close()
            
    def close(self):
        self._ser.close()

    def test_hash(self):
        hash_val = self._hash_command()
        if hash_val != 0x40419b8b99b1c6e8:
            print('Hash Mismatch! Received hash {} but expected {}. Ensure both host and device are the same version.'.format(hex(hash_val), b'40419b8b99b1c6e8'.upper()))
            return False
        return True

    # Callbacks
    # --------------------------------------------------
    # Callback called before initiating a write to a slave
    def pre_write_cb(self, command, *data):
        pass

    # Callback called after finishing a write to a slave
    def post_write_cb(self, command, *data):
        pass

    # Callback called before initiating a read from a slave
    def pre_read_cb(self):
        pass

    # Callback called after finishing a read from a slave
    def post_read_cb(self, *data):
        pass
        
    # Commands
    # --------------------------------------------------
    def send_byte(self, b):
        """
        Send a byte to the slave

        Arguments:
        b (uint8) -- Byte to be sent
        """
        self._write_packet(COMMANDS.SPCMD_COMMAND_SEND_BYTE, 'B', b)
        ret_val = self._read_packet('')

    def recv_byte(self):
        """
        Receive a byte from the slave
        
        Returns:
        b (uint8) -- Received byte
        """
        self._write_packet(COMMANDS.SPCMD_COMMAND_RECV_BYTE, '')
        ret_val = self._read_packet('B')
        return ret_val[0]

    def echo(self, send):
        """
        Send string to slave and read it back

        Arguments:
        send (uint32) -- No description provided
        
        Returns:
        recv (uint32) -- No description provided
        """
        self._write_packet(COMMANDS.SPCMD_COMMAND_ECHO, 'I', send)
        ret_val = self._read_packet('I')
        return ret_val[0]

    def bigtest(self, b1, b2):
        """
        No description provided

        Arguments:
        b1 (uint32) -- No description provided
        b2 (uint32) -- No description provided
        
        Returns:
        b3 (uint32) -- No description provided
        """
        self._write_packet(COMMANDS.SPCMD_COMMAND_BIGTEST, 'II', b1, b2)
        ret_val = self._read_packet('I')
        return ret_val[0]

    
    # Internal functions
    # --------------------------------------------------
    def _write_packet(self, command_name, format_string, *data):
        self.pre_write_cb(command_name, *data)
        packet_format = ''.join(['<B', format_string])
        packed_struct = struct.pack(packet_format, command_name.value, *data)
        self._ser.write(packed_struct)
        self.post_write_cb(command_name, *data)

    def _read_packet(self, format_string):
        self.pre_read_cb()
        packet_format = ''.join(['<', format_string])
        num_bytes = struct.Struct(packet_format).size
        packet = self._ser.read(num_bytes)
        # Read failed either due to timeout or transmission error
        if len(packet) != num_bytes:
            print("Packet read failed")
            #raise # READ ERROR
        data = struct.unpack(packet_format, packet)
        self.post_read_cb(data)
        return data

    def _hash_command(self):
        self._write_packet(COMMANDS.SPCMD_HASH, '')
        return self._read_packet('Q')[0]
