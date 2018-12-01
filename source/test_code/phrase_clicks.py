import json
import datetime
import csv
import matplotlib.pyplot as plt

user_id_email_mapping = {}


def email_uid():
    print ("email to uid mappings")
    with open("./UserEngagement/dwh/userdetails.json") as json_data:
        x = json.load(json_data)
    for feature in x:
        user_id_email_mapping[feature['email']] = feature['id']


def extract_phrase_clicks():
    with open("./UserEngagement/dwh/phraseclicks_28Oct.json") as json_data:
        x = json.load(json_data)
        user_data = {}
        for feature in x:
            phrase_clicks = {}
            for i in range(15, 100):
                phrase_clicks[i] = 0.0
            for days in x[feature].keys():
                year = days[:4]
                month = days[5:7]
                day = days[8:]
                dt = datetime.date(int(year), int(month), int(day))
                week_number = dt.isocalendar()[1]
                if year == '2017':
                    if week_number in phrase_clicks:
                        count = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            count += float(len(x[feature][days][key]))
                            # print time, phrase_clickss
                        phrase_clicks[week_number] += count
                else:
                    week_number += 52
                    if week_number in phrase_clicks:
                        count = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            count += float(len(x[feature][days][key]))
                            # print time, phrase_clickss
                        phrase_clicks[week_number] += count
                if feature in user_id_email_mapping:
                    user_data[user_id_email_mapping[feature]] = phrase_clicks
        Z1 = sorted(user_data.keys())
        sorted_phrase_clicks = {}
        for index in Z1:
            sorted_phrase_clicks[index] = user_data[index]
    return sorted_phrase_clicks
    print(user_data)


def save_phrase_clicks_data():
    email_uid()
    print("phrase_clicks")
    phrase_clicks_data = extract_phrase_clicks()
    for user in phrase_clicks_data:
        # print user
        index = phrase_clicks_data[user].keys()
        count = phrase_clicks_data[user].values()
        with open('./UserEngagement/dwh/csv/non_course_phrase_clicks_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/non_course_phrase_clicks_data/" + str(user) + ".png")
        plt.clf()
    for user in phrase_clicks_data:
        index = phrase_clicks_data[user].keys()
        count = phrase_clicks_data[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/non_course_phrase_clicks_plot.png");
    plt.show()



save_phrase_clicks_data()