from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import YoutubeLoader
from langchain_core.prompts import PromptTemplate

def summarize(url, scope, language):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
    llm.google_api_key = "YOUR_GOOGLE_API_KEY"  # Replace with your actual API key

    loader = YoutubeLoader.from_youtube_url(url, add_video_info=False, language=["en", "de", "fr", "it", "es"])
    transcript = loader.load()[0].page_content

    promptTemplate = """
    You summarize the content of Youtube videos. For that you are given the following transcript {transcript}. 
    The summary should be {scope}.
    The summary should be in the language {language}.
    Don't include any other information. Don't mention that you are referencing a video in the summary. Use fitting headlines and paragraphs.
    """
    
    prompt = PromptTemplate(template=promptTemplate, input_variables=["transcript", "scope", "language"])
    
    # Create the chain and stream the output
    chain = prompt | llm
    return chain.invoke({"transcript": transcript, "scope": scope, "language": language}).content

