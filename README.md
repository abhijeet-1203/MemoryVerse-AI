# 🚀 MemoryVerse AI

> **An AI-Powered Digital Identity System that understands your journey, not just your files.**

MemoryVerse AI is an intelligent knowledge repository that automatically organizes, connects, and retrieves a student's academic and professional documents. Instead of manually managing folders, users can upload documents once and instantly access them using natural language.

Built for the **Wooble AI Hackathon**, MemoryVerse AI transforms scattered certificates, resumes, internship letters, project reports, achievements, and portfolios into a structured digital identity.

---

# 📖 Overview

Every student builds a digital footprint throughout their academic journey. Certificates, resumes, internship letters, project reports, achievements, and learning records accumulate over time across multiple folders, cloud drives, and devices.

Traditional storage platforms can save files, but they cannot understand the relationships between them.

MemoryVerse AI solves this problem by using AI to:

* Extract meaningful information from uploaded documents.
* Automatically categorize content.
* Build relationships between skills, certifications, projects, internships, and achievements.
* Generate a chronological journey timeline.
* Enable semantic search using natural language.
* Preserve original documents while making them instantly accessible.

---

# ✨ Features

## 📂 AI Document Ingestion

Users can upload:

* Certificates
* Resumes
* Project Reports
* Internship Letters
* Academic Documents
* Portfolio Links
* GitHub Links
* Images
* PDFs
* DOCX Files
* PPT/PPTX Files

The ingestion workflow automatically extracts document content and metadata for further processing.

---

## 🧠 Intelligent Information Extraction

MemoryVerse AI analyzes uploaded documents to identify:

* Skills
* Projects
* Certifications
* Internships
* Education
* Organizations
* Achievements
* Dates
* Technologies
* Roles

This extracted information becomes part of the user's digital identity.

---

## 📚 Automatic Categorization

Documents are automatically classified into structured categories such as:

* Certifications
* Projects
* Skills
* Internships
* Achievements
* Academics
* Organizations
* Education

No manual sorting is required.

---

## 🔗 Relationship Engine

The platform connects extracted entities to build a meaningful knowledge graph.

Examples:

* Certification → Skill
* Skill → Project
* Project → Internship
* Internship → Organization
* Organization → Career Journey

These relationships help users understand how their experiences are connected over time.

---

## 📅 Digital Journey Timeline

MemoryVerse AI automatically generates a timeline of the user's academic and professional growth.

Example:

```
2023
├── Python Certification

2024
├── Full Stack Development Project
├── Data Structures Course

2025
├── AI Internship
├── Machine Learning Certification

2026
├── MemoryVerse AI
```

The timeline updates automatically whenever new documents are uploaded.

---

## 🔍 Smart Semantic Search

Instead of searching through folders, users can simply ask:

* Show all my certificates
* Show AI projects
* Show internship documents
* Show my latest resume
* Find projects using Python
* Show my achievements
* What certifications do I have?

The system retrieves the most relevant information along with the original uploaded documents.

---

# 🏗 System Architecture

```
                     Upload Document
                            │
                            ▼
                  Document Parser
                            │
                            ▼
                Information Extraction
                            │
                            ▼
               Entity Identification
                            │
                            ▼
             Categorization & Storage
                            │
                            ▼
              Relationship Generation
                            │
                            ▼
                 Timeline Generation
                            │
                            ▼
             Semantic Search & Retrieval
```

---

# ⚙ Workflow

MemoryVerse AI follows an automated ingestion pipeline.

```
Upload
   │
   ▼
Parse Document
   │
   ▼
Extract Metadata
   │
   ▼
Store Structured Information
   │
   ▼
Generate Relationships
   │
   ▼
Regenerate Timeline
   │
   ▼
Ready for Semantic Search
```

---

# 📂 Project Structure

```
MemoryVerse AI

├── agents/
│   ├── memory_chat_agent
│   ├── memory_extractor
│   └── connector-quiet-check
│
├── apps/
│   ├── memoryverse_app
│   └── job-connectors
│
├── workflows/
│   └── ingest_document
│
├── functions/
│   ├── upload_document
│   ├── parse_document
│   ├── persist_extraction
│   ├── regenerate_timeline
│   ├── auth_login
│   ├── auth_logout
│   ├── auth_get_session
│   └── auth_setup_profile
│
├── tables/
│   ├── profiles
│   ├── documents
│   ├── skills
│   ├── projects
│   ├── certifications
│   ├── internships
│   ├── education
│   ├── achievements
│   ├── organizations
│   ├── relationships
│   ├── timeline_events
│   ├── embeddings
│   ├── conversations
│   ├── conversation_messages
│   ├── sessions
│   └── audit_logs
│
└── README.md
```

---

# 🗄 Database Design

The project maintains structured data using dedicated tables:

| Table                 | Purpose                          |
| --------------------- | -------------------------------- |
| profiles              | User profile information         |
| documents             | Uploaded document metadata       |
| skills                | Extracted skills                 |
| projects              | User projects                    |
| certifications        | Certificates and credentials     |
| internships           | Internship records               |
| education             | Academic history                 |
| achievements          | Awards and accomplishments       |
| organizations         | Companies and institutions       |
| relationships         | Links between extracted entities |
| timeline_events       | Career timeline                  |
| embeddings            | Semantic embeddings              |
| conversations         | Chat sessions                    |
| conversation_messages | User conversations               |
| sessions              | Authentication sessions          |
| audit_logs            | System activity logs             |

---

# 🤖 AI Components

MemoryVerse AI integrates multiple AI capabilities:

* Intelligent document parsing
* Information extraction
* Entity recognition
* Relationship generation
* Timeline creation
* Semantic retrieval
* Conversational memory assistant

---

# 🚀 Core Functions

### upload_document

Handles user uploads including PDFs, DOCX, PPTX, images, and URLs.

### parse_document

Extracts textual content and metadata from uploaded documents.

### persist_extraction

Stores extracted entities into structured database tables.

### regenerate_timeline

Automatically rebuilds the user's career and academic timeline whenever new information is added.

### memory_chat_agent

Provides conversational access to the user's digital identity.

### memory_extractor

Processes uploaded content and identifies structured information.

---

# 💡 Example Queries

Users can ask:

```
Show all my certificates

Show internship letters

Find projects related to AI

Show my latest resume

Which certifications teach Python?

What skills have I learned?

Show my academic achievements

List all organizations I have worked with
```

---

# 🎯 Hackathon Requirements Covered

| Requirement                     | Status |
| ------------------------------- | ------ |
| AI Data Ingestion               | ✅      |
| Intelligent Categorization      | ✅      |
| Relationship Engine             | ✅      |
| Digital Journey Timeline        | ✅      |
| Smart Retrieval                 | ✅      |
| Original File Preservation      | ✅      |
| AI-powered Knowledge Repository | ✅      |

---

# 🔮 Future Enhancements

* OCR support for handwritten documents
* LinkedIn synchronization
* GitHub repository analysis
* Resume generation
* Career recommendation engine
* Skill-gap analysis
* Mobile application
* Voice-enabled search
* AI career mentor

---

# ❤️ Why MemoryVerse AI?

MemoryVerse AI goes beyond document storage. It creates a living digital identity that understands a student's achievements, skills, projects, and experiences. By connecting fragmented information into a searchable knowledge graph, it empowers users to rediscover their journey instantly without ever searching through folders again.

---


> **"From scattered files to an intelligent digital identity."**
