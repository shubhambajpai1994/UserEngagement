import os
import json

def user_action(client_msg):
    if "content_id :" in client_msg:
        return client_msg.split("msg: '")[1].split(" content_id :")[0]

    else:
        if "curriculum" in client_msg or "leaderboard" in client_msg:
            if "msg:'" not in client_msg and "msg: '" not in client_msg:
                # print client_msg.split("msg: ")[1][:-2]
                return client_msg.split("msg: ")[1][:-2]
            else:
                # print client_msg.split("msg:")[1].split("'")[1].split("'")[0]
                return client_msg.split("msg:")[1].split("'")[1].split("'")[0]
        else:
            if "msg: '" in client_msg:
                return client_msg.split("msg: '")[1].split("'")[0]
            elif "msg:'" in client_msg:
                return client_msg.split("msg:'")[1].split("'")[0]



def user_json():
    userAction = []
    for file in os.listdir("./UserEngagement/logdumps_organisationX/"):
            print file
            with open("./UserEngagement/logdumps_organisationX/" + file) as json_data:
                x = json.load(json_data)
            for feature in x:

                # print feature['client_msg'].encode('utf-8').strip()
                input = user_action(feature['client_msg'].encode('utf-8').strip())
                # print input
                if input not in userAction:
                    print input
                    userAction.append(input)



user_json()