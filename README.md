# 🌾 AgroGen AI — Master Project Context

# Project Name

**AgroGen AI**

**Tagline:**
AI-Powered Smart Farming Assistant for Maharashtra Farmers

---

# Project Vision

AgroGen AI is a production-grade AI-powered agriculture platform designed to assist farmers in Maharashtra by combining Artificial Intelligence, Computer Vision, Retrieval-Augmented Generation (RAG), Machine Learning, Voice AI, and Modern Web Technologies into one unified application.

Unlike existing agricultural applications that solve only one problem (weather, disease detection, market prices, etc.), AgroGen AI integrates multiple intelligent services into a single AI assistant.

The application supports both Marathi and English.

The project should be designed like an industry-level SaaS product rather than a college project.

---

# Primary Users

- Farmers
- Agriculture Officers
- Government Agencies
- Researchers
- Students

---

# Main Goal

Create an AI assistant capable of helping farmers make informed agricultural decisions using AI and real-time data.

---

# Core Features

## 🌾 AI Crop Disease Detection

- Upload crop image
- Disease Detection
- Bounding Box Detection
- Confidence Score
- Disease Severity
- Treatment Recommendation
- Prevention Methods

Technology

- YOLOv8
- OpenCV
- PyTorch

---

## 🤖 AI Farming Assistant

Supports

- Marathi
- English

Can answer questions related to

- Crops
- Fertilizers
- Diseases
- Weather
- Government Schemes
- Farming Practices
- Organic Farming
- Irrigation

Technology

- Gemini 2.5 Flash
- LangChain
- LangGraph

---

## 🌦 Weather Forecast

Display

- Temperature
- Humidity
- Rainfall
- Wind Speed
- Weather Alerts

API

OpenWeatherMap

---

## 💰 Live Mandi Prices

Display

- Crop Prices
- Nearby Markets
- Historical Prices

API

- Agmarknet
- eNAM

---

## 🌱 Fertilizer Recommendation

Recommend fertilizer based on

- Crop
- Soil
- Weather
- Season

---

## 💧 Irrigation Advice

Provide irrigation schedule using

- Weather
- Soil
- Temperature

---

## 📸 Image Upload

Allow farmers to upload crop images for disease detection.

---

## 🎤 Voice Chat

Support

- Marathi
- English

Technology

- Whisper

---

## 🔊 Voice Responses

Use Text-to-Speech

Languages

- Marathi
- English

---

## 📍 Location-Based Recommendation

Recommend

- Crops
- Fertilizers
- Weather
- Market Prices

Based on GPS Location.

---

## 👨‍🌾 Farmer Dashboard

Show

- Weather
- Disease History
- Crop Recommendations
- Notifications
- Chat History
- Farm Activity

---

## 📈 Crop Yield Prediction

Predict crop yield using ML.

Models

- XGBoost
- LightGBM

---

## 📰 Government Scheme Information

Provide latest

- PM-KISAN
- Crop Insurance
- Maharashtra Schemes
- Subsidies

---

## 🌿 Organic Farming Guidance

Recommend

- Organic Fertilizers
- Organic Pesticides
- Best Practices

---

## 🚜 Equipment Suggestions

Recommend

- Tractors
- Seeders
- Pumps
- Sprayers

---

## 📝 Farm Activity History

Maintain

- Chat History
- Disease Reports
- Crop Reports
- Recommendations

---

# Technology Stack

## Frontend

- React.js
- Tailwind CSS
- React Router
- Axios

---

## Backend

- FastAPI
- Python
- SQLAlchemy
- Alembic
- Pydantic

---

## Authentication

- JWT
- Refresh Tokens
- bcrypt

---

## Database

- PostgreSQL

---

## Vector Database

- ChromaDB

---

## AI

- Gemini 2.5 Flash
- LangChain
- LangGraph

---

## Computer Vision

- YOLOv8
- OpenCV
- PyTorch

---

## ML

- XGBoost
- LightGBM
- Prophet

---

## Voice AI

- Whisper
- gTTS

---

## Deployment

Frontend

- Vercel

Backend

- AWS EC2

Database

- PostgreSQL

Server

- Nginx

Container

- Docker

---

## Monitoring

- LangSmith

---

# APIs

- Gemini API
- OpenWeatherMap API
- Agmarknet API
- eNAM API
- Maps API (Optional)

---

# Architecture

Frontend

↓

FastAPI Backend

↓

Authentication

↓

LangGraph

↓

LangChain

↓

Gemini

↓

RAG

↓

ChromaDB

↓

Agriculture Knowledge Base

↓

PostgreSQL

↓

Frontend

YOLO runs independently for image detection and sends detected disease information to Gemini for treatment recommendation.

---

# Machine Learning

## Crop Disease Detection

YOLOv8

Workflow

Image

↓

OpenCV

↓

YOLOv8

↓

Disease

↓

Gemini

↓

Treatment Recommendation

---

## Yield Prediction

Model

- XGBoost

Input

- Weather
- Soil
- Fertilizer
- Crop

Output

Expected Yield

---

## Market Price Prediction

Model

- Prophet

Output

Future Crop Prices

---

# RAG Pipeline

Documents

↓

Loader

↓

Splitter

↓

Embedding

↓

ChromaDB

↓

Retriever

↓

Prompt Template

↓

Gemini

↓

Answer

---

# LangGraph Agents

Planner Agent

↓

Disease Agent

↓

Weather Agent

↓

Market Agent

↓

Government Scheme Agent

↓

Recommendation Agent

↓

Organic Farming Agent

↓

Equipment Agent

↓

Yield Prediction Agent

↓

Memory Node

↓

Decision Node

↓

Response

---

# Development Phases

## Phase 0

Project Initialization

---

## Phase 1

Project Synopsis

---

## Phase 2

Requirement Analysis

---

## Phase 3

System Design

---

## Phase 4

Database

---

## Phase 5

Backend

---

## Phase 6

Frontend

---

## Phase 7

Crop Disease Detection

---

## Phase 8

RAG Pipeline

---

## Phase 9

LangGraph

---

## Phase 10

External APIs

---

## Phase 11

Prediction Services

- Yield Prediction
- Fertilizer Recommendation
- Irrigation Advice
- Market Price Prediction

---

## Phase 12

Voice AI

---

## Phase 13

Authentication

---

## Phase 14

Monitoring

---

## Phase 15

Docker

---

## Phase 16

Deployment

---

## Phase 17

Testing

---

## Phase 18

Documentation

---

# Development Rules

Every phase must contain:

## Objective

Explain the purpose.

---

## Theory

Explain concepts before coding.

---

## Folder Structure

Show every file.

---

## Code

Provide complete production-ready code.

---

## Explanation

Explain every line.

---

## Testing

Show how to test.

---

## Expected Output

Explain expected results.

---

## Common Errors

List common mistakes and fixes.

---

## Deliverables

List everything completed in that phase.

---

## Connection

Explain how the phase connects to the next phase.

---

# Coding Standards

- Production-ready code
- Modular architecture
- Scalable design
- Clean Code principles
- SOLID principles
- Type hints
- Proper logging
- Error handling
- API validation
- Environment variables
- Reusable components

---

# Final Goal

Develop AgroGen AI as a production-grade AI-powered agriculture platform suitable for:

- Smart India Hackathon (SIH)
- Final Year Engineering Project
- GitHub Portfolio
- Resume Showcase
- AI/ML Job Interviews
- Real-world deployment

The project should be designed and implemented as if it will be deployed for actual farmers across Maharashtra.