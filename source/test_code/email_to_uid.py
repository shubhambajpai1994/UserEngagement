import json

def email_uid():
    print "email to uid mappings"
    with open("./UserEngagement/dwh/userdetails.json") as json_data:
        x = json.load(json_data)
    count=0
    for feature in x:
        print feature['id'],feature['email']
        count+=1
    print count




email_uid()