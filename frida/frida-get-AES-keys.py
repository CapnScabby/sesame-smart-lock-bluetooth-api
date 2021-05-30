#!/usr/bin/env python3

from __future__ import print_function
import frida
import sys
import json
import time

def on_message(message, payload):
	if(message['type'] == 'send'):
		rec_data = json.loads(message['payload'])
		if rec_data['my_type'] == 'IV':
			print("[$] IvParameterSpec :: {}".format(payload.decode))
		elif rec_data['my_type'] == 'KEY':
			string = ""
			for byte in payload:
				string += "%02X" %(byte)
			print("[$] SecretSpecKey :: {}".format(payload))
			print(string)
		else:
			print(message)
	else:
		print(message)

js_code = """
console.log("Script loaded");
Java.perform(function x() {
    //hooking SecretKeySpec's constructor to get the SecretKeySpec
    var secret_key_spec = Java.use("javax.crypto.spec.SecretKeySpec");
    secret_key_spec.$init.overload("[B", "java.lang.String").implementation = function (x, y) {
        send('{"my_type" : "KEY"}', new Uint8Array(x));
        return this.$init(x, y);
    }
    
    //hooking IvParameterSpec's constructor to get the IV 
    var iv_parameter_spec = Java.use("javax.crypto.spec.IvParameterSpec");
    iv_parameter_spec.$init.overload("[B").implementation = function (x) {
        send('{"my_type" : "IV"}', new Uint8Array(x));
        return this.$init(x);
    }
});
"""

# device = frida.get_usb_device()
# pid = device.spawn(["com.example.a11x256.frida_test"])
# device.resume(pid)
# time.sleep(1) 
# session = device.attach(pid)

session = frida.get_usb_device().attach('co.candyhouse.sesame')
script = session.create_script(js_code)
script.on("message", on_message)
script.load()

sys.stdin.read()
