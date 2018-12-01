import json
import datetime
from sklearn.cluster import KMeans
import numpy as np
import math
from flask import Flask

app = Flask(__name__)

user_id_email_mapping = {}

user_group = {}
nudges = ["Nudge for General Engaged Above User Threshold", "Nudge for General Engaged Below User Threshold",
          "Nudge for General Moderately Engaged Above User Threshold",
          "Nudge for General Moderately Engaged Below User Threshold",
          "Nudge for General Disengaged Above User Threshold", "Nudge for General Disengaged Below User Threshold",
          "Nudge for Zombie Users"]
# current_week_number = datetime.date.today().isocalendar()[1] + 52
current_week_number = 95


def email_uid():
    print("mapping email to uid")
    with open("./UserEngagement/dwh/userdetails.json") as json_data:
        x = json.load(json_data)
    for feature in x:
        user_id_email_mapping[feature['email']] = feature['id']


def extract_zombie():
    print("Identifying Zombie Users")
    users_last_login = {}

    zombie_user = []

    with open("./UserEngagement/dwh/loggedin.json") as json_data:
        x = json.load(json_data)
        for days in x:
            year = days[:4]
            month = days[5:7]
            day = days[8:]
            dt = datetime.date(int(year), int(month), int(day))
            week_number = dt.isocalendar()[1]
            if year == "2018":
                week_number += 52
            for user in x[days]:

                if user in users_last_login:
                    if week_number < users_last_login[user]:
                        users_last_login[user] = week_number
                else:
                    users_last_login[user] = week_number

    # print(current_week_number)
    for user in users_last_login:
        if users_last_login[user] < current_week_number - 8:
            if user in user_id_email_mapping:
                # print(user_id_email_mapping[user], users_last_login[user])
                zombie_user.append(user_id_email_mapping[user])
    return zombie_user


def extract_video_count():
    print("Extracting video count")
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
    print("Extracting video durations")
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
    print("Extracting mmtoc clicks")
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
    # print user_data


def extract_phrase_clicks():
    print("Extracting phrase cloud clicks")
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
    # print(user_data)


def classification():
    users = []
    mean_user_engagement_video = []

    print("Starting......")

    email_uid()
    video_count = extract_video_count()
    video_duration = extract_video_duration()
    phrase_cloud = extract_phrase_clicks()
    mmtoc = extract_mmtoc_clicks()
    zombie_user = extract_zombie()

    print("Running algorithm")

    week_data_video = []
    week_data_non_video = []
    for i in range(0, 85):
        week_data_non_video.append([])
        week_data_video.append([])
    for user in video_count:
        users.append(user)
        mean_user_engagement_video.append(0.0)
        for i in range(0, 85):
            val1 = 0.0
            if user in mmtoc:
                val1 += float(mmtoc[user][i + 15])
            if user in phrase_cloud:
                val1 += float(phrase_cloud[user][i + 15])

            val2 = 0.0
            if user in video_count:
                val2 += float(5.0 * video_count[user][i + 15])
            if user in video_duration:
                val2 += float(2.0 * video_duration[user][i + 15])

            week_data_video[i].append([val2, val1])
    # print(users)
    week_count = 0.0
    centroid_set = []
    for j in range(0, 85):
        centroid_set.append([])
    # #############################################################################
    # Compute clustering

    # till week 95 i.e. 28th october 2018 date of video data
    for j in range(15, 95):
        X = np.array(week_data_video[j - 15])

        kmeans = KMeans(n_clusters=3)
        kmeans.fit(X)

        week_count += 1.0

        centroid = kmeans.cluster_centers_
        labels = kmeans.labels_

        colors = ["y.", "r.", "g.", "b.", "m.", "k."]

        origin = np.array([0.0, 0.0])
        centroid_of_group_1 = np.linalg.norm(centroid[0] - origin)
        centroid_of_group_2 = np.linalg.norm(centroid[1] - origin)
        centroid_of_group_3 = np.linalg.norm(centroid[2] - origin)

        disengaged_group = min(centroid_of_group_1, centroid_of_group_2, centroid_of_group_3)
        engaged_group = max(centroid_of_group_1, centroid_of_group_2, centroid_of_group_3)
        if j == 92:
            for i in range(len(X)):
                if users[i] not in zombie_user:
                    centroid_of_user_group = np.linalg.norm(centroid[labels[i]] - origin)
                    current_week_user_engagement_value = math.sqrt(math.pow(X[i][0], 2) + math.pow(X[i][1], 2))

                    if centroid_of_user_group == engaged_group:
                        if mean_user_engagement_video[i] < current_week_user_engagement_value:
                            user_group[users[i]] = 0
                            # print([users[i], " General Engaged Above User Threshold"])
                        else:
                            user_group[users[i]] = 1
                            # print([users[i], " General Engaged Below User Threshold"])

                    elif centroid_of_user_group != disengaged_group:
                        if mean_user_engagement_video[i] < current_week_user_engagement_value:
                            user_group[users[i]] = 2
                            # print([users[i], " General Moderately Engaged Above User Threshold"])
                        else:
                            user_group[users[i]] = 3
                            # print([users[i], " General Moderately Engaged Below User Threshold"])

                    else:
                        if mean_user_engagement_video[i] < current_week_user_engagement_value:
                            user_group[users[i]] = 4
                            # print([users[i], " General Disengaged Above User Threshold"])
                        else:
                            user_group[users[i]] = 5
                            # print([users[i], " General Disengaged Below User Threshold"])

                    mean_user_engagement_video[i] = float(
                        (mean_user_engagement_video[i] * 0.115) + current_week_user_engagement_value)
                else:
                    user_group[users[i]] = 6
                    # print([users[i], " Zombie User"])
                print(user_group[users[i]])


@app.route('/')
def index():
    #results =""
    for users in user_group:
        #results += str(users) + "  " + nudges[user_group[users]] + "\n"
        print("Nudge sent to user " + str(users))
    return "Nudge sent to all the users"


@app.route('/<user_id>')
def index1(user_id):
    if int(user_id) in user_group:
        print (user_id, user_group[int(user_id)])
        return nudges[user_group[int(user_id)]]
    return "Not a valid user ID"


classification()

if __name__ == '__main__':
    app.run(debug=True)
