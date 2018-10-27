import json
import csv
import os
import datetime
import matplotlib.pyplot as plt


def extract_phrase_cloud():
    print "phrase_cloud"
    user_wise_data = {}
    for file in os.listdir("./UserEngagement/dwh/user_file/"):
        phrase_cloud_clicks = {}
        for i in range(15, 40):
            phrase_cloud_clicks[i] = 0.0
        with open("./UserEngagement/dwh/user_file/" + file, 'r') as df:
            for l in df.readlines():
                d = json.loads(l)
                if d['user_action'] and "phrase cloud" in d['user_action']:

                    # extract week number based on iso gregorian calendar

                    year = d['date'][:4]
                    month = d['date'][5:7]
                    day = d['date'][8:]
                    dt = datetime.date(int(year), int(month), int(day))
                    week_number = dt.isocalendar()[1]
                    if week_number in phrase_cloud_clicks:
                        phrase_cloud_clicks[week_number] += 1.0
                    else:
                        phrase_cloud_clicks[week_number] = 1.0

            user_wise_data[file.split(".json")[0]] = phrase_cloud_clicks
    return user_wise_data


def save_phrase_cloud_data():
    phrase_cloud_clicks = extract_phrase_cloud()
    for users in phrase_cloud_clicks:
        for week in range(15, 40):
            phrase_cloud_clicks[users][week] = phrase_cloud_clicks[users][week]
    for user in phrase_cloud_clicks:
        # print user.split(".json")[0]
        usr = user.split(".json")[0]
        index = phrase_cloud_clicks[user].keys()
        count = phrase_cloud_clicks[user].values()
        # print index
        # print count
        with open('./UserEngagement/dwh/csv/phrase_cloud_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/phrase_cloud/" + usr + ".png")
        plt.clf()
    for user in phrase_cloud_clicks:
        index = phrase_cloud_clicks[user].keys()
        count = phrase_cloud_clicks[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/phrase_cloud_plot.png");
    plt.show()


save_phrase_cloud_data()
