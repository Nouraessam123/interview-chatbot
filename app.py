from flask import Flask, request, jsonify
from transformers import pipeline, set_seed
from textblob import TextBlob

app = Flask(__name__)

# إعداد مولد الأسئلة من GPT-2
generator = pipeline('text-generation', model='gpt2')
set_seed(42)

@app.route('/')
def home():
    return "Mock Interview API is running!"

@app.route('/ask', methods=['POST'])
def generate_question():
    data = request.json
    job_title = data.get("job_title", "software engineer")

    prompt = f"Generate an interview question for a {job_title}:"
    result = generator(prompt, max_length=50, num_return_sequences=1)
    question = result[0]['generated_text'].replace(prompt, '').strip()

    return jsonify({"question": question})

@app.route('/evaluate', methods=['POST'])
def evaluate_answer():
    data = request.json
    answer = data.get("answer", "")

    analysis = TextBlob(answer)
    sentiment = analysis.sentiment.polarity

    if sentiment > 0.3:
        rating = "Strong"
    elif sentiment > 0:
        rating = "Neutral/Good"
    else:
        rating = "Needs Improvement"

    return jsonify({"sentiment_score": sentiment, "rating": rating})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=7860)
