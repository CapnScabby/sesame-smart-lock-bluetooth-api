

CODE_LOCK = 1;
CODE_UNLOCK = 2;
SERVICE_OPERATION_UUID =           '00001523-1212-efde-1523-785feabcd123'
CHARACTERISTIC_COMMAND_UUID =      '00001524-1212-efde-1523-785feabcd123' #where we write the commands
CHARACTERISTIC_COMMAND_HANDLE = 0x0016
CHARACTERISTIC_ANGLE_STATUS_UUID = '00001525-1212-efde-1523-785feabcd123'
CHARACTERISTIC_ANGLE_STATUS_HANDLE = 0x0019
CHARACTERISTIC_STATUS_UUID =       '00001526-1212-efde-1523-785feabcd123' #used as nonce when signing
CHARACTERISTIC_STATUS_HANDLE = 0x001c
"""
pi@raspberrypi:~ $ sudo gatttool --device=df:fb:ce:46:41:53 --characteristics -t random
handle = 0x0002, char properties = 0x02, char value handle = 0x0003, uuid = 00002a00-0000-1000-8000-00805f9b34fb
handle = 0x0004, char properties = 0x02, char value handle = 0x0005, uuid = 00002a01-0000-1000-8000-00805f9b34fb
handle = 0x0006, char properties = 0x02, char value handle = 0x0007, uuid = 00002a04-0000-1000-8000-00805f9b34fb
handle = 0x0009, char properties = 0x20, char value handle = 0x000a, uuid = 00002a05-0000-1000-8000-00805f9b34fb
handle = 0x000d, char properties = 0x04, char value handle = 0x000e, uuid = 00001532-1212-efde-1523-785feabcd123
handle = 0x000f, char properties = 0x18, char value handle = 0x0010, uuid = 00001531-1212-efde-1523-785feabcd123
handle = 0x0012, char properties = 0x02, char value handle = 0x0013, uuid = 00001534-1212-efde-1523-785feabcd123
handle = 0x0015, char properties = 0x0a, char value handle = 0x0016, uuid = 00001524-1212-efde-1523-785feabcd123
handle = 0x0017, char properties = 0x12, char value handle = 0x0018, uuid = 00001525-1212-efde-1523-785feabcd123
handle = 0x001a, char properties = 0x12, char value handle = 0x001b, uuid = 00001526-1212-efde-1523-785feabcd123
handle = 0x001d, char properties = 0x02, char value handle = 0x001e, uuid = 00001527-1212-efde-1523-785feabcd123
handle = 0x001f, char properties = 0x02, char value handle = 0x0020, uuid = 00001528-1212-efde-1523-785feabcd123
pi@raspberrypi:~ $ sudo gatttool --device=df:fb:ce:46:41:53 --char-desc -t random
handle = 0x0001, uuid = 00002800-0000-1000-8000-00805f9b34fb
handle = 0x0002, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0003, uuid = 00002a00-0000-1000-8000-00805f9b34fb
handle = 0x0004, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0005, uuid = 00002a01-0000-1000-8000-00805f9b34fb
handle = 0x0006, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0007, uuid = 00002a04-0000-1000-8000-00805f9b34fb
handle = 0x0008, uuid = 00002800-0000-1000-8000-00805f9b34fb
handle = 0x0009, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x000a, uuid = 00002a05-0000-1000-8000-00805f9b34fb
handle = 0x000b, uuid = 00002902-0000-1000-8000-00805f9b34fb
handle = 0x000c, uuid = 00002800-0000-1000-8000-00805f9b34fb
handle = 0x000d, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x000e, uuid = 00001532-1212-efde-1523-785feabcd123
handle = 0x000f, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0010, uuid = 00001531-1212-efde-1523-785feabcd123
handle = 0x0011, uuid = 00002902-0000-1000-8000-00805f9b34fb
handle = 0x0012, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0013, uuid = 00001534-1212-efde-1523-785feabcd123
handle = 0x0014, uuid = 00002800-0000-1000-8000-00805f9b34fb
handle = 0x0015, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0016, uuid = 00001524-1212-efde-1523-785feabcd123
handle = 0x0017, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0018, uuid = 00001525-1212-efde-1523-785feabcd123
handle = 0x0019, uuid = 00002902-0000-1000-8000-00805f9b34fb
handle = 0x001a, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x001b, uuid = 00001526-1212-efde-1523-785feabcd123
handle = 0x001c, uuid = 00002902-0000-1000-8000-00805f9b34fb
handle = 0x001d, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x001e, uuid = 00001527-1212-efde-1523-785feabcd123
handle = 0x001f, uuid = 00002803-0000-1000-8000-00805f9b34fb
handle = 0x0020, uuid = 00001528-1212-efde-1523-785feabcd123
pi@raspberrypi:~ $ 

"""


import sys
import binascii
import struct
import time
from bluepy.btle import UUID, Peripheral, DefaultDelegate
import hashlib
import hmac
import binascii

class SesameSmartLockBTController:
    def __init__(self, user_name, mac_address, password):
        self.user_name = user_name
        self.user_hash = hashlib.md5(self.user_name.encode()).digest()
        self.mac_address = mac_address
        self.mac_data = bytearray.fromhex(self.mac_address.replace(':',' '))
        self.mac_data.reverse()
        self.password = password
        self.byte_password = bytearray.fromhex(self.password)        
        
    def handle_status_bt_msg(self, handle, value):
        """
        handle -- integer, characteristic read handle the data was received on
        value -- bytearray, the data returned in the notification
        """
        print("Received data: %s" % hexlify(value))
        self.last_status = value
        
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
        #print("status data: {}".format(binascii.hexlify(status_data)))
        #print("status slice: {}".format(binascii.hexlify(status_data[6:10])))
        nonce = int.from_bytes(status_data[6:10], byteorder='little', signed=False) + 1
        #print("nonce:{}".format(nonce))
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
        sesame_service = p.getServiceByUUID(SERVICE_OPERATION_UUID)
        status_characteristic = sesame_service.getCharacteristics(CHARACTERISTIC_STATUS_UUID)[0]
        command_characteristic = sesame_service.getCharacteristics(CHARACTERISTIC_COMMAND_UUID)[0]
        #angle_characteristic = sesame_service.getCharacteristics(CHARACTERISTIC_ANGLE_STATUS_UUID)[0]
        if (status_characteristic.supportsRead()):
            data = status_characteristic.read()
            status_data = status_characteristic.read()
        else:
            raise ValueError("Could not get status")
        packets = self.prepare_packets(command, status_data)
        for packet in packets:
            packet_bytes = bytes(packet)
            #print(binascii.hexlify(packet_bytes))
            command_characteristic.write(packet_bytes, withResponse=True)
        p.disconnect()
        
    def lock(self):
        self.send_command(CODE_LOCK)
    
    def unlock(self):
        self.send_command(CODE_UNLOCK)
        
if __name__ == "__main__":
    import time
    api = SesameSmartLockBTController(user_name, mac_address, password)
    #status_data = bytearray.fromhex("00 00 00 00 00 00 34 30 30 30 1a d3 67 3a 00")
    #api.prepare_packets(CODE_UNLOCK, status_data)
    api.lock()
    time.sleep(3)
    api.unlock()
        
