# Payzen Bank - Premium Digital Banking Experience

Payzen Bank is a state-of-the-art digital banking application built with a focus on modern aesthetics, security, and AI-driven user experience.

## ✨ Features

- **AI Chat Assistant**: Powered by Google Gemini 2.0 Flash, providing multilingual support (English & Marathi).
- **Secure Authentication**: JWT-based auth with brute-force protection and email OTP verification.
- **Smart Dashboard**: Real-time balance updates, interactive bank card, and quick access to banking services.
- **Support System**: Integrated ticketing system for seamless customer service.
- **Transaction Alerts**: Real-time email notifications for every deposit, withdrawal, and transfer.
- **KYC Management**: Robust document submission and verification workflow.
- **Premium UI**: Crafted with React & Tailwind CSS, featuring glassmorphism, smooth animations, and skeleton loaders.

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Notifications**: Firebase Cloud Messaging (FCM)

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLAlchemy (SQLite for development)
- **AI**: Google GenAI (Gemini)
- **Email**: SMTP (Gmail Service)
- **Auth**: JWT (JSON Web Tokens)

## 🚀 Getting Started

### Backend Setup
1. Navigate to the `backend` directory.
2. Create a `.env` file with the following:
   ```env
   GMAIL_USER=your-email@gmail.com
   GMAIL_PASSWORD=your-app-password
   GOOGLE_API_KEY=your-gemini-api-key
   SECRET_KEY=your-secret-key
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `python run.py`

### Frontend Setup
1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Start the dev server: `npm start`

## 🔒 Security Features
- **Input Validation**: Strict regex checks for emails and password complexity.
- **CORS Protection**: Restricted to authorized origins.
- **Locked Accounts**: Automatic lockout after 3 failed login attempts.

---
Built with ❤️ by Payzen Team.