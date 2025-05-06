from flask import Flask, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os
from openai import OpenAI
import re
from dotenv import load_dotenv


load_dotenv() 
# ---- CONFIG ----

token = os.environ.get("GITHUB_TOKEN") 
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)


@app.route("/generate-questions", methods=["POST"])
def generate_questions():
    data = request.json
    job_role = data.get("job_role", "Data Scientist")

    prompt = (
        f"Generate 3 behavioral and 2 technical interview questions for a {job_role} role. "
        "Please list only the questions, numbered."
    )
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
    )
    content = response.choices[0].message.content.strip()
    lines = content.split("\n")
    questions = [line.strip() for line in lines if line.strip() and "?" in line]

    return jsonify({"questions": questions})


@app.route("/evaluate-answer", methods=["POST"])
def evaluate_answer():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if not question or not answer:
        return jsonify({"error": "Missing question or answer"}), 400

    sentiment = analyzer.polarity_scores(answer)

    feedback_prompt = (
        f"Evaluate how well the following answer responds to the interview question "
        f"in terms of relevance, completeness, and clarity.\n\n"
        f"Question: {question}\n"
        f"Answer: {answer}\n\n"
        f"Provide detailed feedback, then add a score out of 10 using this format:\n"
        f"Rating: X/10"
    )

    feedback_response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": feedback_prompt}],
        temperature=0.7,
        top_p=1.0,
        max_tokens=500,
    )

    feedback_text = feedback_response.choices[0].message.content.strip()

    # --- SAFELY EXTRACT RATING ---
    rating = None
    if "Rating:" in feedback_text:
        rating_line = [line for line in feedback_text.split('\n') if "Rating:" in line]
        if rating_line:
            rating_str = rating_line[0].split(":")[1].strip()
            match = re.search(r'\d+', rating_str)
            if match:
                extracted = int(match.group())
                if 0 <= extracted <= 10:
                    rating = extracted

    return jsonify({
        "sentiment": sentiment,
        "feedback": feedback_text,
        "rating": rating
    })


if __name__ == "__main__":
    app.run(debug=True)
