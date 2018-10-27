import json
import csv
import os
import datetime
import matplotlib.pyplot as plt


def extract_discussion():
    print "Discussions"
    user_wise_data = {}
    for file in os.listdir("./UserEngagement/dwh/user_file/"):
        Discussion_clicks = {}
        for i in range(15, 40):
            Discussion_clicks[i] = 0.0
        with open("./UserEngagement/dwh/user_file/" + file, 'r') as df:
            for l in df.readlines():
                d = json.loads(l)
                if d['user_action'] and "Discussions" in d['user_action']:

                    # extract week number based on iso gregorian calendar

                    year = d['date'][:4]
                    month = d['date'][5:7]
                    day = d['date'][8:]
                    dt = datetime.date(int(year), int(month), int(day))
                    week_number = dt.isocalendar()[1]
                    if week_number in Discussion_clicks:
                        Discussion_clicks[week_number] += 1.0
                    else:
                        Discussion_clicks[week_number] = 1.0
            #print file.split(".json")[0]
            user_wise_data[file.split(".json")[0]] = Discussion_clicks
    return user_wise_data


def save_discussion_data():
    Discussion_clicks = extract_discussion()
    for user in Discussion_clicks:
        # print user.split(".json")[0]
        usr = user.split(".json")[0]
        index = Discussion_clicks[user].keys()
        count = Discussion_clicks[user].values()
        # print index
        # print count
        with open('./UserEngagement/dwh/csv/discussion_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/discussions/" + usr + ".png")
        plt.clf()
    for user in Discussion_clicks:
        index = Discussion_clicks[user].keys()
        count = Discussion_clicks[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/Discussion_plot.png");
    plt.show()


save_discussion_data()
