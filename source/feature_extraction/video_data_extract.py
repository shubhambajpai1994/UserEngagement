import json
import csv
import datetime
import matplotlib.pyplot as plt


def extract_video_count():
    with open("./UserEngagement/dwh/user_id_daywise_timespent.json") as json_data:
        x = json.load(json_data)
        user_data = {}
        for feature in x:
            video = {}
            for i in range(15, 40):
                video[i] = 0.0
            for days in x[feature].keys():
                year = days[:4]
                month = days[5:7]
                day = days[8:]
                # print year
                dt = datetime.date(int(year), int(month), int(day))
                week_number = dt.isocalendar()[1]
                if year == '2017' and week_number < 40:
                    if week_number in video:
                        videos = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            videos += 1.0
                            # print time, videos
                    video[week_number] = videos
            user_data[feature] = video
        Z1 = sorted(user_data.keys())
        sorted_videos = {}
        for index in Z1:
            sorted_videos[index] = user_data[index]
            # print index,sorted_videos[index]
    # print(sorted_videos)
    return sorted_videos


def extract_video_duration():
    with open("./UserEngagement/dwh/user_id_daywise_timespent.json") as json_data:
        x = json.load(json_data)
        user_data = {}
        for feature in x:
            video = {}
            for i in range(15, 40):
                video[i] = 0.0
            for days in x[feature].keys():
                year = days[:4]
                month = days[5:7]
                day = days[8:]
                # print year
                dt = datetime.date(int(year), int(month), int(day))
                week_number = dt.isocalendar()[1]
                if year == '2017' and week_number < 40:
                    if week_number in video:
                        time = 0.0
                        for key in x[feature][days].keys():
                            # print x[feature][key]
                            time += float(x[feature][days][key])
                            # print time, videos
                    video[week_number] = time
            user_data[feature] = video
        Z1 = sorted(user_data.keys())
        sorted_videos = {}
        for index in Z1:
            sorted_videos[index] = user_data[index]
            # print index,sorted_videos[index]
    # print(sorted_videos)
    return sorted_videos


def save_video_count_data():
    print "video count"
    video_data = extract_video_count()
    for user in video_data:
        # print user
        index = video_data[user].keys()
        count = video_data[user].values()
        # print index
        # print count
        with open('./UserEngagement/dwh/csv/video_count_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/video_count_data/" + user + ".png")
        plt.clf()
    for user in video_data:
        index = video_data[user].keys()
        count = video_data[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/Video_count_plot.png");
    plt.show()


def save_video_duration_data():
    print "video duration"
    video_data = extract_video_duration()
    for user in video_data:
        # print user
        index = video_data[user].keys()
        count = video_data[user].values()
        # print index
        # print count
        with open('./UserEngagement/dwh/csv/video_duration_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        # plt.show()
        plt.savefig("./UserEngagement/dwh/plots/video_duration_data/" + user + ".png")
        plt.clf()
    for user in video_data:
        index = video_data[user].keys()
        count = video_data[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/Video_duration_plot.png");
    plt.show()


def save_video_data():
    save_video_count_data()
    save_video_duration_data()


save_video_data()
