import errno
import os
from datetime import datetime
from datetime import timezone
from subprocess import Popen, TimeoutExpired, PIPE

from flask import Flask, jsonify, abort, Response

import constant

app = Flask(__name__)


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise


def run_command():
    proc = Popen("pg_ctl status", stdout=PIPE, stderr=PIPE, shell=True)
    try:
        outs, errs = proc.communicate(timeout=10)
    except TimeoutExpired:
        proc.kill()
        return False
    if errs:
        return False
    if outs.decode('utf-8').find("(PID:") != -1:
        return True
    else:
        return False


def read_command_result(command):
    proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    try:
        outs, errs = proc.communicate(timeout=60)
    except TimeoutExpired:
        proc.kill()
        abort(500, description="The timeout is expired!")
    if errs:
        abort(500, description=errs.decode('utf-8'))
    return jsonify(success=True, message=outs.decode('utf-8'))


def read_command_result_html(command):
    proc = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    try:
        outs, errs = proc.communicate(timeout=75)
    except TimeoutExpired:
        proc.kill()
        result = "<h1> Error occurred !!! </h1> <br/>" + "The timeout is expired!"
        return Response(result, mimetype='text/html')
    if outs:
        result = "<h1> Success </h1> <br/>"
        result = result + outs.decode('utf-8')
        result = result + "<br/><br/><br/>"
    if errs:
        result = result + "<h1> Error/Warn Found</h1> <br/>"
        result = result + errs.decode('utf-8')
    result = result.replace('\n', '<br/>')
    return Response(result, mimetype='text/html')


@app.errorhandler(400)
def bad_request(error):
    return jsonify(success=False, message=error.description), 400


@app.errorhandler(500)
def server_error(error):
    return jsonify(success=False, message=error.description), 500


@app.route('/pgBackRest/backup/full', methods=['GET'])
def full_backup_job():
    return read_command_result_html(constant.PGBACKREST_FULL_BACKUP)


@app.route('/pgBackRest/backup/diff', methods=['GET'])
def diff_backup_job():
    return read_command_result_html(constant.PGBACKREST_DIFF_BACKUP)


@app.route('/pgBackRest/backup/incr', methods=['GET'])
def incr_backup_job():
    return read_command_result_html(constant.PGBACKREST_INCR_BACKUP)


@app.route('/pgBackRest/info', methods=['GET'])
def info_backup():
    return read_command_result_html(constant.PGBACKREST_INFO_BACKUP)


@app.route('/pgBackRest/create', methods=['GET'])
def create_backup():
    return read_command_result_html(constant.PGBACKREST_CREATE)


@app.route('/pgBackRest/restore/delta', methods=['GET'])
def delta_restore():
    if run_command():
        result = "<h1> Error occurred !!! </h1> <br/>" + "Postgres is still running"
        return Response(result, mimetype='text/html')
    silent_remove("/var/lib/postgresql/data/postmaster.pid")
    return read_command_result_html(constant.PGBACKREST_RESTORE)


@app.route('/pgBackRest/restore/db', methods=['GET'])
def db_restore():
    if run_command():
        result = "<h1> Error occurred !!! </h1> <br/>" + "Postgres is still running"
        return Response(result, mimetype='text/html')
    silent_remove("/var/lib/postgresql/data/postmaster.pid")
    return read_command_result_html(constant.PGBACKREST_RESTORE_DB.format(""))


@app.route('/pgBackRest/restore/time/latest', methods=['GET'])
def time_restore():
    if run_command():
        result = "<h1> Error occurred !!! </h1> <br/>" + "Postgres is still running"
        return Response(result, mimetype='text/html')
    silent_remove("/var/lib/postgresql/data/postmaster.pid")
    return read_command_result_html(constant.PGBACKREST_RESTORE_TIME.format(datetime.now(timezone.utc)))


@app.route('/pgBackRest/db_status', methods=['GET'])
def db_status():
    return Response("Postgres status " + str(run_command()), mimetype='text/html')


app.run(debug=True, host='0.0.0.0')
