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

def non_course_based_clustering():
    video_duration = extract_video_duration()
    video_count = extract_video_count()
    for user in video_duration:
        # print user
        index = video_duration[user].keys()
        count = video_duration[user].values()


non_course_based_clustering()