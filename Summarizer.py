from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_core.prompts import PromptTemplate

def summarize(url, scope, language):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
    llm.google_api_key = "YOUR_API_KEY"  # Replace with your actual API key

    transcript = YouTubeTranscriptApi.get_transcript(url, languages=["en", "de", "fr", "it", "es"])
    text = " ".join([t['text'] for t in transcript])

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

