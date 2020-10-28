import speedtest as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
import sqlite3
import multiprocessing
import time
import numpy as np

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

# Label each bar in graph
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

# Get internet speed
def getSpeed():
    speed_test = st.Speedtest()
    speed_test.get_best_server()

    # Get ping
    ping = speed_test.results.ping
    # Get Download and Upload Speeds
    download = speed_test.download()
    upload = speed_test.upload()

    # Convert to mbs
    download_mbs = round(download / (10**6), 2)
    upload_mbs = round(upload / (10**6), 2)

    return (ping, download_mbs, upload_mbs)

# Create and connect to db file
class DataBase():
    def __init__(self):
        self.con = sqlite3.connect('./results.db')
        self.c = self.con.cursor()

    def createDataBase(self):
        # Create table in db if it doesn't already exist
        self.c.execute("""CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY,
            ping INTEGER,
            download_mbs INTEGER,
            upload_mbs INTEGER,
            time TEXT
            ) """)
        self.con.commit()
    
    # Add row to db
    def addToDB(self, ping, download_mbs, upload_mbs):
        self.con.execute(f"INSERT INTO results VALUES (null,{ping},{download_mbs},{upload_mbs},datetime('now','localtime'))")
        self.con.commit()

def getNewData():
    while True:
        # Run speed test
        stats = getSpeed()

        # Assign data to variables
        ping = stats[0]
        download_mbs = stats[1]
        upload_mbs = stats[2]

        # Add stats to Database
        DataBase().addToDB(ping, download_mbs, upload_mbs)
        time.sleep(60)

def updateBarGraph(i):
    # Read db into pandas
    og_df = pd.read_sql_query('SELECT * FROM results', DataBase().con)
    df = og_df.tail(5)

    # Plot onto graph
    ax1.cla()
    download_bar = ax1.bar(df.time, df.download_mbs, width=0.8, label='Download')
    upload_bar = ax1.bar(df.time, df.upload_mbs, width=0.8, label='Upload')

    autolabel(download_bar)
    autolabel(upload_bar)
    # plt.subplots_adjust(bottom=0.25)
    ax1.legend(loc='upper center', fancybox=True, shadow=True, ncol=5)
    # plt.gcf().autofmt_xdate()
    ax1.set_ylabel('Speed')
    ax1.set_xlabel('Date')
    ax1.set_title('Last Five Results')
    

    ax2.cla()
    ax2.plot(og_df.time, og_df.download_mbs, linewidth=1, label='Download')
    ax2.plot(og_df.time, og_df.upload_mbs, linewidth=1, label='Download')
    ax2.legend(loc='upper center', fancybox=True, shadow=True, ncol=5)
    ax2.set_ylabel('Speed')
    ax2.set_xlabel('Date')
    ax2.set_title('Last Five Results')
    plt.xticks(og_df.time[::10], og_df.time[::10])

    plt.title('Internet Speed Over Time')
    # plt.setp(ax1.get_xticklabels(), fontsize=10, rotation=30, ha='right')
    plt.setp(ax2.get_xticklabels(), fontsize=10, rotation=30, ha='right')

def main():
    # Graph styles
    plt.style.use('fivethirtyeight')

    # Open Database
    DataBase().createDataBase()

    # Run speed test on new thread
    p1 = multiprocessing.Process(target=getNewData)
    p1.start()
    # p1.join()

    # Update the graph every minute
    ani = FuncAnimation(plt.gcf(), updateBarGraph, interval=1000)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()