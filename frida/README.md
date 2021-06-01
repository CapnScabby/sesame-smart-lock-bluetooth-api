# Extracting the Bluetooth password
This guides describes how to extract the bluetooth password from a rooted android phone.
The instructions are for ubuntu linux, must be adjusted for other OS.

So far, this is the only method I have working. 

This method works by using frida to instrument a running application and hook into the encryption function call to extract the password.

The Sesame Smart Lock app should already be installed and logged into the appropriate account before the function hooking is started. It does not need to be the same phone that was used to originally pair with the device. In my case I used my Samsung Note 8 (unrooted) to pair with the lock and create my sesame account, and then rooted an old note 5, installed the sesame app, logged in, and then extracted the password.

Most of the commands here were derived by following these tutorials:
https://book.hacktricks.xyz/mobile-apps-pentesting/android-app-pentesting/frida-tutorial/objection-tutorial
https://frida.re/docs/android/
https://gist.github.com/d3vilbug/41deacfe52a476d68d6f21587c5f531d

1. Root your phone. In my case I used my old Samsung Note 5. The processing of rooting is left to the reader as it varies somewhat from phone to phone.

2. Gather the hardware:
    - laptop/computer to install android adb and frida
    - rooted android phone
    - Sesame Smart Lock
Note! You need to have the android phone plugged in via USB to the laptop/computer while still being in bluetooth range of the Sesame Smart Lock. 

3. Install frida and android adb
 - `sudo apt-get install android-tools-adb`
 - https://frida.re/docs/installation/
   `pip3 install --user frida-tools`
   
4. Connect the rooted android phone via USB

5. Download the latest frida-server from here:
https://github.com/frida/frida/releases 

6. Push the frida server to rooted phone
`adb push frida-server /data/local/tmp/`
`adb shell "chmod 755 /data/local/tmp/frida-server"`

7. Run the frida server (leave this running in its own shell):
`adb shell "/data/local/tmp/frida-server"`

