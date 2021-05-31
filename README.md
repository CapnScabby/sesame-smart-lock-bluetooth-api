# Sesame Smart Lock Bluetooth API
The sesame smart lock wifi api is easy to use, but very slow. (In my case, from the time my application posts on the API until the door actually begins to unlock is usually between 10 and 15 seconds).
 
The bluetooth api is desirable for complete local control with low latency.

Two prior works are used to achieve this:
 - https://itsze.ro/blog/2016/12/18/opensesame-reverse-engineering-ble-lock.html
 - https://qiita.com/odetarou/items/9628d66d4d94290b5f2d

The original reverse engineering of the API was done by @itszero. The api is pretty standard for a bluetooth low energy device (using services and characteristics that can be subscribed to), with one complexity: a password is required into order to add a HMAC signature to command messages (messages that lock or unlock the door, messages to request lock status do not require any authentication).

This HMAC password is created when pairing with the Sesame Smart Lock app as (I assume) part of the pairing/registration process. So the most difficult part of using this API is extracting your HMAC password from the Sesame App (see the Frida folder for this). 

Once that is done, all you need to control your lock is the MAC address, your email address associated with you sesame account. 

https://book.hacktricks.xyz/mobile-apps-pentesting/android-app-pentesting/frida-tutorial/objection-tutorial
https://frida.re/docs/android/

https://gist.github.com/d3vilbug/41deacfe52a476d68d6f21587c5f531d

# Frida

adb push frida-server /data/local/tmp/
adb shell "chmod 755 /data/local/tmp/frida-server"
adb shell "/data/local/tmp/frida-server &"



# Objection
objection --gadget co.candyhouse.sesame explore
android hooking watch class co.candyhouse.sesame --dump-args --dump-return

android hooking search methods co.candyhouse.sesame SesameData
android hooking search classes co.candyhouse.sesame

co.candyhouse.sesame.model.SesameData.getDevicePassword


android hooking watch class_method co.candyhouse.sesame.model.SesameData.getDevicePassword --dump-args --dump-backtrace --dump-return

android hooking watch class_method javax.crypto.spec.SecretKeySpec --dump-args --dump-backtrace --dump-return

