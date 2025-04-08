from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.prompts import PromptTemplate

# This is a simple test file, that is not used in the actual application
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=cd67_M-a5xE", add_video_info=False, language=["en", "de", "fr", "it", "es"])
transcript = loader.load()[0].page_content
scope = "very detailed"
language = "German"

promptTemplate = """
You summarize the content of Youtube videos. For that you are given the following transcript {transcript}. 
The summary should be {scope}.
The summary should be in the language {language}.
"""
prompt = PromptTemplate(template=promptTemplate, input_variables=["transcript", "scope", "language"])
chain = prompt | llm
for chunk in chain.stream({"transcript": transcript, "scope": scope, "language": language}):
    print(chunk.content)