import re
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi


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


def getYoutubePrompt(video_id):

  if "v=" in video_id:
    video_id = video_id.split("v=")[1]

  transcriptData = YouTubeTranscriptApi.get_transcript(video_id)
  words_in_video = " ".join([item["text"] for item in transcriptData])

  if len(words_in_video.split(" ")) >= 2000:
    words_in_video = " ".join(words_in_video.split(" ")[:2000])

  words_in_video = re.sub("\n", " ", words_in_video)
  prompt = "Please create a summary of the following voice-to-text transcript of an educational Youtube video:\n\n"
  prompt += "\"\"\"" + words_in_video + "\"\"\"\n\n"
  return prompt