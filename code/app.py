import whisper
from pytube import YouTube
from gpt_summarizer import get_completion
import gradio as gr
import os
import re
import logging

logging.basicConfig(level=logging.INFO)
model = whisper.load_model("base")

def get_text(url):
    #try:
    if url != '':
        output_text_transcribe = ''

    yt = YouTube(url)
    #video_length = yt.length --- doesn't work anymore - using byte file size of the audio file instead now
    #if video_length < 5400:
    video = yt.streams.filter(only_audio=True).first()
    out_file=video.download(output_path=".")

    file_stats = os.stat(out_file)
    logging.info(f'Size of audio file in Bytes: {file_stats.st_size}')
    
    if file_stats.st_size <= 30000000:
        base, ext = os.path.splitext(out_file)
        new_file = base+'.mp3'
        os.rename(out_file, new_file)
        a = new_file
        result = model.transcribe(a)
        return result['text'].strip()
    else:
        logging.error('Videos for transcription on this space are limited to about 1.5 hours. Sorry about this limit but some joker thought they could stop this tool from working by transcribing many extremely long videos. Please visit https://steve.digital to contact me about this space.')


def get_summary(url):
    text = get_text(url)
    prompt = f"""Your task is to summarize the given text\
    Based on given text, Identify the following:\
    - Topics discussed -each topic should be comma seperated 
    - summary of the whole text\
    the text is delimitited with backticks.\
    format your response as article where you can select each topic\
    to view the summary\
    text : ```{text}```
        """
    return get_completion(prompt)
if __name__=='__main__':
    with gr.Blocks() as demo:
        gr.Markdown("<h1><center>Free Fast YouTube URL Video-to-Text-Summary using OpenAI's Whisper and GPT Models</center></h1>")
        gr.Markdown("<center>Enter the link of any YouTube video to generate a text transcript of the video and then create a summary of the video transcript using openai API by prompting GPT model.</center>")
        gr.Markdown("<center><b>'Whisper is a neural net that approaches human level robustness and accuracy on English speech recognition.'</b></center>")
        gr.Markdown("<center>Transcription and summarization takes 25-30 seconds per minute of the video (bad audio/hard accents slow it down a bit). #patience</center>")
        
        input_text_url = gr.Textbox(placeholder='Youtube video URL', label='YouTube URL')
        result_button_transcribe = gr.Button('Transcribe and summarize')
        output_text_transcribe = gr.Textbox(placeholder='Summary of the YouTube video.', label='Transcript')      
        result_button_transcribe.click(get_summary, inputs = input_text_url, outputs = output_text_transcribe)

    demo.queue(default_enabled = True).launch(debug = True)
