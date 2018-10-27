import json
import csv
import os
import datetime
import matplotlib.pyplot as plt




def extract_quiz_submit():
    print "quiz_submit"
    user_wise_quiz_submit_data = {}
    global max_week
    max_week = 0.0
    for file in os.listdir("./UserEngagement/dwh/user_file/"):
            quiz_submit_data = {}
            for i in range(15, 40):
                quiz_submit_data[i]=0.0
            with open("./UserEngagement/dwh/user_file/" + file, 'r') as df:
                for l in df.readlines():
                    d = json.loads(l)
                    if d['user_action'] and "quiz is submitted" in d['user_action']:

                        #extract week number based on iso gregorian calendar

                        year = d['date'][:4]
                        month = d['date'][5:7]
                        day = d['date'][8:]
                        dt = datetime.date(int(year), int(month), int(day))
                        week_number = dt.isocalendar()[1]
                        if week_number in quiz_submit_data:
                            quiz_submit_data[week_number] += 1.0
                        else:
                            quiz_submit_data[week_number] = 1.0
                user_wise_quiz_submit_data[file.split(".json")[0]] = quiz_submit_data
                #print user_wise_quiz_submit_data[file]
    return user_wise_quiz_submit_data

#extract_quiz_submit()

def save_quiz_submit_data():
    quiz_submit_count = extract_quiz_submit()

    for user in quiz_submit_count:
        #print user.split(".json")[0]
        usr = user.split(".json")[0]
        index = quiz_submit_count[user].keys()
        count = quiz_submit_count[user].values()
        #print index
        #print count
        with open('./UserEngagement/dwh/csv/quiz_submit_user_data.csv', 'a') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(count)
        plt.plot(index, count)
        #plt.show()
        plt.savefig("./UserEngagement/dwh/plots/quiz_submit/"+user+".png")
        plt.clf()
    for user in quiz_submit_count:
        index = quiz_submit_count[user].keys()
        count = quiz_submit_count[user].values()
        plt.plot(index, count)
    plt.savefig("./UserEngagement/dwh/plots/overall/Quiz_submit_plot.png");
    plt.show();

save_quiz_submit_data()