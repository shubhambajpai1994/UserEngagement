import json
import datetime
import csv
import matplotlib.pyplot as plt

user_id_email_mapping = {}


def email_uid():
    print "email to uid mappings"
    with open("./UserEngagement/dwh/userdetails.json") as json_data:
        x = json.load(json_data)
    for feature in x:
        user_id_email_mapping[feature['email']] = feature['id']


def extract_mmtoc_clicks():
    with open("./UserEngagement/dwh/mmtocclicks_28Oct.json") as json_data:
        x = json.load(json_data)
        user_data = {}
        for feature in x:
            mmtoc_clicks = {}
            for i in range(15, 100):
                mmtoc_clicks[i] = 0.0
            for days in x[feature].keys():
                year = days[:4]
                month = days[5:7]
                day = days[8:]
                dt = datetime.date(int(year), int(month), int(day))
                week_number = dt.isocalendar()[1]
                if year == '2017':
                    if week_number in mmtoc_clicks:
                        count = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            count += float(len(x[feature][days][key]))
                            # print time, mmtoc_clickss
                        mmtoc_clicks[week_number] += count
                else:
                    week_number += 52
                    if week_number in mmtoc_clicks:
                        count = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            count += float(len(x[feature][days][key]))
                            # print time, mmtoc_clickss
                        mmtoc_clicks[week_number] += count
                if feature in user_id_email_mapping:
                    user_data[user_id_email_mapping[feature]] = mmtoc_clicks
                else:
                    fobj = open("./UserEngagement/dwh/unmapped_emails.txt", 'a+')
                    fobj.write(feature + "\n")
                    fobj.close()
        Z1 = sorted(user_data.keys())
        sorted_mmtoc_clicks = {}
        for index in Z1:
            sorted_mmtoc_clicks[index] = user_data[index]
    return sorted_mmtoc_clicks
    print user_data


def save_mmtoc_clicks_data():
    email_uid()
    print "mmtoc_clicks"
    mmtoc_clicks_data = extract_mmtoc_clicks()
    for user in mmtoc_clicks_data:
        # print user
        index = mmtoc_clicks_data[user].keys()
        count = mmtoc_clicks_data[user].values()
        with open('./UserEngagement/dwh/csv/non_course_mmtoc_clicks_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/non_course_mmtoc_clicks_data/" + str(user) + ".png")
        plt.clf()
    for user in mmtoc_clicks_data:
        index = mmtoc_clicks_data[user].keys()
        count = mmtoc_clicks_data[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/non_course_mmtoc_clicks_plot.png");
    plt.show()



save_mmtoc_clicks_data()