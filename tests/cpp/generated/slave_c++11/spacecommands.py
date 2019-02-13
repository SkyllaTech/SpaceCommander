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


class SlaveBase:
    def __init__(self, port):
        self._ser = serial.serial_for_url(port,
                                          baudrate=9600,
                                          parity=serial.PARITY_NONE,
                                          timeout=1000,
                                          do_not_open=True)

        self._commands = {
            COMMANDS.SPCMD_HEARTBEAT: self._heartbeat_command,
            COMMANDS.SPCMD_HASH: self._hash_command,
            COMMANDS.SPCMD_COMMAND_SEND_BYTE: self._send_byte,
            COMMANDS.SPCMD_COMMAND_RECV_BYTE: self._recv_byte,
            COMMANDS.SPCMD_COMMAND_ECHO: self._echo,
            COMMANDS.SPCMD_COMMAND_BIGTEST: self._bigtest,
        }
        self._heartbeat_count = 0
        self._heartbeat_max = 1 << 8

    # User functions
    # --------------------------------------------------
    def begin(self):
        self._ser.open()
            
    def close(self):
        self._ser.close()

    def process_commands(self):
        if self._ser.in_waiting > 0:
            command_byte = self._ser.read(1)
            command_value = struct.unpack('<B', command_byte)
            command = COMMANDS(command_value[0])
            self._commands.get(command, self._bad_command)()

    # Callbacks
    # --------------------------------------------------
    # Callback called before initiating a write to master
    def pre_write_cb(self, *data):
        pass

    # Callback called after finishing a write to master
    def post_write_cb(self, *data):
        pass

    # Callback called before initiating a read from master
    def pre_read_cb(self):
        pass

    # Callback called after finishing a read from master
    def post_read_cb(self, *data):
        pass
    
    # Command callbacks
    # --------------------------------------------------
    def send_byte_cb(self):
        """
        Send a byte to the slave

        Returns:
        b (uint8) -- Byte to be sent
        """
        pass

    def recv_byte_cb(self, b):
        """
        Receive a byte from the slave
        
        Arguments:
        b (uint8) -- Received byte
        """
        pass

    def echo_cb(self, recv):
        """
        Send string to slave and read it back
        
        Arguments:
        recv (uint32) -- No description provided

        Returns:
        send (uint32) -- No description provided
        """
        pass

    def bigtest_cb(self, b3):
        """
        No description provided
        
        Arguments:
        b3 (uint32) -- No description provided

        Returns:
        b1 (uint32) -- No description provided
        b2 (uint32) -- No description provided
        """
        pass


    # Internal functions
    # --------------------------------------------------
    def _write_packet(self, format_string, *data):
        self.pre_write_cb(*data)
        packet_format = ''.join(['<', format_string])
        packed_struct = struct.pack(packet_format, *data)
        self._ser.write(packed_struct)
        self.post_write_cb(*data)

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

    def _bad_command(self):
        pass
    
    def _heartbeat_command(self):
        self._write_packet('B', self._heartbeat_count)

    def _hash_command(self):
        self._write_packet('Q', 0x40419b8b99b1c6e8)

    def _send_byte(self):
        ret_read = self._read_packet('B')
        ret_cb = self.send_byte_cb(*ret_read)
        self._write_packet('')

    def _recv_byte(self):
        ret_cb = self.recv_byte_cb()
        self._write_packet('B', ret_cb)

    def _echo(self):
        ret_read = self._read_packet('I')
        ret_cb = self.echo_cb(*ret_read)
        self._write_packet('I', ret_cb)

    def _bigtest(self):
        ret_read = self._read_packet('II')
        ret_cb = self.bigtest_cb(*ret_read)
        self._write_packet('I', ret_cb)

