import sys
import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral, DefaultDelegate
import hashlib
import hmac
import binascii

CODE_LOCK = 1;
CODE_UNLOCK = 2;
SERVICE_OPERATION_UUID             = '00001523-1212-efde-1523-785feabcd123'
CHARACTERISTIC_COMMAND_UUID        = '00001524-1212-efde-1523-785feabcd123' #where we write the commands
CHARACTERISTIC_COMMAND_HANDLE      = 0x0016
CHARACTERISTIC_ANGLE_STATUS_UUID   = '00001525-1212-efde-1523-785feabcd123' #Not used
CHARACTERISTIC_ANGLE_STATUS_HANDLE = 0x0018
CHARACTERISTIC_STATUS_UUID         = '00001526-1212-efde-1523-785feabcd123' #used to fetch nonce for signing
CHARACTERISTIC_STATUS_HANDLE       = 0x001b

class SesameSmartLockBTController:
    def __init__(self, user_name, mac_address, password):
        self.user_name = user_name
        self.user_hash = hashlib.md5(self.user_name.encode()).digest()
        self.mac_address = mac_address
        self.mac_data = bytearray.fromhex(self.mac_address.replace(':',' '))
        self.mac_data.reverse()
        self.password = password
        self.byte_password = bytearray.fromhex(self.password)
        
    def sign_payload(self, lock_code, nonce):
        hmac_sig = hmac.new(self.byte_password, digestmod=hashlib.sha256)
        byte_buffer = bytearray(59)
        byte_buffer[32:32+6] = self.mac_data
        byte_buffer[38:38+16] = self.user_hash
        byte_buffer[54:58] = nonce.to_bytes(4, 'little')
        byte_buffer[58] = lock_code
        hmac_sig.update(byte_buffer[32:])
        hmac_digest = hmac_sig.digest()
        byte_buffer[0:32] = hmac_digest
        print(binascii.hexlify(byte_buffer))
        return bytes(byte_buffer)
        
    def prepare_packets(self, lock_code, status_data):
        nonce = int.from_bytes(status_data[6:10], byteorder='little', signed=False) + 1
        msg = self.sign_payload(lock_code, nonce)
        packets = []
        i = 0
        while i < len(msg):
            packet_len = min(len(msg) - i, 19)
            packet = bytearray(packet_len)
            if i == 0:
                packet[0] = 1
            elif packet_len < 19:
                packet[0] = 4
            else:
                packet[0] = 2
            packet[1:] = msg[i:i+packet_len]
            packets.append(packet)
            print(binascii.hexlify(packets[-1]))
            i += 19
        return packets
        
    def send_command(self, command):
        p = Peripheral(self.mac_address, "random")
        status_data = p.readCharacteristic(CHARACTERISTIC_STATUS_HANDLE)
        packets = self.prepare_packets(command, status_data)
        for packet in packets:
            packet_bytes = bytes(packet)
            p.writeCharacteristic(CHARACTERISTIC_COMMAND_HANDLE, packet_bytes, withResponse=True)
        p.disconnect()
        
    def lock(self):
        self.send_command(CODE_LOCK)
    
    def unlock(self):
        self.send_command(CODE_UNLOCK)
