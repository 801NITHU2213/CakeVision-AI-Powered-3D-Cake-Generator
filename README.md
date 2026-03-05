# CakeVision – AI Powered 3D Cake Generator 🎂

CakeVision is a generative AI application that converts natural language cake descriptions into realistic cake textures and renders them on a 3D cake model in real time.

The system integrates Stable Diffusion XL for image generation and Babylon.js for 3D visualization, enabling users to design and visualize custom cakes interactively.

## Features

• AI-based cake texture generation using Stable Diffusion XL  
• Natural language cake description input  
• Automatic prompt optimization for seamless texture generation  
• Real-time 3D cake rendering using Babylon.js  
• REST API backend built with Flask  
• Dynamic texture mapping on 3D models

## System Architecture

User Prompt (Frontend UI)
        ↓
Flask REST API (/generate)
        ↓
Prompt Optimization + Side Texture Hint
        ↓
Stable Diffusion XL API
        ↓
Base64 Image Response
        ↓
Decode + Store Generated Texture
        ↓
Babylon.js 3D Viewer
        ↓
Textured Cake Model Rendering

## Tech Stack

Backend
• Python
• Flask
• PyTorch
• MiDaS

Frontend
• HTML
• JavaScript
• Babylon.js

AI
• Stable Diffusion XL

## Installation

1. Clone the repository

git clone https://github.com/801NITHU2213/CakeVision-AI-Powered-3D-Cake-Generator

2. Install dependencies

pip install -r requirements.txt

3. Add your Stability API key

Create a .env file:

STABILITY_API_KEY=your_api_key

4. Run the backend

python app.py

5. Open index.html in a browser
