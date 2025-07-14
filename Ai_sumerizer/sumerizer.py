from transformers import pipeline

# Load once at start
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

def split_text(text, max_tokens=900):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_tokens:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def summarize_text(text: str) -> str:
    chunks = split_text(text)
    summaries = []

    for chunk in chunks:
        if len(chunk.strip()) == 0:
            continue
        result = summarizer(chunk, max_length=130, min_length=50, do_sample=False)
        summaries.append(result[0]['summary_text'])

    return " ".join(summaries)
