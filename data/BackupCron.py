import os
import time

import schedule

import constant


def full_backup_job():
    bat = constant.PGBACKREST_FULL_BACKUP
    os.system(bat)


def diff_backup_job():
    bat = constant.PGBACKREST_DIFF_BACKUP
    os.system(bat)


# separate schedule for each day of the week can be configured
schedule.every().monday.at(constant.BACKUP_TIME_MON).do(diff_backup_job)
schedule.every().tuesday.at(constant.BACKUP_TIME_TUE).do(diff_backup_job)
schedule.every().wednesday.at(constant.BACKUP_TIME_WED).do(diff_backup_job)
schedule.every().thursday.at(constant.BACKUP_TIME_THUR).do(diff_backup_job)
schedule.every().friday.at(constant.BACKUP_TIME_FRI).do(diff_backup_job)
schedule.every().saturday.at(constant.BACKUP_TIME_SAT).do(diff_backup_job)
schedule.every().sunday.at(constant.BACKUP_TIME_SUN).do(full_backup_job)

time.sleep(10)  # wait for the db to start
os.system(constant.PGBACKREST_CREATE)
os.system(constant.PGBACKREST_CHECK_BACKUP)
while True:
    schedule.run_pending()
    time.sleep(10)
