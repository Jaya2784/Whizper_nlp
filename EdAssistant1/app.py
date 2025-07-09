import openai
from flask import Flask, render_template, request, send_file, jsonify
from utils.ocr_utils import ocr_from_pdf, extract_text_from_image
from utils.summarize import summarize_text
from gtts import gTTS
import os
from flask_cors import CORS
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
import requests

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key here


# Set your Gemini API key here directly in the code
GEMINI_API_KEY = 'AIzaSyDlBIw1F_Pva3fZ7E49fTyagNdi00nEDy4'  # Replace this with your actual Gemini API key

# Load the question-answering pipeline
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Load the FLAN-T5 model and tokenizer
#flan_t5_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
#flan_t5_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Upload page (for file upload)
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return render_template('upload.html', error="No file selected")
            
            file = request.files['file']
            if file.filename == '':
                return render_template('upload.html', error="No file selected")

            if file:
                file_path = f"uploads/{file.filename}"
                file.save(file_path)

                # Determine if the file is a PDF or image and call the respective OCR function
                try:
                    if file.filename.lower().endswith('.pdf'):
                        text = ocr_from_pdf(file_path)  # OCR on PDF
                    else:
                        text = extract_text_from_image(file_path)  # OCR on image

                    if not text or text.strip() == "":
                        return render_template('upload.html', error="No text could be extracted from the file")

                    # Generate summary from the extracted text
                    try:
                        summary = summarize_text(text)
                        return render_template('results.html', summary=summary, original_text=text)
                    except Exception as e:
                        return render_template('upload.html', error=f"Error during summarization: {str(e)}")
                except Exception as e:
                    return render_template('upload.html', error=f"Error processing file: {str(e)}")
        except Exception as e:
            return render_template('upload.html', error=f"An error occurred: {str(e)}")  
    return render_template('upload.html')

# Example function to call the Gemini API
def get_gemini_answer(question, format_type="paragraph"):
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY is not set")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": question}
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Response Status Code: {response.status_code}")
        print(f"Full Response JSON: {response.json()}")  # Log the full response

        if response.status_code == 200:
            data = response.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                content = data['candidates'][0].get('content', {})
                parts = content.get('parts', [])
                if len(parts) > 0:
                    answer = parts[0].get('text', "No response text found")
                    # Remove asterisks from the response
                    formatted_answer = answer.replace('*', '')

                    # Format the response based on the format_type
                    if format_type == "points":
                        formatted_answer = "\n".join(
                            [f"- {line.strip()}" for line in formatted_answer.split('.') if line.strip()]
                        )
                    elif format_type == "paragraph":
                        formatted_answer = "\n".join(
                            [line.strip() for line in formatted_answer.split('.') if line.strip()]
                        )

                    return formatted_answer
                else:
                    return "No parts found in response"
            else:
                return "No candidates found in response"
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception occurred while calling Gemini API: {str(e)}")
        return None

# New route for generating answers using Gemini API
@app.route('/generate-answer', methods=['POST'])
def generate_answer():
    try:
        question = request.json.get('question')
        format_type = request.json.get('format')  # New parameter for format type
        if not question:
            return jsonify({'error': "Question is required"}), 400

        gemini_answer = get_gemini_answer(question, format_type)  # Pass format_type
        if gemini_answer:
            return jsonify({'answer': gemini_answer})
        else:
            return jsonify({'error': "Failed to get a response from Gemini API"}), 500
    except Exception as e:
        print(f"Error in /generate-answer route: {str(e)}")
        return jsonify({'error': f"Error generating response: {str(e)}"}), 500

# Generate audio from text (existing function)
@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    text = request.form.get('text')
    audio_type = request.form.get('type')  # New parameter to determine text type
    if text:
        print(f"Received text: {text}, Type: {audio_type}")  # Debugging line
        tts = gTTS(text=text, lang='en')
        audio_file = 'audio.mp3'
        tts.save(audio_file)
        return send_file(audio_file, as_attachment=True)
    return "No text provided", 400
@app.route('/download-audio', methods=['POST'])
def download_audio():
    data = request.json
    text = data.get('text')
    filename = data.get('filename', 'audio')

    if not text:
        return {"error": "No text provided"}, 400

    # Generate audio file using gTTS
    tts = gTTS(text)
    filepath = f"static/audio/{filename}.mp3"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    tts.save(filepath)

    # Serve the file to the user
    return send_file(filepath, as_attachment=True)
if __name__ == "__main__":
    app.run(debug=True)
