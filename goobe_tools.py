from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools import YouTubeSearchTool
from pytubefix import YouTube
from pydub import AudioSegment
import os
import whisper
import re
import subprocess
import json

@tool
def youtube_link(query: str, max_results: int) -> dict[str, any]:
  """This tool searches videos on YouTube and returns links based on the search and the quantity received."""
  youtube_tool = YouTubeSearchTool()
  return youtube_tool.run(f"{query},{max_results}")

@tool
def google_trends(query: str) -> dict[str, any]:
  """Return information of google trends topics in the last year only, the input must be related to the user's query."""
  gtool_wrapper = GoogleTrendsQueryRun(api_wrapper=GoogleTrendsAPIWrapper())
  return gtool_wrapper.run(query)

def video_to_text(url):
    """This tool receives the URL of a YouTube video given by the user and returns what was said in text."""
    
    try:
        
        def get_youtube_tokens():
            result = subprocess.run(['node', 'generate_token.js'], stdout=subprocess.PIPE)
            tokens = json.loads(result.stdout)
            return tokens['visitorData'], tokens['poToken']
        
        visitor_data, po_token = get_youtube_tokens()        
        yt = YouTube(url, client='WEB_CREATOR', use_po_token=True, po_token_verifier=po_token)
        video = yt.streams.filter(only_audio=True).first()
        title = yt.title  
        title_safe = re.sub(r'[\/:*?"<>|]', '', title)  
        out_file = video.download(filename=f"{title_safe}.mp4")        
        wav_filename = f"{title_safe}.wav"
        AudioSegment.from_file(f"{title_safe}.mp4").set_frame_rate(16000).export(wav_filename, format="wav")   
        model = whisper.load_model("base")       
        audio = whisper.load_audio(wav_filename)
        result = model.transcribe(audio)        
        text = result["text"]
        
        os.remove(f"{title_safe}.mp4")
        os.remove(f"{title_safe}.wav")

        return text

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None
      
@tool
def ddg_search(query):
  """This tool receives a input to search on Internet, can be used to return current information and news"""
  search = DuckDuckGoSearchResults(backend="news", max_results=3)
  return search.invoke({"query": query})