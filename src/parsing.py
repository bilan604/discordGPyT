import re
import os
from datetime import datetime



def load_credentials():
    rightPath = False
    for file in os.listdir():
        if file == '.env':
            rightPath = True
            break
    if not rightPath:
        print("Please check path: .env file not in current working directory.")
        return {}
    
    credentials = {}
    with open('.env', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            lineLst = line.split("=")
            KEY = lineLst[0].strip()
            VALUE = "".join(lineLst[1:]).strip()
            credentials[KEY] = VALUE
    return credentials


def check_spam(last_time, message_time_stack):
    current_time = datetime.now()
    diff1 = current_time - last_time
    secondsSinceLastMessage = getSeconds(diff1)
    if secondsSinceLastMessage < 3:
        print("Recieved spam", secondsSinceLastMessage)
        return True, message_time_stack
    
    if len(message_time_stack) >= 10:
        stackFirstTime = message_time_stack[0]
        diff2 = current_time - stackFirstTime
        secondsForStack = getSeconds(diff2)
        if secondsForStack < 150:
            print("StackSpam", secondsForStack)
            if secondsForStack < 20:
                ghost = True    
            return ghost, message_time_stack

        message_time_stack.append(current_time)
        message_time_stack = message_time_stack[1:]
    else:
        message_time_stack.append(current_time)
        return False, message_time_stack

def getSeconds(timeDiff):
        timeDiff = str(timeDiff)
        hours, minutes, seconds = [val for val in timeDiff.split(":")]
        if "." in seconds:
            seconds = seconds.split(".")[0]

        return int(seconds) + (60 * int(minutes)) + (3600 * int(hours))


