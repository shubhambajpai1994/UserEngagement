import json
import re
import os

#                                           EXTRACT COURSE ID FOR WHICH CONTENT IS ACCESSED
def course_id(client_msg):
    # print client_msg
    if "Course : " in client_msg:
        return client_msg.split("Course : ")[1].split(" ")[0]
    elif "course_id: " in client_msg:
        return client_msg.split("course_id: '")[1].split("'")[0]

    return "null"


#                                           EXTRACT VIDEO ID BEING PLAYED/BUFFERING/PAUSED
def video_id(client_msg):
    # print client_msg
    if ": video" in client_msg:
        if ": video id" in client_msg:
            return client_msg.split("video id  : ")[1].split(" :")[0]
        elif ": video" in client_msg:
            return client_msg.split("video : ")[1].split(" :")[0]

    if "youtube_id: " in client_msg:
        return client_msg.split("youtube_id: '")[1].split("'")[0]

    return "null"


#                                           EXTRACT KENLIST ID ACCESSED BY USER
def kenlist_id(client_msg):

    #print client_msg
    if "kenlistID :" in client_msg:
        if "at : " in client_msg.split("kenlistID : ")[1]:
            return re.sub("[^0-9]", "", client_msg.split("kenlistID : ")[1].split(" :")[0])
        else:
            return client_msg.split("kenlistID : ")[1].split("'")[0]
    if "playlist_id: '" in client_msg:
        return client_msg.split("playlist_id: '")[1].split("'")[0]

    return "null"


#                                 IF LOG IS FOR VIDEO GIVES DURATION OF OPERATION ELSE RETURN NULL
def get_duration(client_msg):
    if "kenlistID :" in client_msg:
        if "at : " in client_msg.split("kenlistID : ")[1]:
            time = re.sub("[^0-9.]", "", client_msg.split("kenlistID : ")[1].split(" : ")[1])
            if time[-1] == '.':
                time = time[:-1]

            return time

    if "User playing time" in client_msg:
        # print re.sub("[^0-9.]", "", client_msg.split("User playing time")[1].split(":")[1])
        return re.sub("[^0-9.]", "", client_msg.split("User playing time")[1].split(":")[1])

    return "null"


#                   EXTRACT USER ACTION FROM CLIENT MESSAGE
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


#                       CREATE JSON FOR EVERY INDIVIDUAL USER AND STORE INDIVIDUAL ACTION AS AN OBJECT

def user_json():
    for file in os.listdir("./UserEngagement/logdumps_organisationX/"):
        fobj = open("./UserEngagement/dwh/extracted_files.txt", 'r')
        extracted_files = fobj.read().strip().split()
        if file not in extracted_files:
            print file
            fobj.close()
            fobj = open("./UserEngagement/dwh/extracted_files.txt", 'a+')
            fobj.write(file + "\n")
            fobj.close()
            with open("./UserEngagement/logdumps_organisationX/" + file) as json_data:
                x = json.load(json_data)
            for feature in x:
                try:
                    fo = open("./UserEngagement/dwh/user_file/" + feature['uid'] + ".json", 'a')
                    input = {}
                    # print feature['client_msg'].encode('utf-8').strip()
                    input['uid'] = feature['uid']
                    input['email_id'] = feature['email_id']
                    input['timestamp'] = feature['timestamp']
                    input['@timestamp'] = feature['@timestamp']
                    input['date'] = feature['@timestamp'].split("T")[0]
                    input['time'] = feature['@timestamp'].split("T")[1][:-2]
                    input['offset'] = feature['offset']
                    input['Course_Id'] = course_id(feature['client_msg'].encode('utf-8').strip())
                    input['Video_Id'] = video_id(feature['client_msg'].encode('utf-8').strip())
                    input['Kenlist_Id'] = kenlist_id(feature['client_msg'].encode('utf-8').strip())
                    input['duration'] = get_duration(feature['client_msg'].encode('utf-8').strip())
                    input['user_action'] = user_action(feature['client_msg'].encode('utf-8').strip())
                    # print input
                    json.dump(input, fo)
                    fo.write('\n')
                except:
                    print "Error log for :", feature['uid']
                    fo = open("./UserEngagement/dwh/error_file.json", 'a')
                    json.dump(feature, fo)
                    fo.write('\n')
                    pass
        else:
            print "File "+ file + " already processed"


user_json()