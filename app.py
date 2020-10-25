import speedtest as st
import pandas as pd
import sqlite3

# Create and connect to db file
con = sqlite3.connect('./results.db')
c = con.cursor()

# Create table in db if it doesn't already exist
c.execute("""CREATE TABLE IF NOT EXISTS results (
    ping INTEGER,
    download_mbs INTEGER,
    upload_mbs INTEGER 
    ) """)

# Commit changes to db
con.commit()

# Read db into pandas
df = pd.read_sql_query('SELECT * FROM results', con)

print(df)

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

# print(getSpeed())