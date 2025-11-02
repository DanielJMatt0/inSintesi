# Project Documentation – inSintesi

## 1. Introduction

At **Endress+Hauser**, decision-making relies on collaboration among thousands of experts worldwide. Aligning these diverse perspectives is key to achieving smarter, faster, and more inclusive outcomes.  

**inSintesi** addresses this challenge by providing an AI-powered platform that collects, analyzes, and synthesizes opinions from teams — enabling organizations to find common ground efficiently and transparently.

The tool transforms diverse viewpoints into meaningful consensus using artificial intelligence, supporting decision-making processes that truly reflect collective intelligence.

---

## 2. Concept & Objectives

The goal of **inSintesi** is to **capture the wisdom of the crowd** through structured input and AI-driven synthesis.  
It allows team leads to create discussions on any topic — from product decisions to sustainability strategies — and collects feedback from participants through a simple and accessible interface.

Key objectives:
- **Gather opinions** from multiple users across teams.
- **Analyze and categorize** input automatically using AI.
- **Visualize consensus** and insights in an intuitive dashboard.
- **Empower decision-makers** with evidence-based, inclusive summaries.

---

## 3. System Architecture

**inSintesi** is built as a web application combining modern web technologies with an AI-powered backend.

**Architecture overview:**
- **Frontend:** Built with **Vite** and **Vue.js** for a responsive, fast, and modular interface.
- **Backend:** Implemented with **FastAPI** in **Python** for efficient request handling and API management.
- **AI Layer:** Uses the **Mistral AI API** (`mistral-medium-latest`, version 2508, November 2025) for natural language analysis.
- **Database / User Management:** Supports user authentication via email tokens and role-based access for team leads.
- **Visualization:** Dynamic dashboards displaying results tailored to question type and analysis mode.

**Tech stack summary:**
- **Languages:** Python, TypeScript  
- **Frameworks:** FastAPI, Vue.js, Vite  
- **AI API:** Mistral AI (`mistral-medium-latest`)  
- **Hosting:** **Resend** (email handling), **Render** (deployment), **Neon** (database)

---

## 4. Implementation

### 4.1 Core Features
- **Team Management:**  
  Team leads can log in and manage their teams via email-based invitations. Each participant receives an individual token, ensuring controlled access.
  
- **Question Types:**  
  The system automatically detects the nature of the question and applies the corresponding AI analysis mode. Supported categories include:
  - `stance_analysis`
  - `option_comparison`
  - `idea_generation`
  - `priority_ranking`
  - `feedback_analysis`

- **AI-Powered Analysis:**  
  Using prompt-engineered templates, the backend sends participant responses to Mistral AI. The model interprets the data and synthesizes themes, patterns, or rankings depending on the question type.

- **Dashboard Visualization:**  
  Results are displayed in an interactive dashboard. Each question type is visualized differently to best represent the insights (e.g., sentiment distribution, ranked priorities, summarized options).

### 4.2 Data Flow
1. **Question creation** by a team lead.  
2. **Question type classification** by the AI model.  
3. **Participants submit answers** via individual or universal token links.  
4. **AI analysis** processes responses using the appropriate prompt template.  
5. **Results visualization** on the team dashboard, tailored to the analysis mode.

---

## 5. User Journey

1. **Team Lead Login:**  
   The lead logs into the web platform and creates a new discussion question.

2. **Participant Invitation:**  
   The system generates individual or universal tokens, automatically distributed by email.

3. **Opinion Submission:**  
   Participants answer directly from the web interface.

4. **AI Consensus Generation:**  
   Once responses are collected, the system triggers Mistral-based analysis pipelines.

5. **Dashboard Overview:**  
   The team lead can view aggregated insights — showing agreement zones, conflicting views, and summarized perspectives.

---

## 6. Results & Evaluation

During the hackathon, the full pipeline was successfully implemented and demonstrated.  
All major components — authentication, AI analysis, and data visualization — functioned as intended.  

The team encountered minor challenges with frontend integration during the final phase, mainly related to data binding and layout synchronization, but these were resolved enough to ensure a complete demo.

The resulting system effectively showed:
- Automatic adaptation to question type.
- Accurate and interpretable AI summaries.
- Smooth user experience for both leads and participants.

---

## 7. Future Work & Improvements

While the MVP performed well, several enhancements are planned for future iterations:
- **Enhanced prompt engineering:** More sophisticated analysis pipelines and fine-tuned models for improved contextual understanding.  
- **Registration and onboarding:** Dedicated registration flow for new users and teams.  
- **Advanced analytics:** Clustering visualization, and exportable reports.  
- **Integration options:** Slack, Teams, or other communication tools for easier access.

---

