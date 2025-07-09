# Whizper - Intelligent Voice Learning Assistant

Whizper is an AI-powered web application that transforms educational materials (PDFs and images) into accessible, summarized text and audio. It leverages OCR, advanced summarization, and conversational AI (Google Gemini) to make learning content more accessible, especially for visually impaired users or those who prefer audio-based learning.

---

## Features

- **Upload Educational Content:** Supports PDF and image files (JPG, PNG).
- **OCR Extraction:** Extracts text from scanned documents and images using Tesseract OCR.
- **AI Summarization:** Summarizes lengthy content using a BART-based transformer model.
- **Conversational Q&A:** Ask questions about your content using Google Gemini API.
- **Text-to-Speech:** Converts both original and summarized text to downloadable audio (MP3) using gTTS.
- **Modern UI:** Responsive, accessible, and visually appealing interface.

---

## Project Structure

```
.
├── app.py                  # Main Flask application
├── .env                    # Environment variables (API keys)
├── utils/
│   ├── ocr_utils.py        # OCR utilities for PDF/image text extraction
│   └── summarize.py        # Summarization utilities using transformers
├── static/
│   ├── css/
│   │   └── styles.css      # Main stylesheet
│   ├── js/
│   │   ├── result.js       # JS for results page (Q&A, audio controls)
│   │   └── script.js       # (empty/placeholder)
│   └── audio/              # Generated audio files
├── templates/
│   ├── index.html          # Home page
│   ├── about.html          # About page
│   ├── upload.html         # Upload page
│   └── results.html        # Results (text, summary, Q&A)
├── uploads/                # Uploaded files (PDFs/images)
└── audio.mp3               # Temporary audio file
```

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone <your-repo-url>
cd EdAssistant1
```

### 2. Install Dependencies

Make sure you have Python 3.8+ and `pip` installed.

```sh
pip install -r requirements.txt
```

**Required Python Packages:**
- Flask
- flask-cors
- openai
- gtts
- transformers
- torch
- pdf2image
- pytesseract
- Pillow
- requests

**System Requirements:**
- Tesseract OCR (install from https://github.com/tesseract-ocr/tesseract)
- Poppler (for PDF to image conversion, install from http://blog.alivate.com.au/poppler-windows/ or your package manager)

### 3. Set API Keys

- **Google Gemini API Key:** Add your Gemini API key to the `.env` file as `GEMINI_API_KEY=...`
- **OpenAI API Key:** Set in `app.py` (currently hardcoded).

> **Note:** For production, never hardcode API keys. Use environment variables or a secure secrets manager.

### 4. Run the Application

```sh
python app.py
```

The app will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## Usage

1. **Home:** Learn about Whizper and its features.
2. **Upload:** Upload a PDF or image. The app extracts and summarizes the content.
3. **Results:** 
   - View original and summarized text.
   - Listen to or download audio versions.
   - Ask questions about the content (Q&A tab).
4. **About:** Learn more about the mission and technology.

---

## File Descriptions

- [`app.py`](app.py): Main Flask backend. Handles routing, file uploads, OCR, summarization, Q&A (Gemini), and audio generation.
- [`utils/ocr_utils.py`](utils/ocr_utils.py): Functions for extracting text from PDFs and images using Tesseract.
- [`utils/summarize.py`](utils/summarize.py): Summarizes text using a BART transformer model.
- [`static/js/result.js`](static/js/result.js): Handles tab switching, Q&A AJAX, and audio controls on the results page.
- [`static/css/styles.css`](static/css/styles.css): Main stylesheet for the app.
- [`templates/`](templates/): Jinja2 HTML templates for all pages.

---

## API Endpoints

- `/upload` (GET/POST): Upload and process files.
- `/generate-answer` (POST): Q&A endpoint (expects JSON: `{question: "...", format: "paragraph"|"points"}`).
- `/generate-audio` (POST): Generate audio from text (form data).
- `/download-audio` (POST): Download audio as MP3 (JSON: `{text: "...", filename: "..."}`).

---

## Notes

- Uploaded files and generated audio are stored locally.
- Summarization and Q&A rely on external APIs/models and may require internet access.
- For best results, ensure Tesseract and Poppler are correctly installed and available in your system PATH.

---

## License

This project is for educational purposes. Please review and update the license as appropriate for your use case.

---

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Transformers (HuggingFace)](https://huggingface.co/transformers/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [gTTS](https://pypi.org/project/gTTS/)
- [Google Gemini API](https://ai.google.dev/)

---
