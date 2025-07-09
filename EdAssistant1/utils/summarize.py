from transformers import pipeline
import textwrap

# Initialize the BART summarization pipeline with error handling
try:
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    print(f"Error initializing summarizer: {str(e)}")
    summarizer = None

def chunk_text(text, chunk_size=1024):
    """
    Splits the text into smaller chunks based on the token limit.
    
    Args:
        text (str): The long input text to split.
        chunk_size (int): The maximum number of tokens per chunk (default: 1024).
        
    Returns:
        list: A list of text chunks.
    """
    wrapped_text = textwrap.fill(text, chunk_size)
    chunks = wrapped_text.split('\n')
    return chunks

def summarize_text(text, max_length=150, min_length=50):
    """
    Summarizes the input text using BART while handling long text by splitting it into chunks.
    
    Args:
        text (str): The text to summarize.
        max_length (int): Maximum length of the summary.
        min_length (int): Minimum length of the summary.
        
    Returns:
        str: The combined summarized text.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")

    if summarizer is None:
        raise RuntimeError("Summarization model failed to initialize")

    try:
        # Clean and prepare the text
        text = text.strip()
        if len(text) < min_length:
            return text  # Return original text if it's too short

        # Split the text into chunks if it's too long
        chunks = chunk_text(text)
        summaries = []

        # Summarize each chunk and collect the results
        for chunk in chunks:
            if chunk.strip():  # Only process non-empty chunks
                summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
                summaries.append(summary[0]['summary_text'])

        # Combine the summaries from each chunk
        final_summary = " ".join(summaries)
        return final_summary

    except Exception as e:
        print(f"Error during summarization: {str(e)}")
        raise RuntimeError(f"Summarization failed: {str(e)}")
