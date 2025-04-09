# Overview
This application automatically generates a text-summary of a Youtube-video.
The user can select the desired level of detail and the language in which the summary should be generated.
Before using, the actual Gemini api-key has to be entered in Summarizer.py. This should later be replaced by a Settings-UI which allows the storage of the api-keys in a SQLite database (see Planned features section).

## Technical description
A simple UI was built using PyQt6. 
Youtube_transcript_api is used to get the transcript of the Youtube video. Afterwards LangChain is used to generate a summary of the transcript with Google Gemini

## Planned features
* Text streaming
* Multiple LLMs: Switch between Gemini-, ChatGPT- and Deepseek-models
* SQLite Database for API-keys
* Settings UI (to set API-keys)
* Audio output

## License
[MIT](https://choosealicense.com/licenses/mit/)