import os
import shutil
from datetime import datetime, timedelta

# Path to the log files

log_files = {
    "crontab_logs_lin_hst": "/root/logs/crontab_logs_lin_hst.log",
    "crontab_logs_win_hst": "/root/logs/crontab_logs_win_hst.log",
    "crontab_logs_lin_hsc": "/root/logs/crontab_logs_lin_hsc.log",
    "crontab_logs_win_hsc": "/root/logs/crontab_logs_win_hsc.log"
}

#Path where the logs would be archived

archive_dir = "/root/logs/"

#Ensure the archive_dir exists
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)


#Get the current date in format MM DD YYYY
current_date = datetime.now().strftime("%m%d%Y-")

now =datetime.now()
days_ago_7 = now - timedelta(days=2)
for log_name, log_path in log_files.items():
    #check if file exists
    if os.path.exists(log_path):
        # Create new name for rotated log
        archived_log = os.path.join(archive_dir,f"{current_date}{log_name}.log")
        # Move the log file to the archive
        shutil.move(log_path,archived_log)

        print(f"Rotated log file: {log_path} -> {archived_log}")
    else: 
        print(f"Log file doesn't exist: {log_path}")    
    
for log_file in os.listdir(archive_dir):
    log_file_path = os.path.join(archive_dir,log_file)
    if os.path.isfile(log_file_path):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(log_file_path))

        if file_mod_time < days_ago_7:
            os.remove(log_file_path)
            print(f"Deleted old log file: {log_file_path}")
        else:
            print("No old logfile found")    
