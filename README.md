# Sukoon AI - Enterprise Trust & Safety Infrastructure

Sukoon AI is an API-first platform that automatically intercepts, verifies, and neutralizes viral misinformation, deepfakes, and hate speech. We provide the "Stripe for Misinformation"—equipping social platforms (Meta, X, WhatsApp) and massive Newsrooms with a localized, legally defensible RAG verification engine.

## 🚀 The Moat
Unlike generic LLMs that hallucinate, Sukoon AI is anchored by a specialized RAG (Retrieval-Augmented Generation) pipeline directly indexing authoritative Indian fact-checkers:
- **PIB Fact Check** (Government policy & economic claims)
- **Alt News** (Communal & geopolitical misinformation)
- **BOOM Live** (Deepfakes and multimedia forensics)

To minimize AI hallucinations and handle viral fake news efficiently, Sukoon AI implements an internal knowledge ring using a hosted Qdrant Vector database on Google Cloud. Instead of blindly sending every request to a massive LLM, our backend performs a semantic vector search against locally verified facts first. If a piece of misinformation has already been debunked by community admins, Sukoon AI retrieves it instantly in milliseconds, saving massive operational token costs and preventing the system from generating contradictory advice.

## 🏗 Architecture

Sukoon AI handles immense scale using an asynchronous fan-out/fan-in processing pipeline.

```text
                    ┌─────────────────────────┐
                    │      USER INPUTS        │
                    │                         │
                    │ WhatsApp Forward        │
                    │ Instagram Reel Link     │
                    │ X Tweet Mention         │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌─────────────────────────┐
                    │   FASTAPI API GATEWAY   │
                    └──────────┬──────────────┘
                               │
       ┌───────────────────────┼─────────────────────────┐
       ▼                       ▼                         ▼
┌─────────────────┐  ┌─────────────────┐   ┌─────────────────┐
│ TEXT ANALYZER   │  │ AUDIO ANALYZER  │   │ IMAGE/VIDEO AI  │
└────────┬────────┘  └────────┬────────┘   └────────┬────────┘
         │                    │                     │
         └───────────┬────────┴─────────────┬───────┘
                     ▼                     
           ┌─────────────────────────┐
           │ CLAIM EXTRACTION AGENT  │
           └──────────┬──────────────┘
                      │
                      ▼
           ┌─────────────────────────┐
           │   RAG VERIFICATION HUB  │
           │ (PIB, AltNews, BoomLive)│
           └──────────┬──────────────┘
                      │
                      ▼
          ┌──────────────────────────┐
          │ TRUTH CARD GENERATOR     │
          │ (Green, Yellow, Red)     │
          └──────────┬───────────────┘
                     │
                     ▼
       ┌─────────────────────────────┐
       │ PLATFORM RESPONSE LAYER     │
       │ (Webhooks, API JSON return) │
       └─────────────────────────────┘
```

## 💻 Tech Stack
- **Frontend**: Next.js 15 (App Router), React, Tailwind CSS, ShadCN, Framer Motion
- **Backend API**: FastAPI, WebSockets
- **Async Processing**: Celery, Redis
- **Database / Cache**: PostgreSQL, Qdrant (Vector DB for RAG edge caching)

## 🎨 Design Philosophy: "Clinical & Calm"
Sukoon AI deals with high-anxiety viral content. To instantly de-escalate emotional states, the UI entirely avoids bright "startup" colors. 
- **Colors**: Muted earth tones (`stone-50`), deep navy (`slate-900`), and clinical `teal-700`.
- **Typography**: Tracked-out uppercase micro-copy to establish a forensic, structured layout.
- **Components**: Pillowy cards, extremely soft ambient shadows, and slow-pulsing animations.

## 🛠 Running the MVP Locally

### 1. Start the FastAPI Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Start the Next.js Frontend
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000` to view the Developer API Landing Page, or navigate to `http://localhost:3000/dashboard` to access the Analyst Command Center.
