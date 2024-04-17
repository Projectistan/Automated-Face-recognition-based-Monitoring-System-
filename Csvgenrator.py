import json
from datetime import datetime
import time
import csv
import time
import os
import tkinter as tk
from subprocess import Popen


#parse the details and generate csv file

def parser_pr(UID, Date_user):
    
    temp = []
    broken_time = []
    total_t = 0
    p='logJson/'+Date_user + ".json"

    if os.path.exists(p):
        with open(p, "r", encoding='utf-8') as f:
            c = json.load(f, encoding='utf-8')
            for key in c:
                if key['name'] == UID:
                    temp.append(float(key['datetime']))

            if len(temp) > 1:
                print('...................')
                OUTPUT_FILE = "raiuniverity-" + UID + '-' + Date_user + ".csv"

                with open(OUTPUT_FILE, "w+", newline="") as cv:
                    details_writer = csv.writer(cv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    details_writer.writerow(["Camera_id", "ID", "Start_time", "End_time", "Total_time"])

                    s_time = temp[0]
                    all_time=0
                    total_t = 0
                    for i in range(0, len(temp) - 1):
                        e_time = temp[i]
                        e1_time = temp[i + 1]
                        second = time_calulator(e_time, e1_time)
                        # print(second)
                        if time_partition(second):
                            #total_t
                            broken_time.append(s_time)
                            broken_time.append(e_time)

                            if(total_t>5):
                                details_writer.writerow(['1001', UID, datetime.fromtimestamp(s_time).strftime('%H:%M:%S'),
                                                        datetime.fromtimestamp(e_time).strftime('%H:%M:%S'), total_t])

                            s_time = e1_time
                            total_t = 0
                        else:
                            total_t = second + total_t
                            all_time = second + all_time
                    if(all_time>10):
                        details_writer.writerow(['1001', UID, datetime.fromtimestamp(s_time).strftime('%H:%M:%S'),datetime.fromtimestamp(e_time).strftime('%H:%M:%S'), total_t])

                cv.close()
                f.close()
                if (all_time < 7):
                    os.remove("raiuniverity-" + UID + '-' + Date_user + ".csv")
                    alert()
                    return False
                csv_open("raiuniverity-" + UID + '-' + Date_user + ".csv")
                return True
            else:
                f.close()
                alert()
                return False
    else:
        alert()
        return False


#check time dilation between each user
def time_calulator(t1, t2):
    elip = datetime.fromtimestamp(t2) - datetime.fromtimestamp(t1)
    return elip.seconds + (elip.microseconds / 1000000)

#divide time on basis ka time
def time_partition(second):
    if second > 15:
        return True
    else:
        return False

#open csv in excel
def csv_open(rasta):
    Popen(rasta, shell=True)

#alert if user not  found
def alert():
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text="User not Found")
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


#parser_pr('sumit', '20-05-20')

# parser will return false if name not found
# if name found it will generate a csv
