## Multi-Lingual Video Summarization with LLMs
 

The explosion of online video content presents a challenge: quickly extracting relevant information. Watching entire videos is time-consuming, especially for non-native speakers. To address this, a system was developed to automatically summarize video content in multiple languages.

 

The task was to create a solution using LLMs to generate accurate and concise summaries from video URLs, with multi-language support. This was achieved by leveraging Google Cloud's Gemini Pro and Google Translate. Users input YouTube URLs, and the system extracts transcripts using youtube_transcript_api. A prompt guides Gemini Pro to generate summaries in the user's preferred language, including background context and related topics. Users can also ask questions about the video, with the LLM retrieving answers from the transcript. Google Translate ensures multi-lingual accessibility. The system is deployed as a Flask web application.

 

The prototype successfully generates concise, informative summaries in multiple languages, enabling quick content comprehension. Users can also ask questions and receive comprehensive answers. This technology revolutionizes video consumption, making it more accessible and efficient for everyone.

## **Skills and Technology:** 
Python, Gemini-Pro, Prompt Engineering, VertexAI, GCP, Cloud Build, Cloud Function, HTML, CSS
