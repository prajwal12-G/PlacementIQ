# Product Requirements Document (PRD)

# PlacementIQ

Version: 1.0

Project Type: Final Year Engineering Project

Status: Active Development

Last Updated: July 2026

---

# 1. Executive Summary

PlacementIQ is an AI-powered Placement Readiness Platform designed to help engineering students evaluate, improve, and track their placement preparation.

Unlike traditional platforms that focus only on coding practice or job listings, PlacementIQ provides a complete placement readiness ecosystem by analyzing resumes, comparing them with job descriptions, conducting AI-powered mock interviews, identifying skill gaps, and generating a personalized Placement Readiness Index (PRI).

The platform acts as an intelligent career mentor that continuously guides students toward becoming placement-ready.

---

# 2. Problem Statement

Engineering students often struggle to understand whether they are ready for campus placements.

Current platforms solve only isolated problems.

Examples include:

- Coding practice platforms
- Resume builders
- Job portals
- Interview preparation websites

None provide an end-to-end evaluation of placement readiness.

Students often face questions such as:

- Is my resume ATS-friendly?
- Which skills am I missing?
- How well does my resume match a job description?
- Am I prepared for technical interviews?
- What should I improve next?

PlacementIQ aims to answer these questions through intelligent analysis and personalized guidance.

---

# 3. Vision

To build an AI-powered placement mentor that helps students continuously improve their employability by providing data-driven insights, personalized recommendations, and measurable progress tracking.

---

# 4. Objectives

Primary objectives include:

- Improve student placement readiness
- Automate resume analysis
- Identify missing skills
- Provide AI-based interview practice
- Track progress over time
- Deliver personalized learning recommendations

---

# 5. Target Users

Primary Users

- Engineering Students
- Final Year Students
- Fresh Graduates

Secondary Users

- Placement Coordinators
- College Faculty
- Career Counselors

Future Users

- Recruiters
- HR Teams
- Training Institutes

---

# 6. User Personas

## Student

Goals

- Build a better resume
- Prepare for placements
- Improve interview skills
- Track improvement

Pain Points

- Doesn't know what to improve
- Doesn't know required skills
- Low interview confidence

---

## Placement Officer

Goals

- Monitor student readiness
- Identify weak areas
- Improve placement statistics

---

# 7. Scope

## In Scope

- User Authentication
- Resume Upload
- Resume Parsing
- ATS Score
- Resume Suggestions
- JD Matching
- Skill Gap Analysis
- AI Career Coach
- AI Mock Interview
- Placement Readiness Index
- Dashboard
- Progress Tracking

---

## Out of Scope (Current Version)

- Company Recruitment Portal
- Live Interview Platform
- Resume Sharing Marketplace
- Video Conferencing
- Mobile Application

---

# 8. Functional Requirements

## Authentication Module

Features

- User Registration
- Login
- JWT Authentication
- Protected APIs
- Password Hashing
- User Profile

Status

In Progress

---

## Resume Intelligence

Features

- Resume Upload
- Resume Storage
- Resume Parsing
- ATS Analysis
- Resume Score
- Improvement Suggestions

Status

Planned

---

## Job Description Matching

Features

- JD Upload
- Resume Matching
- Missing Skills Detection
- Match Percentage

Status

Planned

---

## AI Career Coach

Features

- Personalized Advice
- Learning Roadmap
- Career Suggestions
- Skill Recommendations

Status

Planned

---

## Interview Intelligence

Features

- AI Mock Interview
- Technical Questions
- HR Questions
- Feedback
- Communication Analysis

Status

Planned

---

## Placement Readiness Index (PRI)

Features

Generate a placement readiness score using

- Resume Quality
- ATS Score
- Skill Coverage
- Projects
- Certifications
- Interview Performance

Status

Planned

---

# 9. Non-Functional Requirements

Performance

- Fast API responses
- Optimized database queries

Scalability

- Modular architecture
- Easy feature expansion

Security

- JWT Authentication
- Password Hashing
- Environment Variables
- Protected Routes

Maintainability

- Clean Architecture
- Repository Pattern
- Modular Services

Reliability

- Database Transactions
- Input Validation
- Error Handling

---

# 10. Technology Stack

Frontend

- React
- TypeScript
- Tailwind CSS
- Vite

Backend

- FastAPI
- SQLAlchemy

Database

- MySQL

Authentication

- JWT
- bcrypt
- Passlib

AI

Future

- Ollama
- Qwen
- LangChain (optional)

Version Control

- Git
- GitHub

---

# 11. System Architecture

```
React Frontend

↓

FastAPI

↓

API Layer

↓

Service Layer

↓

Repository Layer

↓

SQLAlchemy ORM

↓

MySQL
```

---

# 12. Database

Current Tables

Users

Future Tables

- resumes
- resume_scores
- job_descriptions
- skill_analysis
- interviews
- interview_feedback
- pri_scores
- notifications
- learning_paths

---

# 13. User Journey

Student Registration

↓

Login

↓

Dashboard

↓

Upload Resume

↓

Resume Analysis

↓

ATS Score

↓

Upload Job Description

↓

Skill Gap Analysis

↓

Learning Recommendations

↓

Mock Interview

↓

Placement Readiness Index

↓

Continuous Improvement

---

# 14. Sprint Roadmap

## Sprint 1

Project Planning

Status

Completed

---

## Sprint 2

Backend Foundation

Status

Completed

Deliverables

- Project Structure
- Database
- Models
- Authentication Foundation

---

## Sprint 3

Authentication

Deliverables

- Register
- Login
- JWT
- Protected Routes

Status

In Progress

---

## Sprint 4

Resume Upload

---

## Sprint 5

Resume Parser

---

## Sprint 6

ATS Engine

---

## Sprint 7

JD Matching

---

## Sprint 8

AI Career Coach

---

## Sprint 9

Interview Intelligence

---

## Sprint 10

Placement Dashboard

---

## Sprint 11

Testing

---

## Sprint 12

Deployment

---

# 15. Success Metrics

Technical

- API response time < 300 ms
- Secure authentication
- Stable database

Product

- Resume successfully analyzed
- Accurate ATS scoring
- Correct skill gap identification
- Meaningful AI recommendations

User

- Improved placement readiness
- Better interview confidence
- Resume improvement over time

---

# 16. Risks

Technical Risks

- Resume parsing accuracy
- AI hallucinations
- OCR quality
- PDF formatting differences

Project Risks

- Time limitations
- AI model resource usage
- Deployment complexity

Mitigation

- Modular architecture
- Incremental development
- Continuous testing

---

# 17. Future Enhancements

- Company Recommendation Engine
- Internship Recommendation
- LinkedIn Profile Analysis
- GitHub Analysis
- Coding Profile Integration
- AI Resume Builder
- AI Cover Letter Generator
- HR Analytics Dashboard
- Recruiter Portal
- Mobile Application

---

# 18. Acceptance Criteria

The project will be considered successful when a student can:

✓ Register and login securely

✓ Upload a resume

✓ Receive ATS score

✓ Compare resume with a Job Description

✓ View missing skills

✓ Receive AI-generated suggestions

✓ Practice mock interviews

✓ Track Placement Readiness Index

✓ Monitor improvement over time

---

# 19. Project Outcome

PlacementIQ should function as an intelligent placement mentor that helps engineering students prepare for campus placements through continuous analysis, personalized recommendations, AI-assisted learning, and measurable progress tracking.