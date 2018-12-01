import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import style
import csv

style.use("ggplot")

from sklearn.cluster import KMeans

count = 0

phrase_cloud = []
with open("./UserEngagement/dwh/csv/phrase_cloud_user_data.csv") as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for rowpc in csvReader:
        count += 1
        a = []
        for i in range(0, 85):
            a.append(float(rowpc[i]))
        phrase_cloud.append(a)
        # print phrase_cloud
mmtoc = []
with open("./UserEngagement/dwh/csv/mmtoc_user_data.csv") as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for rowm in csvReader:
        a = []
        for i in range(0, 85):
            a.append(float(rowm[i]))
        mmtoc.append(a)
        # print mmtoc

video_count = []
with open("./UserEngagement/dwh/csv/video_count_user_data.csv") as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for rowqs in csvReader:
        a = []
        for i in range(0, 85):
            a.append(float(rowqs[i]))
            video_count.append(a)
        # print video_count
video_duration = []
with open("./UserEngagement/dwh/csv/video_duration_user_data.csv") as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for rowq in csvReader:
        a = []
        for i in range(0, 85):
            a.append(float(rowq[i]))
            video_duration.append(a)
        # print video_duration

# [[1,2],[5,8],[1.5,1.8],[1,0.6],[9,11],[12,10],[1,15]]
week_data_video = []
week_data_non_video= []
for i in range(0, 85):
    week_data_non_video.append([])
    week_data_video.append([])
for user in range(0, count):
    for i in range(0, 85):
        val1 = float(mmtoc[user][i]) + float(phrase_cloud[user][i])
        val2 = (2 * video_count[user][i]) + video_duration[user][i]
        week_data_video[i].append([val2, 0])
        week_data_non_video[i].append([val1, 0])
# print week_data

user = []
mean_user_engagement_video = []

for file in os.listdir("./UserEngagement/dwh/user_file/"):
    user.append(file.split(".json")[0])
    mean_user_engagement_video.append(0.0)
#print user
#print mean_user_engagement

week_count = 0.0

centroid_set = []
for j in range(0, 85):
    centroid_set.append([])
# #############################################################################
# Compute clustering
for j in range(15, 40):
    X = np.array(week_data_video[j - 15])
    # print X

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(X)

    week_count += 1.0

    centroid = kmeans.cluster_centers_
    labels = kmeans.labels_

    '''
    # print (centroid)
    centroid_set[j - 15] = centroid
    with open('./UserEngagement/dwh/csv/course_based_cluster_data.csv', 'a') as file1:
        csv_writer = csv.writer(file1)
        csv_writer.writerow(centroid_set[j - 15])
    # print labels
    '''
    colors = ["y.", "r.", "g.", "b.", "m.", "k."]
    #colors = ["slategray.", "firebrick", "whitesmoke", "tan", "moccasin", "pink", "brown", "skyblue", "peru", "lavender", "y.", "r.", "g.", "b.", "m.", "k."]
    # #############################################################################
    # Plot result
    for i in range(len(X)):
        # print ("coordinate:" , X[i], "label:", labels[i])
        #plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)
        if centroid[labels[i]][0] > (centroid[0][0] + centroid[1][0]) / 2:
            #print centroid[labels[i]][0], centroid[0][0], centroid[1][0], (centroid[0][0] + centroid[1][0]) / 2
            with open("./UserEngagement/dwh/csv/course_based_result/video/week_" + str(j) + ".csv", 'a') as file1:
                csv_writer = csv.writer(file1)
                if mean_user_engagement_video[i] < X[i][0]:
                    csv_writer.writerow([user[i] + " General Engaged" + " Above User Threshold"])
                    #print user[i] + " General Engaged" + "Below User Threshold"
                else:
                    csv_writer.writerow([user[i] + " General Engaged" + " Below User Threshold"])
                    #print user[i] + " General Engaged" + " Above User Threshold"
            #print user[i], "General Engaged"
        else:
            #print centroid[labels[i]][0], centroid[0][0], centroid[1][0], (centroid[0][0] + centroid[1][0]) / 2
            with open("./UserEngagement/dwh/csv/course_based_result/video/week_" + str(j) + ".csv", 'a') as file1:
                csv_writer = csv.writer(file1)
                if mean_user_engagement_video[i] < X[i][0]:
                    csv_writer.writerow([user[i] + " General Disengaged" + " Above User Threshold"])
                    #print user[i] + " General Engaged" + " Below User Threshold"
                else:
                    csv_writer.writerow([user[i] + " GeneralDisengaged" + " Below User Threshold"])
                    #print user[i] + " General Engaged" + " Above User Threshold"
            #print user[i], "General Disengaged"

        mean_user_engagement_video[i] =float(((mean_user_engagement_video[i] * 0.115) + X[i][0]))




mean_user_engagement_non_video = []

for file in os.listdir("./UserEngagement/dwh/user_file/"):
    mean_user_engagement_non_video.append(0.0)
#print user
#print mean_user_engagement

week_count = 0.0

centroid_set = []
for j in range(0, 25):
    centroid_set.append([])
# #############################################################################
# Compute clustering
for j in range(15, 40):
    Y = np.array(week_data_non_video[j - 15])
    # print X

    kmeans = KMeans(n_clusters=2)
    kmeans.fit(Y)

    week_count += 1.0

    centroid = kmeans.cluster_centers_
    labels = kmeans.labels_
    '''
    # print (centroid)
    centroid_set[j - 15] = centroid
    with open('./UserEngagement/dwh/csv/course_based_cluster_data.csv', 'a') as file1:
        csv_writer = csv.writer(file1)
        csv_writer.writerow(centroid_set[j - 15])
    # print labels
    '''
    colors = ["y.", "r.", "g.", "b.", "m.", "k."]
    #colors = ["slategray", "firebrick", "whitesmoke", "tan", "moccasin", "pink", "brown", "skyblue", "peru", "lavender", "y.", "r.", "g.", "b.", "m.", "k."]
    # #############################################################################
    # Plot result
    for i in range(len(Y)):
        # print ("coordinate:" , X[i], "label:", labels[i])
        #plt.plot(Y[i][0], Y[i][1], colors[labels[i]], markersize=10)
        if centroid[labels[i]][0] > (centroid[0][0] + centroid[1][0]) / 2:
            with open("./UserEngagement/dwh/csv/course_based_result/non_video/week_" + str(j) + ".csv", 'a') as file1:
                csv_writer = csv.writer(file1)
                if mean_user_engagement_non_video[i] < Y[i][0]:
                    csv_writer.writerow([user[i] + " General Engaged" + " Above User Threshold"])
                    #print user[i] + " General Engaged" + "Below User Threshold"
                else:
                    csv_writer.writerow([user[i] + " General Engaged" + " Below User Threshold"])
                    #print user[i] + " General Engaged" + " Above User Threshold"
            #print user[i], "General Engaged"
        else:
            with open("./UserEngagement/dwh/csv/course_based_result/non_video/week_" + str(j) + ".csv", 'a') as file1:
                csv_writer = csv.writer(file1)
                if mean_user_engagement_non_video[i] < Y[i][0]:
                    csv_writer.writerow([user[i] + " General Disengaged" + " Above User Threshold"])
                    #print user[i] + " General Engaged" + " Below User Threshold"
                else:
                    csv_writer.writerow([user[i] + " General Disengaged" + " Below User Threshold"])
                    #print user[i] + " General Engaged" + " Above User Threshold"
            #print user[i], "General Disengaged"

        mean_user_engagement_non_video[i] =float(((mean_user_engagement_non_video[i] * 0.115) + X[i][0]))
