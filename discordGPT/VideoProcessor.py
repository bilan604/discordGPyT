import re
from openAI import askOpenAI003
from youtube_transcript_api import YouTubeTranscriptApi


def getTranscript(video_id):
  transcript = YouTubeTranscriptApi.get_transcript(video_id)
  return transcript


def getVideoString(transcriptData):
  s = " ".join([item["text"] for item in transcriptData])
  s = re.sub("\n", " ", s)
  return s



class VideoProcessor(object):

  def __init__(self, video_id=""):
    self.video_id = video_id
    self.video_data = []
    self.video_words = ""
    self.jsonData = {}
    self.initialize()

  def initialize(self):
    self.video_data = getTranscript(self.video_id)
    self.video_words = getVideoString(self.video_data)
    return

  async def summarize(self):
    prompt = "Please create a summary of the following voice-to-text transcript of an educational Youtube video:\n\n"
    prompt += "\"\"\"" + self.video_words + "\"\"\"\n\n"
    summary = await askOpenAI003(prompt)
    self.jsonData["summary"] = summary
    return summary