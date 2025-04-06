from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 

loader = YoutubeLoader.from_youtube_url("https://www.youtube.com/watch?v=2rphLdQWexU&ab_channel=BBCNews", add_video_info=False)
transcript = loader.load()[0].page_content
scope = "very detailed"

promptTemplate = """
You summarize the content of Youtube videos. For that you are given the following transcript {transcript}. The summary should be {scope}.
"""
prompt = PromptTemplate(template=promptTemplate, input_variables=["transcript", "scope"])
chain = prompt | llm
for chunk in chain.stream({"transcript": transcript, "scope": scope}):
    print(chunk.content)