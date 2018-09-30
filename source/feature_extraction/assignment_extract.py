import json
import csv
import os
import datetime
import matplotlib.pyplot as plt

def extract_Assignment():
    print "Assignments"
    user_wise_data = {}
    for file in os.listdir("./UserEngagement/dwh/user_file/"):
            Assignment_clicks = {}
            for i in range(15, 40):
                Assignment_clicks[i]=0.0
            with open("./UserEngagement/dwh/user_file/" + file, 'r') as df:
                for l in df.readlines():
                    d = json.loads(l)
                    if d['user_action'] and "Assignments" in d['user_action']:

                        #extract week number based on iso gregorian calendar

                        year = d['date'][:4]
                        month = d['date'][5:7]
                        day = d['date'][8:]
                        dt = datetime.date(int(year), int(month), int(day))
                        week_number = dt.isocalendar()[1]
                        if week_number in Assignment_clicks:
                            Assignment_clicks[week_number] += 1.0
                        else:
                            Assignment_clicks[week_number] = 1.0

                user_wise_data[file] = Assignment_clicks
    return user_wise_data


def save_Assignment_data():
    Assignment_clicks = extract_Assignment()
    for users in Assignment_clicks:
        for week in range(15,40):
            Assignment_clicks[users][week]=Assignment_clicks[users][week]
    for user in Assignment_clicks:
        #print user.split(".json")[0]
        usr = user.split(".json")[0]
        index = Assignment_clicks[user].keys()
        count = Assignment_clicks[user].values()
        #print index
        #print count
        with open('./UserEngagement/dwh/csv/assignment_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        #plt.show()
        plt.savefig("./UserEngagement/dwh/plots/assignments/"+usr+".png")
        plt.clf()
    for user in Assignment_clicks:
        index = Assignment_clicks[user].keys()
        count = Assignment_clicks[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/assignment_plot.png");
    plt.show();

save_Assignment_data()
