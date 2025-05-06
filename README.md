
# 🧠 AI Interview Chatbot – Flask API

This Flask-based API supports generating interview questions and evaluating user answers using GPT and sentiment analysis.

---

## 📍 Endpoints

### 1. `POST /generate-questions`

Generates 5 interview questions based on the provided job role.

#### 🔸 Request
**URL**: `/generate-questions`  
**Method**: `POST`  
**Content-Type**: `application/json`

**Body:**
```json
{
  "job_role": "Data Scientist"
}
```

#### 🔸 Success Response – `200 OK`
```json
{
  "questions": [
    "Can you describe a challenging project you've worked on?",
    "How do you approach problem-solving under pressure?",
    "Tell me about a time you worked in a team.",
    "What is overfitting in machine learning?",
    "Explain the difference between supervised and unsupervised learning."
  ]
}
```

---

### 2. `POST /evaluate-answer`

Evaluates a user’s answer to a given interview question and returns detailed feedback and a rating out of 10.

#### 🔸 Request
**URL**: `/evaluate-answer`  
**Method**: `POST`  
**Content-Type**: `application/json`

**Body:**
```json
{
  "question": "What is overfitting in machine learning?",
  "answer": "Overfitting happens when the model learns the training data too well..."
}
```

#### 🔸 Success Response – `200 OK`
```json
{
  "feedback": "Your answer is clear and relevant. Rating: 8/10",
  "rating": 8
}
```

---

## ❌ Error Responses

### Missing Parameters – `400 Bad Request`
```json
{
  "error": "Missing 'question' or 'answer' in request."
}
```

### Feedback Extraction Failed – `200 OK` (but rating is null)
```json
{
  "feedback": "Answer provided but could not extract a numeric rating.",
  "rating": null
}
```

### Internal Server Error – `500 Internal Server Error`
```json
{
  "error": "An unexpected error occurred during evaluation."
}
```

---

## 🧪 Example cURL Request

```bash
curl -X POST http://127.0.0.1:5000/evaluate-answer \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain the difference between supervised and unsupervised learning.",
    "answer": "Supervised learning uses labeled data..."
}'
```

---

## 📌 Notes for Frontend Developers

- `feedback` should be displayed clearly as text.
- `rating` can be visualized using stars or progress bar.
- If `rating = null`, show a warning or message.
- Only show "Next Question" button after receiving feedback.
