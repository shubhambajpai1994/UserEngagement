import json
import datetime

def extract_zombie():
    # login_data_extract
    print "Zombie Users"
    users_last_login = {}
    with open("./UserEngagement/dwh/loggedin.json") as json_data:
        x = json.load(json_data)
        for days in x:
            #print days
            year = days[:4]
            month = days[5:7]
            day = days[8:]
            dt = datetime.date(int(year), int(month), int(day))
            week_number = dt.isocalendar()[1]
            if year == "2018":
                week_number += 52
            for users in x[days]:
                #print users
                if users in users_last_login:
                    if week_number < users_last_login[users]:
                        users_last_login[users] = week_number
                else:
                    users_last_login[users] = week_number
    current_week_number =  datetime.date.today().isocalendar()[1] + 52

    print current_week_number
    for users in users_last_login:
        #print users,users_last_login[users]
        if users_last_login[users] < current_week_number - 8:
            print users, users_last_login[users]

extract_zombie()