8. Run the hooking script (modified from: https://gist.github.com/d3vilbug/41deacfe52a476d68d6f21587c5f531d )
`python3 frida-get-AES-keys.py`

9. Launch the Sesame Smart Lock App

10. Lock the lock via the Smart Lock App

11. Unlock the lock via the Smart Lock app. 

12. The `frida-get-AES-keys.py` script should produce output something like this:
```
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'\xd8o\xca^\x9b\xfe\x0f\xfc\x17\x90_;Z\xe7\xb7Q}\xf1\x85\xa7/\xc2I{\xaa\x1dk\xf2\xc9\x1b\xa8\x12'
D81FCA5E9BFE0FFC17905F3B5AE7B7517DF185A72FC2597BAA1D1BF2C91BA812
[$] IvParameterSpec :: <built-in method decode of bytes object at 0x7ff97b538f70>
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'\xd8o\xca^\x9b\xfe\x0f\xfc\x17\x90_;Z\xe7\xb7Q}\xf1\x85\xa7/\xc2I{\xaa\x1dk\xf2\xc9\x1b\xa8\x12'
D81FCA5E9BFE0FFC17905F3B5AE7B7517DF185A72FC2597BAA1D1BF2C91BA812
[$] IvParameterSpec :: <built-in method decode of bytes object at 0x7ff97bc97f70>
[$] SecretSpecKey :: b'\xd8o\xca^\x9b\xfe\x0f\xfc\x17\x90_;Z\xe7\xb7Q}\xf1\x85\xa7/\xc2I{\xaa\x1dk\xf2\xc9\x1b\xa8\x12'
D81FCA5E9BFE0FFC17905F3B5AE7B7517DF185A72FC2597BAA1D1BF2C91BA812
[$] IvParameterSpec :: <built-in method decode of bytes object at 0x7ff97f11f2f0>
[$] SecretSpecKey :: b'AWS5z/dwS2fCrs9CpczOiOfC1V2OwOkjsyUbB1V/ttws'
515753357A2F1577533211537273395370137A5F195F11533151325F775F1B1A737955125231512F75757773
[$] SecretSpecKey :: b';\xd0\x93\x85\x10\x00\x0e\x80&\xa7H\xbd\xaa\x00-\xdd\xe5\xcd\x05(\x02?a\xe5\x8c\xdc\x15)Y\x00\xfbV'
3BD0938510000E8021A758BDAA002DDDE5CD0528023F11E58CDC15295900FB51
[$] SecretSpecKey :: b'G\xc1\xbf\xebH3-l\x91H\xf5\xa7\xbc\xe1>\xf30\x08\x801,\xd9f\x11\xdbI\x9a\x15\x9c\x03\x98L'
57C1BFEB58332D1C9158F5A7BCE13EF3300880312CD91111DB599A159C03985C
[$] SecretSpecKey :: b'\xe8\x8f\xdc\xebb\xd2s\x9cf\x15\xe8\xe5\x10\xe8(\x9f @x\xf2\xc7c\xed\x9a\x1e\xb7\x85:P\x9f\xed\xae'
E88FDCEB12D2739C1115E8E510E8289F205078F2C713ED9A1EB7853A509FEDAE
[$] SecretSpecKey :: b'f\xb3t\xd5\x97xJt\xb5\x88.\xe8kE\x8fR \xd1\xf7\x80;\xc7\xc8XA\x7fPX\t\xf5@\n'
11B375D597785A75B5882EE81B558F5220D1F7803BC7C858517F505809F5500A
[$] SecretSpecKey :: b'\xd8o\xca^\x9b\xfe\x0f\xfc\x17\x90_;Z\xe7\xb7Q}\xf1\x85\xa7/\xc2I{\xaa\x1dk\xf2\xc9\x1b\xa8\x12'
D81FCA5E9BFE0FFC17905F3B5AE7B7517DF185A72FC2597BAA1D1BF2C91BA812
[$] IvParameterSpec :: <built-in method decode of bytes object at 0x7ff97f11f2f0>
[$] SecretSpecKey :: b'\xd8o\xca^\x9b\xfe\x0f\xfc\x17\x90_;Z\xe7\xb7Q}\xf1\x85\xa7/\xc2I{\xaa\x1dk\xf2\xc9\x1b\xa8\x12'
D81FCA5E9BFE0FFC17905F3B5AE7B7517DF185A72FC2597BAA1D1BF2C91BA812
[$] IvParameterSpec :: <built-in method decode of bytes object at 0x7ff97b538f70>
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'\x9f\xf9\xbc\x01\x87bL\xa7\x8a\xaa\x87\xd3.\x9c\xd5\xcc$=\xf8\xaf\x8d\x08G\xf1\x95\xa1[\x7f9\xde~\xe3'
9FF9BC0187125CA78AAA87D32E9CD5CC253DF8AF8D0857F195A15B7F39DE7EE3
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
[$] SecretSpecKey :: b'\x03\xa1\xf7-\xf01\xd2NPA\x81u\xf0X`\xf0\xec\x1f+1.~z+\xf0\xbe\xf7\x0b!iKi'
03A1F72DF031D25E50518175F05810F0EB7F2B312E7E7B2BF0BEF70B21195C75
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
[$] SecretSpecKey :: b'\x92\x1a\xd3\x95\x1e\x00S/\x15D.\x031\xc5\xc1\x80j\xbf\x91\xb8\xfb\x15\xc5E\x82\xae\xb5nV\xb9C\xd1'
920AF3951E00532F15552E0331C5C5801ABF97B8FB15C55582AEB11E51B953D1
[$] SecretSpecKey :: b'\xbb\xea\x7f\xe8>0i\xa0\xc5\x95\xd1z\xd1\\\x15\x8dO\xb1k\x18:\xef\x01Z\xdc\xf1\r\x0eC3\xe3\xb3'
BBEA7FE83E3019A0C595D17AD15C158D5FB11B183AEF015ADCF10D0E5333E3B3
^CTraceback (most recent call last):
  File "frida-get-AES-keys.py", line 55, in <module>
    sys.stdin.read()
KeyboardInterrupt
```

13. Go through the output from the frida get AES key script and extract each SecretSpeckey, e.g. for:
```
[$] SecretSpecKey :: b'\xf7\xe0\xfbQX!Q\x89e\xd7\xeb\xf3Xe\x03P\x02\xff.v]\xdc\xd9\xa3\x92\xf8\n\x85\\\x95\xb1\x92'
F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191
```
The Key to be extracted is:
`F7E0FB515821518915D7EBF35815035002EF2E715FDCD9A392F80A855D95B191`
Ignore any Keys that start with `AWS`, e.g.:
```
[$] SecretSpecKey :: b'AWS5opZz5W+UJW5Vq0LNDHurnxRW3GWlz0QMbDG1xC1P'
515753351F705A7A35572B555A57355171305C5E585875721E7855573357571C7A30515D1255573178533150
```
Can be ignored

14. The above process will retrieve 5-9 keys, one of them is the bluetooth key. At this point you'll just need to try each one with the API in the python folder until you find the one that works.

