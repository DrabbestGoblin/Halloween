import json
import requests
import time
import uuid
import kasaLogin

def main(cycle_time):
    #changes the color of the fron porch light between three halloween colors based on cycles input
    token = login_user()
    deviceID_value = get_deviceID(token)
    y = 0
    for _ in range(cycle_time):
        #orange is 30
        #green is 100
        #purple is 260
        colors = [30,100,260]
        
        for z in range(len(colors)):
            get_hue = get_bulb_command(colors[z])
            get_new_payload = get_payload(deviceID_value, get_hue)
            requests.post("https://wap.tplinkcloud.com?token={0}".format(token), json=get_new_payload)
            y += 1
            print(f'Cycle {y}')
            time.sleep(30)

def login_user():
    #used to login user with creditials and retrieve token. Token does not have to be stored.
    uname = kasaLogin.uname
    pword = kasaLogin.pword

    payload = {
        "method": "login",
        "params": {
            "appType": "Kasa_Android",
            "cloudPassword": pword,
            "cloudUserName": uname,
            "terminalUUID": str(uuid.uuid4())
        }
    }

    response = requests.post("https://wap.tplinkcloud.com", json=payload)
    obj = response.json()
    token = obj["result"]["token"]

    #with open('tokenKasa.txt', 'w') as outfile:
    #    json.dump(obj, outfile)
    
    return token

def get_deviceID(token):
    #used to identify user friendly name to device ID which we then use in json payload
    jsontext = {"method":"getDeviceList"}
    response = requests.post("https://wap.tplinkcloud.com?token={0}".format(token), json=jsontext)
    data = response.json()

    for i in range(len(data["result"]["deviceList"])):
        if (data["result"]["deviceList"][i]["alias"]) == 'Porch Light':
            deviceID_value = data["result"]["deviceList"][i]["deviceId"]
    
    return deviceID_value

def get_bulb_command(variable):
    #sets the bulb command with the color
	bulb_command = {
        "smartlife.iot.smartbulb.lightingservice": {
            "transition_light_state": {
                "on_off": 1,
                "brightness": 40,
                "hue": variable,
                "saturation": 100,
                "transition_period": 5000
            }
        }
    }
	return bulb_command

def get_payload(variable, bulb_command):
    #posts the payload to change bulb color
	payload = {
		"method": "passthrough",
		"params": {
			"deviceId": variable,
			"requestData": json.dumps(bulb_command)  # Request data needs to be escaped, it's a string!
		}
	}
	return payload

if __name__ == '__main__':
    main(cycle_time=10)