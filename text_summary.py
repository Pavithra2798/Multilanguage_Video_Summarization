# pip install youtube-transcript-api

import io
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
import vertexai
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

vertexai.init(project="<project-id>", location="us-central1")
from vertexai.preview.generative_models import GenerativeModel, Part

def summary_content(video_urls):  
    
    video_ids = [get_youtube_video_id(url) for url in video_urls]
    print(video_ids)
    
    video_ids_flattened_list = []
    for sublist in video_ids:
        video_ids_flattened_list.extend(sublist)
        
    video_response = {}
    for ids in video_ids_flattened_list:
        text = YouTubeTranscriptApi.get_transcript(ids)
        response = ""
        for i in text:
            response = response+ " " + "{}".format(i["text"])
        video_response[ids] = response

    output_string = ""
    for key, value in video_response.items():
        output_string += "Video ID: " + key + "\n"
        output_string += "Transcript: " + value + "\n\n--------------------\n\n"
        
    return output_string
 
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def generate_text(response, user_query) -> str: 

    multimodal_model = GenerativeModel("gemini-pro")
    op_response = multimodal_model.generate_content(f'''Context : {response}.
    User Query : {user_query}.
    The context is a transcript of one or many videos. The user might ask question from any of the 
    video context. So you need to read the entire context thoroughly and find relevant information
    for the user's question. If there are multiple contents in the context for the user question,
    combine and generate a well-researched answer to the user question.

    If the transcript is very large, make the summary also large.
    The generated output should not be less than 1000 words.

    Do not format using markdown language. 
    You are an AI assistant that can generate HTML and CSS code for creating visually effective document
    content.
    Please ensure that all content in the output is consistently formatted using HTML tags for visual enhancement. 
    Use HTML tags such as <b> for bold text, <i> for italics, <ul> and <ol> for 
    lists, <p> for paragraphs, <h3> for headings, and <a> for hyperlinks. 
    Additionally, apply CSS styles for proper layout, typography, colors, and any other visual enhancements. 
    If applicable, utilize <div> and <span> for structuring and styling, <img> for images, and <table> for 
    tabular data. It's essential that the HTML formatting and CSS styles are applied uniformly and
    effectively to elevate the visual appeal of the output. Apply CSS styles to specify colors 
    for each heading level. Use these color codes #a24756 and #59000f only for headings.
    The use of colors should align with the overall design and visual appeal of 
    the output. Consistency in color choices and readability should be considered when applying 
    these styles.Please pay close attention to applying HTML tags and CSS styles consistently 
    and comprehensively and ensure that you are not using markdown language.

    use sample style like the below:
    h3 color: #a24756; 
    h4 color: #59000f;
    ul list-style-position: inside;
    ol list-style-position: inside;

    If the answer is not in the context, provide "answer not available"
    ''')
    print(op_response.text)
    to_markdown(op_response.text)

    return op_response.text

def get_youtube_video_id(*urls):
    url_id = []
    for url in urls:    
        query = urlparse(url)
        if query.hostname == 'www.youtube.com' or query.hostname == 'youtube.com':
            if query.path == '/watch':
                id = parse_qs(query.query)['v'][0]
                url_id.append(id)
            elif query.path.startswith('/embed/'):
                id = query.path.split('/')[2]
                url_id.append(id)
            elif query.path.startswith('/v/'):
                id = query.path.split('/')[2]
                url_id.append(id)
        elif query.hostname == 'youtu.be':
            id = query.path[1:]
            url_id.append(id)
        else:
            return None
    print(url_id)
    return url_id

def generate_summary(response) -> str: 

    multimodal_model = GenerativeModel("gemini-pro")
    op_response = multimodal_model.generate_content(f''' 
    Context : {response}.
    For the above context, extract the key information and provide a summary. 
    Provide as much information possible by using limited words.
    If you are not able to convey the information using less words, use as much words needed to convey the 
    information. But do not eliminate the information that has been said in the video when summarizing.
    Provide the summary separately for each of the video.
    Extract the exact Video title that is mentioned in the video and provide the points under each 
    of the video title. Do not provide any additional content other than in the transcript.
    If you do not know the exact video title give the title as "video1", "video2" etc. 
    Do not include the video ID. Do not include words like "Video Title", "section" 
    etc for heading. 
    
    Do not format using markdown language. 
    You are an AI assistant that can generate HTML and CSS code for creating visually effective document
    content.
    Please ensure that all content in the output is consistently formatted using HTML tags for visual enhancement.
    Use HTML tags such as <b> for bold text, <i> for italics, <ul> and <ol> for 
    lists, <p> for paragraphs, <h3> for headings, and <a> for hyperlinks. 
    Additionally, apply CSS styles for proper layout, typography, colors, and any other visual enhancements. 
    If applicable, utilize <div> and <span> for structuring and styling, <img> for images, and <table> for 
    tabular data. It's essential that the HTML formatting and CSS styles are applied uniformly and
    effectively to elevate the visual appeal of the output. Apply CSS styles to specify different colors 
    for each heading level. Use these color codes #a24756 and #59000f only for headings.
    The use of colors should align with the overall design and visual appeal of 
    the output. Consistency in color choices and readability should be considered when applying 
    these styles.Please pay close attention to applying HTML tags and CSS styles consistently 
    and comprehensively and ensure that you are not using markdown language.

    use sample style like the below:
    h3 color: #a24756; 
    h4 color: #59000f;
    ul list-style-position: inside;
    ol list-style-position: inside;
    
    ''')

    to_markdown(op_response.text)

    return op_response.text

def generate_additional_summary(response) -> str: 

    multimodal_model = GenerativeModel("gemini-pro")
    op_response = multimodal_model.generate_content(f''' Context : {response}.
    From the above context identify the main topic and give me the information based on the topic
    that is not available in the provided context.
    Extract the exact Video title that is mentioned in the video and provide the points under each 
    of the video title. 
    The generated content should not be less than 2000 words.

    Do not format using markdown language. 
    You are an AI assistant that can generate HTML and CSS code for creating visually effective document
    content.
    Please ensure that all content in the output is consistently formatted using HTML tags for visual enhancement.
    Use HTML tags such as <b> for bold text, <i> for italics, <ul> and <ol> for 
    lists, <p> for paragraphs, <h3> for headings, and <a> for hyperlinks. 
    Additionally, apply CSS styles for proper layout, typography, colors, and any other visual enhancements. 
    If applicable, utilize <div> and <span> for structuring and styling, <img> for images, and <table> for 
    tabular data. It's essential that the HTML formatting and CSS styles are applied uniformly and
    effectively to elevate the visual appeal of the output. Apply CSS styles to specify different colors 
    for each heading level. Use these color codes #a24756 and #59000f only for headings.
    The use of colors should align with the overall design and visual appeal of 
    the output. Consistency in color choices and readability should be considered when applying 
    these styles.Please pay close attention to applying HTML tags and CSS styles consistently 
    and comprehensively and ensure that you are not using markdown language.

    use sample style like the below:
    h3 color: #a24756; 
    h4 color: #59000f;
    ul list-style-position: inside;
    ol list-style-position: inside;
    
    ''')

    to_markdown(op_response.text)

    return op_response.text
