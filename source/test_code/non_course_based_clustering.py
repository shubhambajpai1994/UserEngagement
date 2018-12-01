import json
import csv
import datetime
import matplotlib.pyplot as plt

user_id_email_mapping = {}


def email_uid():
    #print "email to uid mappings"
    with open("./UserEngagement/dwh/userdetails.json") as json_data:
        x = json.load(json_data)
    for feature in x:
        user_id_email_mapping[feature['email']] = feature['id']
        # print user_id_email_mapping[feature['email']]


def extract_video_count():
    with open("./UserEngagement/dwh/timespent_28Oct.json") as json_data:
        x = json.load(json_data)
        user_data = {}
        for feature in x:
            video = {}
            for i in range(15, 100):
                video[i] = 0.0
            for days in x[feature].keys():
                year = days[:4]
                month = days[5:7]
                day = days[8:]
                # print year
                dt = datetime.date(int(year), int(month), int(day))
                week_number = dt.isocalendar()[1]
                if year == '2017':
                    if week_number in video:
                        videos = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            videos += 1.0
                            # print time, videos
                        video[week_number] += videos
                else:
                    week_number += 52
                    if week_number in video:
                        videos = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][days][key]
                            videos += 1.0
                            # print time, videos
                        video[week_number] += videos
                        # print user_id_email_mapping[feature]
            if feature in user_id_email_mapping:
                user_data[user_id_email_mapping[feature]] = video
        Z1 = sorted(user_data.keys())
        sorted_videos = {}
        for index in Z1:
            sorted_videos[index] = user_data[index]
            # print index,sorted_videos[index]
    # print(sorted_videos)
    return sorted_videos


def extract_video_duration():
    with open("./UserEngagement/dwh/timespent_28Oct.json") as json_data:
        x = json.load(json_data)
        user_data = {}
        for feature in x:
            video = {}
            for i in range(15, 100):
                video[i] = 0.0
            for days in x[feature].keys():
                year = days[:4]
                month = days[5:7]
                day = days[8:]
                # print year
                dt = datetime.date(int(year), int(month), int(day))
                week_number = dt.isocalendar()[1]
                if year == '2017':
                    if week_number in video:
                        time = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            time += float(x[feature][days][key]['timespent'])
                            # print time, videos
                        video[week_number] += time
                else:
                    week_number += 52
                    if week_number in video:
                        time = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            time += float(x[feature][days][key]['timespent'])
                            # print time, videos
                        video[week_number] += time
            if feature in user_id_email_mapping:
                user_data[user_id_email_mapping[feature]] = video
            else:
                fobj = open("./UserEngagement/dwh/unmapped_emails.txt", 'a+')
                fobj.write(feature + "\n")
                fobj.close()

        Z1 = sorted(user_data.keys())
        sorted_videos = {}
        for index in Z1:
            sorted_videos[index] = user_data[index]
            # print index,sorted_videos[index]
    # print(sorted_videos)
    return sorted_videos


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
        Z1 = sorted(user_data.keys())
        sorted_mmtoc_clicks = {}
        for index in Z1:
            sorted_mmtoc_clicks[index] = user_data[index]
    return sorted_mmtoc_clicks
    #print user_data


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


def save_video_count_data():
    # email_uid()
    print("video count")
    video_data = extract_video_count()
    for user in video_data:
        # print user
        index = video_data[user].keys()
        count = video_data[user].values()
        # print index
        # print count
        with open('./UserEngagement/dwh/csv/non_course_video_count_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/non_course_video_count_data/" + str(user) + ".png")
        plt.clf()
    for user in video_data:
        index = video_data[user].keys()
        count = video_data[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/non_course_video_count_plot.png");
    plt.show()


def save_video_duration_data():
    # email_uid()
    print("video duration")
    video_data = extract_video_duration()
    for user in video_data:
        # print user
        index = video_data[user].keys()
        count = video_data[user].values()
        # print index
        # print count
        with open('./UserEngagement/dwh/csv/non_course_video_duration_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/non_course_video_duration_data/" + str(user) + ".png")
        plt.clf()
    for user in video_data:
        index = video_data[user].keys()
        count = video_data[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/non_course_video_duration_plot.png");
    plt.show()


def save_mmtoc_clicks_data():
    # email_uid()
    print("mmtoc_clicks")
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


def save_video_data():
    save_video_count_data()
    save_video_duration_data()
    save_mmtoc_clicks_data()
    save_phrase_clicks_data()


save_video_data()
