"""This script aims at creating log file and sending it on email"""
import os
import sys
import glob
import logging
import datetime
from shutil import move
import subprocess


"""Generic error handling module"""
def error(status, error_msg, module_name, return_code):

    if status.lower() == 'error':
        logging.error('!!! Error !!!')
        logging.error('Error executing module : %s', module_name)
        logging.error(error_msg)
        logging.error('Module return code : %s', return_code)
        logging.error('Exiting script with exit(1) !!!')
        email_log_file(log_file, status='failure')
        sys.exit(1)

    if status.lower() == 'warning':
        logging.warning('!!! Warning !!!')
        logging.warning('Error executing module : %s', module_name)
        logging.warning(error_msg)
        logging.warning('Module return code : %s', return_code)
        logging.warning('Script execution will continue !!!')


"""Generic Logging function """
def initiate_logging():

    dt_now = datetime.datetime.today()
    log_file = '<file_path>' + 'testing' + dt_now.strftime('_%Y%m%d_%H%M%S') + '.log'
    log_file_pattern = '<file_path>' + 'testing' + '*' + '.log'
    log_file_list = glob.glob(log_file_pattern)

    for file in log_file_list:
        if os.path.exists(file):
            dest_file = '<archive_log_path>' + file.split('/')[-1]
            if os.path.exists(dest_file):
                os.remove(dest_file)
            move(file, '<archive_log_path>')

    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    return log_file


"""Executes the provided unix shell command """
def execute_shell_command(command):

    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        return_code = proc.returncode
        if err:
            print(str(err))
        return out, return_code
    except Exception as err:
        print("Exception Occurred while executing module : %s", str(err))
        return 105


"""Emails the status of job execution along with log file as attachment"""
def email_log_file(log_file, status):

    if status == 'success':
        body = 'Execution successful...PFA log file' 
        subject = 'Execution successful - testing'

        email_cmd = """echo "{b}" | mailx -s "{s}" -a "{l}" "{to}" """.format(b=body, s=subject, l=log_file, to='<email_id>')
        logging.info('Email Command :- %s', email_cmd)
        os.system(email_cmd)
    else:
        body = 'Execution Failed...PFA log file'
        subject = '!!! Failure - testing !!!'

        email_cmd = """echo "{b}" | mailx -s "{s}" -a "{l}" "{to}" """.format(b=body, s=subject, l=log_file, to='<email_id>')
        logging.info('Email Command :- %s', email_cmd)
        os.system(email_cmd)


# Start of Execution
if __name__ == '__main__':

    log_file = initiate_logging()

    logging.info('!!! Execution Begins !!!')

    command ='echo Madhuri'
    result, status = execute_shell_command(command)
    
    if status != 0:
        logging.info("Exception in running shell command")
        STATUS = 'error'
        ERROR_MSG = '!!! Error !!! Execution failed !!!'
        MODULE_NAME = 'Execution Script'
        RETURN_CODE = ''
        error(STATUS, ERROR_MSG, MODULE_NAME, RETURN_CODE)
    else:
        command_result = result.decode('utf8').rstrip("\r\n")
        logging.info(command_result)

    email_log_file(log_file, status='success')
# End of Execution
