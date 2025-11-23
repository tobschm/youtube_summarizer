import re
from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.prompts import PromptTemplate

def extract_video_id(url):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = re.compile(
        r'(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([^&?/\s]{11})'
    )
    match = query.search(url)
    if not match:
        # If no match, assume it might be the ID itself if it's 11 chars
        if len(url) == 11:
            return url
        raise ValueError("Could not extract video ID from URL")
    return match.group(1)

def summarize(url, scope, language):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key="YOUR_API_KEY")

    video_id = extract_video_id(url)
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en", "de", "fr", "it", "es"])
    text = " ".join([t.text for t in transcript])

    promptTemplate = """
    You summarize the content of Youtube videos. For that you are given the following transcript: {transcript}. 
    The summary should be {scope}.
    The summary should be in the language {language}.
    Don't include any other information. Don't mention that you are referencing a video in the summary. Use fitting headlines and paragraphs.
    """
    
    prompt = PromptTemplate(template=promptTemplate, input_variables=["transcript", "scope", "language"])
    
    # Create the chain and stream the output
    chain = prompt | llm
    return chain.invoke({"transcript": text, "scope": scope, "language": language}).content

