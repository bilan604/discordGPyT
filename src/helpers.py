import re
from src.GoogleSearch import ask_question
from youtube_transcript_api import YouTubeTranscriptApi


async def getYoutubePrompt(video_id):

    if "v=" in video_id:
        video_id = video_id.split("v=")[1]

    transcriptData = "None"
    # API call
    transcriptData = YouTubeTranscriptApi.get_transcript(video_id)

    words_in_video = " ".join([item["text"] for item in transcriptData])

    if len(words_in_video.split(" ")) >= 2000:
        words_in_video = " ".join(words_in_video.split(" ")[:2000])

    words_in_video = re.sub("\n", " ", words_in_video)
    prompt = "Please create a summary of the following voice-to-text transcript of an educational Youtube video:\n\n"
    prompt += "\"\"\"" + words_in_video + "\"\"\"\n\n"
    return prompt

async def doGoogleSearch(query):
    suggestedQuestionResults = ask_question(query)
    responseContent = ""
    idx = 0
    for key, val in suggestedQuestionResults.items():
        responseContent += key + "\n" + val + "\n\n"
        if idx == 0:
            responseContent += "Other Related Questions:\n"
        idx += 1
    return responseContent