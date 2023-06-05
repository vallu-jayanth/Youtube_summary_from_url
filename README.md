# Youtube_summary_from_url

Create a summary of the youtube video from it's URL
which extracts important topics that are discussed in the video

It uses whisper to transcribe the audio from the URL given
and then this text is sent as context to openai API and prompt 
is given to summarize the text

Gradio is used to generate a simple UI which looks like this:

![image](https://github.com/vallu-jayanth/Youtube_summary_from_url/assets/76862594/2a577b7d-0ada-4bf1-8a67-fa6da47a18e2)
