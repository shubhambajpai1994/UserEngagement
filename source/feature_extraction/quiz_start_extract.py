import json
import csv
import os
import datetime
import matplotlib.pyplot as plt




def extract_quiz_start():
    print "quiz_start"
    user_wise_quiz_start_data = {}
    global max_week
    max_week = 0.0
    for file in os.listdir("./UserEngagement/dwh/user_file/"):
            quiz_start_data = {}
            for i in range(15, 40):
                quiz_start_data[i]=0.0
            with open("./UserEngagement/dwh/user_file/" + file, 'r') as df:
                for l in df.readlines():
                    d = json.loads(l)
                    if d['user_action'] and "starts quiz" in d['user_action']:

                        #extract week number based on iso gregorian calendar

                        year = d['date'][:4]
                        month = d['date'][5:7]
                        day = d['date'][8:]
                        dt = datetime.date(int(year), int(month), int(day))
                        week_number = dt.isocalendar()[1]
                        if week_number in quiz_start_data:
                            quiz_start_data[week_number] += 1.0
                        else:
                            quiz_start_data[week_number] = 1.0
                user_wise_quiz_start_data[file.split(".json")[0]] = quiz_start_data
                #print user_wise_quiz_start_data[file]
    return user_wise_quiz_start_data

#extract_quiz_start()

def save_quiz_start_data():
    quiz_start_count = extract_quiz_start()

    for user in quiz_start_count:
        #print user.split(".json")[0]
        index = quiz_start_count[user].keys()
        count = quiz_start_count[user].values()
        #print index
        #print count
        with open('./UserEngagement/dwh/csv/quiz_start_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        #plt.show()
        plt.savefig("./UserEngagement/dwh/plots/quiz_start/"+user+".png")
        plt.clf()
    for user in quiz_start_count:
        index = quiz_start_count[user].keys()
        count = quiz_start_count[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/Quiz_start_plot.png");
    plt.show();

save_quiz_start_data()