# 🚀 MemoryVerse AI

> **"I never have to search through folders again."**

MemoryVerse AI is an AI-powered Digital Identity System that transforms scattered academic and professional documents into a structured, searchable, and intelligent knowledge repository.

Unlike traditional cloud storage, MemoryVerse AI understands your journey by automatically organizing files, extracting meaningful information, building relationships between achievements, and enabling natural language search.

---

# 📌 Problem Statement

Students accumulate hundreds of documents throughout their academic journey:

- 📜 Certificates
- 📄 Resumes
- 💼 Internship Letters
- 📚 Project Reports
- 🏆 Achievements
- 💻 GitHub Repositories
- 🌐 Portfolio Links
- 🎓 Academic Documents

These files are often scattered across:

- Google Drive
- Email Attachments
- Downloads Folder
- Cloud Storage
- Different Devices

Traditional storage platforms can save files but cannot understand a person's journey.

MemoryVerse AI solves this by creating an intelligent digital identity that understands, connects, and retrieves information instantly.

---

# 🎯 Features

## 📂 AI Data Ingestion

Upload various document types including:

- PDF
- DOCX
- Images
- Certificates
- Resume
- Internship Letters
- Project Reports
- Portfolio Links

The AI automatically extracts:

- Text
- Skills
- Organizations
- Dates
- Technologies
- Roles
- Achievements

---

## 🧠 Intelligent Categorization

Automatically classifies uploaded documents into categories such as:

- Projects
- Certifications
- Skills
- Internships
- Achievements
- Academics
- Resume
- Portfolio

No manual sorting required.

---

## 🔗 Relationship Engine

MemoryVerse AI builds meaningful relationships between extracted information.

Example:

```
Certification
      ↓
Skill
      ↓
Project
      ↓
Internship
      ↓
Career Growth
```

Relationships include:

- Certification → Skill
- Skill → Project
- Project → Internship
- Internship → Career Path

---

## 📈 Digital Journey Timeline

Automatically creates a visual timeline of academic and professional growth.

Example:

```
2023
│
├── Python Certification
│
2024
│
├── Web Development Project
├── Coding Club Member
│
2025
│
├── AI Internship
├── Machine Learning Certification
│
2026
│
├── MemoryVerse AI
```

---

## 🔍 Smart Retrieval System

Search naturally without remembering filenames.

Examples:

```
Show my certificates

Show AI projects

Show internship documents

Show my latest resume

Find projects using Python

Show Machine Learning achievements
```

The AI understands intent and retrieves the original document instantly.

---

# 🤖 AI Workflow

```
User Uploads Document
          │
          ▼
 OCR / Text Extraction
          │
          ▼
 NLP Entity Recognition
          │
          ▼
 Metadata Extraction
          │
          ▼
 Intelligent Categorization
          │
          ▼
 Embedding Generation
          │
          ▼
 Vector Database Storage
          │
          ▼
 Relationship Engine
          │
          ▼
 Semantic Search + RAG
          │
          ▼
 Natural Language Response
```

---

# 🏗️ System Architecture

```
                    User
                      │
                      ▼
              Upload Documents
                      │
      ┌───────────────┴───────────────┐
      │                               │
      ▼                               ▼
 OCR/Text Extraction          Metadata Extraction
      │                               │
      └───────────────┬───────────────┘
                      ▼
            NLP Entity Recognition
                      │
                      ▼
         Automatic Categorization
                      │
                      ▼
          Embedding Generation
                      │
                      ▼
             Vector Database
                      │
                      ▼
            Relationship Engine
                      │
                      ▼
          Semantic Search (RAG)
                      │
                      ▼
        Original Document Retrieval
```

---

# 🛠️ Tech Stack

## Frontend

- React.js
- Tailwind CSS
- Vite

## Backend

- Node.js
- Express.js

## AI & ML

- LangChain
- OpenAI / Gemini API
- Hugging Face
- Sentence Transformers
- OCR (Tesseract / Google Vision)

## Database

- MongoDB

## Vector Database

- FAISS
- Pinecone
- ChromaDB

---

# 🧠 AI Components

## NLP (Natural Language Processing)

Extracts:

- Skills
- Organizations
- Dates
- Technologies
- Education
- Certifications
- Roles

---

## Embeddings

Every uploaded document is converted into vector embeddings.

Benefits:

- Semantic Search
- Similarity Matching
- Context Retrieval

---

## Retrieval-Augmented Generation (RAG)

Instead of generating answers from memory, MemoryVerse AI retrieves relevant documents first and then generates responses grounded in those documents.

Benefits:

- Personalized responses
- Higher accuracy
- Reduced hallucinations

---

## Semantic Search

Supports natural language queries such as:

```
Show my AI certificates

Find React projects

Show internship documents

Latest resume

Python achievements

Machine Learning projects
```

---

# 📁 Project Structure

```
MemoryVerse-AI/

├── frontend/
├── backend/
├── uploads/
├── models/
├── routes/
├── services/
├── database/
├── vector_store/
├── ai/
├── public/
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/MemoryVerse-AI.git
```

Move into the project

```bash
cd MemoryVerse-AI
```

Install frontend dependencies

```bash
npm install
```

Install backend dependencies

```bash
cd backend
npm install
```

Start backend

```bash
npm run dev
```

Start frontend

```bash
npm run dev
```

---

# 🚀 Usage

1. Upload your academic or professional documents.
2. AI extracts metadata and important information.
3. Documents are automatically categorized.
4. Relationships between skills, projects, certifications, and internships are created.
5. Ask questions in natural language.
6. Retrieve original documents instantly.

---

# 💬 Example Queries

```
Show all my certificates

Show my AI projects

Show internship letters

Show my latest resume

Find projects using Python

What skills do I have?

Show achievements from 2025

Find Machine Learning certifications
```

---

# 🌟 Future Scope

- 🎙️ Voice-based Search
- 📄 AI Resume Generator
- 💼 Job Recommendation System
- 🔗 LinkedIn Integration
- 💻 GitHub Sync
- 📊 Skill Gap Analysis
- 🎯 Career Roadmap Generator
- 📱 Mobile Application
- 🤖 AI Career Assistant

---

# 🎯 Why MemoryVerse AI?

Unlike traditional cloud storage, MemoryVerse AI:

✅ Understands documents instead of just storing them.

✅ Automatically organizes information.

✅ Builds meaningful relationships between experiences.

✅ Enables semantic search using AI.

✅ Preserves original documents while making them instantly accessible.

✅ Represents a student's complete academic and professional journey.

---

# 📊 Hackathon Evaluation Mapping

| Requirement | Our Solution |
|------------|-------------|
| AI Data Ingestion | OCR + NLP based extraction from uploaded documents |
| Intelligent Categorization | Automatic document classification |
| Relationship Engine | AI-powered knowledge graph connecting skills, projects, certifications, internships |
| Digital Journey Timeline | Chronological visualization of growth |
| Smart Retrieval | Semantic Search + RAG |
| NLP | Entity Extraction |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS / ChromaDB / Pinecone |
| Semantic Search | Natural Language Query Processing |

---

# 👨‍💻 Team

Built with ❤️

**MemoryVerse AI** is more than a document storage platform—it's an intelligent digital identity that understands, organizes, and showcases a student's complete academic and professional journey.

> **"From scattered files to a connected digital identity."**
