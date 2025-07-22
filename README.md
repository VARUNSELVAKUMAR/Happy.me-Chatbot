# 😊 Happy.me – Emotion-Aware Conversational Chatbot

> Real-time facial emotion recognition meets empathetic AI conversations.

---

## 🚀 Overview

**Happy.me** is a full-stack AI chatbot that leverages real-time webcam-based emotion detection and conversational intelligence to deliver empathetic, multilingual, and context-aware experiences. The chatbot dynamically adjusts its responses based on the user’s detected emotions and provides features such as secure authentication and exportable chat history.

---

## 🧠 Features

- 🎥 Real-time facial emotion recognition via webcam
- 💬 Emotion-aware GPT/Gemini conversational AI
- 🌍 Multilingual support (English, Hindi, Spanish, French, etc.)
- 📤 Chat export as PDF and Word
- 🔐 Secure JWT-based authentication
- 📱 Responsive UI built with modern React stack

---

## 🏗️ Tech Stack

| Layer     | Stack                                 |
|-----------|----------------------------------------|
| Frontend  | Next.js, TypeScript, Tailwind CSS      |
| Backend   | FastAPI (Python), SQLite/PostgreSQL    |
| AI Model  | GPT-4 or Gemini Pro (via API)          |
| ML Model  | CNN-based emotion detection using OpenCV |
| Export    | ReportLab, python-docx for file export |

---

## 📁 Project Structure

```
Happy.me-Chatbot/
├── backend/
│   └── app/
│       ├── main.py
│       ├── emotion/
│       ├── chatbot/
│       ├── export/
│       ├── auth/
│       └── models/
├── frontend/
│   ├── pages/
│   ├── components/
│   ├── hooks/
│   └── public/
```

---

## ⚙️ Installation

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Fill in your environment values
```

### Frontend

```bash
cd frontend
yarn install
cp .env.local.example .env.local  # Add required frontend environment variables
```

---

## 🧪 Running Locally

### Backend (FastAPI)

```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend (Next.js)

```bash
cd frontend
yarn dev
```

### Optional: Streamlit Dashboard

```bash
cd backend
streamlit run app/streamlit_app.py
```

---

## 🔐 Environment Variables

### Backend `.env`
```
OPENAI_API_KEY=your_api_key
SECRET_KEY=your_secret
DATABASE_URL=sqlite:///./test.db
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend `.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🌐 Multilingual Support

Multilingual chat translation is handled using:
- `react-i18next` in frontend
- `googletrans` in backend

Supported languages include English, Hindi, Spanish, French, and more.

---

## 💬 Emotion-Aware AI Chatbot

- Emotion is detected from the user’s webcam stream
- Chat prompts are generated with emotional context
- Supports OpenAI’s GPT or Google’s Gemini as backend

---

## 📤 Chat Export Feature

Users can download chat logs as:
- PDF via ReportLab
- Word (.docx) via python-docx

Backend processes messages and returns downloadable files on request.

---

## 🐳 Docker Support

### Example Docker Compose Setup

```yaml
version: "3"
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    env_file:
      - ./frontend/.env.local
```

---

## 🧪 Development Standards

- **Linting**: `black`, `flake8`, `eslint`, `prettier`
- **Testing**:
  - Backend: `pytest`
  - Frontend: `yarn test`
- **Branching**:
  - `main`: production
  - `dev`: active development
  - `feature/*`: feature-specific branches

---

## 🛣️ Roadmap

- [ ] Text-to-speech audio replies
- [ ] Emotion trend visualization
- [ ] Push notifications
- [ ] Admin analytics dashboard
- [ ] PostgreSQL migration and CI/CD support

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with conventional commit messages
4. Push the branch and create a pull request

---

## 📝 License

MIT License © 2024 [DhruvJ2k4](https://github.com/DhruvJ2k4)
