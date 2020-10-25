import speedtest as st
import pandas as pd
import sqlite3

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

print(getSpeed())