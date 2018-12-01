import json


def extract_videos():
    with open("./UserEngagement/dwh/user_id_daywise_timespent.json") as json_data:
        x = json.load(json_data)
        user_data = {}
        for feature in x:
            video = []
            for days in x[feature].keys():
                for key in x[feature][days].keys():
                    #print key
                    video.append(key)
            print feature, video
            user_data[feature] = video
        Z1 = sorted(user_data.keys())
        sorted_videos = {}
        for index in Z1:
            sorted_videos[index] = user_data[index]
    return sorted_videos

extract_videos()