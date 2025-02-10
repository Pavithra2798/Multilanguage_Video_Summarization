# pip install google-cloud-translate==2.0.1
# pip install ipython

from flask import Flask, render_template, request, jsonify
import text_summary
import os
import re
from google.cloud import translate_v2 as translate

app = Flask(__name__)

client = translate.Client()

@app.route('/')
def upload_page():
    return render_template('video_summarization.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    video_urls = request.json.get('url')
    queries = request.json.get('question')
    language = request.json.get('language')
    video_url=video_urls.split(",")
    output_string = text_summary.summary_content(video_url) 
    summary_text = text_summary.generate_text(output_string, queries)
    output_text = summary_text
    
    if language != "en":
        print("translation")
        target_language = language
        translated_text = client.translate(output_text, target_language=target_language)
        return jsonify({'video_summary': translated_text['translatedText']})
    else:
        print("no translation")
        return jsonify({'video_summary': output_text})

@app.route('/summarize_video', methods=['POST'])
def summarize_video():
    url = request.json.get('url')
    language = request.json.get('language')
    video_url=url.split(",")
    output_string = text_summary.summary_content(video_url)
    summarized_content = text_summary.generate_summary(output_string)
    print(summarized_content)

    additional_summarized_content = text_summary.generate_additional_summary(output_string)
    print(additional_summarized_content)

    if language != "en":
        print("translation")
        target_language = language
        translated_text = client.translate(summarized_content, target_language=target_language)
        additional_translated_text = client.translate(additional_summarized_content, target_language=target_language)
        return jsonify({'video_summary': translated_text['translatedText'], 'additional_video_summary': additional_translated_text['translatedText']})
    else:
        print("no translation")
        return jsonify({'video_summary': summarized_content, 'additional_video_summary': additional_summarized_content})

 
if __name__ == '__main__':
    app.run(debug=True, port=8080)
    # app.run(debug=True)
