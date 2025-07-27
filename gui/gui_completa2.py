import streamlit as st
import json
import sys
from pathlib import Path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))
from typing import Dict, List, Any
import time
import random
import os
from dotenv import load_dotenv
from file_generation.lore_generation import generate_lore
from langchain_google_genai import ChatGoogleGenerativeAI
from file_generation.domain_generation import create_domain_pddl
from file_generation.problem_generation import create_problem_pddl
from correction_and_validation.reflective_agent import run_correction_workflow, run_user_correction_pddl, update_lore_with_corrections
from correction_and_validation.pddl_validation import run_fastdownward_complete, validate_plan_with_val, get_validation_error_for_correction
from utils import print_lore, print_plan, load_example_json
from file_generation.story_generation import generate_story
import base64
import re
from io import BytesIO
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Configurazione della pagina
st.set_page_config(
    page_title="Creatore di Avventure Interattive",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Creepster&display=swap');
    
    .stApp {
        background: radial-gradient(ellipse at center, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    /* Effetto stelle animate di sfondo migliorato */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(3px 3px at 25px 35px, #ffd700, transparent),
            radial-gradient(2px 2px at 60px 80px, rgba(255,255,255,0.9), transparent),
            radial-gradient(1px 1px at 100px 50px, #87ceeb, transparent),
            radial-gradient(2px 2px at 150px 90px, rgba(255,215,0,0.8), transparent),
            radial-gradient(1px 1px at 180px 40px, #ff69b4, transparent),
            radial-gradient(2px 2px at 220px 70px, #98fb98, transparent);
        background-repeat: repeat;
        background-size: 250px 120px;
        animation: sparkle 25s linear infinite;
        pointer-events: none;
        z-index: -1;
        opacity: 0.7;
    }
    
    @keyframes sparkle {
        from { transform: translateY(0px) rotate(0deg); }
        to { transform: translateY(-120px) rotate(360deg); }
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #ffd700, #ffed4e, #ff6b6b, #4ecdc4, #a29bfe, #ffd700);
        background-size: 600% 600%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Cinzel', serif;
        font-size: 4rem;
        font-weight: 700;
        margin: 2rem 0 3rem 0;
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.8);
        animation: glow 3s ease-in-out infinite alternate, gradientShift 8s ease-in-out infinite;
        letter-spacing: 6px;
        position: relative;
        padding: 1rem 0;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent 20%, rgba(255,255,255,0.6) 50%, transparent 80%);
        animation: shine 4s infinite;
        pointer-events: none;
    }
    
    @keyframes glow {
        from { 
            text-shadow: 0 0 30px rgba(255, 215, 0, 0.6), 0 0 40px rgba(255, 215, 0, 0.4), 0 0 50px rgba(255, 215, 0, 0.2); 
        }
        to { 
            text-shadow: 0 0 40px rgba(255, 215, 0, 1), 0 0 60px rgba(255, 215, 0, 0.8), 0 0 80px rgba(255, 215, 0, 0.6); 
        }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) skewX(-15deg); }
        100% { transform: translateX(200%) skewX(-15deg); }
    }
    
            
    /* EFFETTI VITTORIA */
    @keyframes victoryPulse {
        0%, 100% { 
            transform: scale(1); 
            box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
        }
        50% { 
            transform: scale(1.05); 
            box-shadow: 0 0 60px rgba(255, 215, 0, 1), 0 0 100px rgba(255, 215, 0, 0.8);
        }
    }

    @keyframes confetti {
        0% { 
            transform: translateY(-100vh) rotate(0deg); 
            opacity: 1; 
        }
        100% { 
            transform: translateY(100vh) rotate(720deg); 
            opacity: 0; 
        }
    }

    @keyframes victoryGlow {
        0%, 100% { 
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
            color: #ffd700;
        }
        25% { 
            text-shadow: 0 0 40px rgba(255, 65, 108, 1);
            color: #ff416c;
        }
        50% { 
            text-shadow: 0 0 40px rgba(116, 185, 255, 1);
            color: #74b9ff;
        }
        75% { 
            text-shadow: 0 0 40px rgba(0, 184, 148, 1);
            color: #00b894;
        }
    }

    .victory-container {
        animation: victoryPulse 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }

    .victory-container::before {
        content: '🎉✨🏆⭐🎊🌟💫🎁';
        position: absolute;
        top: -50px;
        left: 0;
        width: 100%;
        font-size: 2rem;
        animation: confetti 3s linear infinite;
        pointer-events: none;
        z-index: 10;
    }

    .victory-title {
        animation: victoryGlow 3s ease-in-out infinite;
        font-family: 'Cinzel', serif;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        text-transform: uppercase;
        letter-spacing: 3px;
    }

    /* Fireworks effect */
    .fireworks {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
    }

    .firework {
        position: absolute;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        animation: fireworkExplode 2s ease-out infinite;
    }

    @keyframes fireworkExplode {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        50% {
            transform: scale(1);
            opacity: 0.8;
        }
        100% {
            transform: scale(2);
            opacity: 0;
        }
    }
            
    /* CONTENITORI PRINCIPALI RIDISEGNATI */
    
    .creation-container {
        background: linear-gradient(135deg, rgba(16, 42, 84, 0.95) 0%, rgba(8, 28, 58, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 3px solid transparent;
        border-radius: 30px;
        padding: 3.5rem 3rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 
            0 0 80px rgba(74, 144, 226, 0.4),
            inset 0 0 80px rgba(255, 255, 255, 0.08),
            0 25px 50px rgba(0,0,0,0.6);
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(1deg);
        transition: all 0.4s ease;
    }
    
    .creation-container:hover {
        transform: perspective(1000px) rotateX(0deg) scale(1.005);
        box-shadow: 
            0 0 100px rgba(74, 144, 226, 0.5),
            inset 0 0 100px rgba(255, 255, 255, 0.1),
            0 35px 70px rgba(0,0,0,0.7);
    }
    
    .creation-container::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, #4a90e2, #74b9ff, #00cec9, #a29bfe, #4a90e2);
        background-size: 400% 400%;
        border-radius: 30px;
        z-index: -1;
        animation: borderGlow 6s ease-in-out infinite;
        opacity: 0.8;
    }
    
    .validation-container {
        background: linear-gradient(135deg, rgba(68, 48, 10, 0.95) 0%, rgba(45, 32, 8, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 3px solid transparent;
        border-radius: 30px;
        padding: 3.5rem 3rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 
            0 0 80px rgba(255, 165, 0, 0.4),
            inset 0 0 80px rgba(255, 255, 255, 0.08),
            0 25px 50px rgba(0,0,0,0.6);
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(1deg);
        transition: all 0.4s ease;
    }
    
    .validation-container:hover {
        transform: perspective(1000px) rotateX(0deg) scale(1.005);
        box-shadow: 
            0 0 100px rgba(255, 165, 0, 0.5),
            inset 0 0 100px rgba(255, 255, 255, 0.1),
            0 35px 70px rgba(0,0,0,0.7);
    }
    
    .validation-container::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, #ffa500, #ff7675, #fd79a8, #fdcb6e, #ffa500);
        background-size: 400% 400%;
        border-radius: 30px;
        z-index: -1;
        animation: borderGlow 6s ease-in-out infinite;
        opacity: 0.8;
    }
    
    .story-container {
        background: linear-gradient(135deg, rgba(32, 8, 68, 0.95) 0%, rgba(20, 5, 45, 0.95) 100%);
        backdrop-filter: blur(20px);
        border: 3px solid transparent;
        border-radius: 30px;
        padding: 3.5rem 3rem;
        margin: 2rem auto;
        max-width: 1200px;
        box-shadow: 
            0 0 80px rgba(162, 155, 254, 0.4),
            inset 0 0 80px rgba(255, 255, 255, 0.08),
            0 25px 50px rgba(0,0,0,0.6);
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(1deg);
        transition: all 0.4s ease;
    }
    
    .story-container:hover {
        transform: perspective(1000px) rotateX(0deg) scale(1.005);
        box-shadow: 
            0 0 100px rgba(162, 155, 254, 0.5),
            inset 0 0 100px rgba(255, 255, 255, 0.1),
            0 35px 70px rgba(0,0,0,0.7);
    }
    
    .story-container::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, #a29bfe, #fd79a8, #e17055, #74b9ff, #a29bfe);
        background-size: 400% 400%;
        border-radius: 30px;
        z-index: -1;
        animation: borderGlow 6s ease-in-out infinite;
        opacity: 0.8;
    }
    
    @keyframes borderGlow {
        0%, 100% { background-position: 0% 50%; opacity: 0.8; }
        25% { background-position: 100% 50%; opacity: 1; }
        50% { background-position: 100% 100%; opacity: 0.9; }
        75% { background-position: 0% 100%; opacity: 1; }
    }
    
    /* INDICATORI DI FASE MIGLIORATI */
    
    .phase-indicator {
        text-align: center;
        font-family: 'Cinzel', serif;
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(45deg, #ffd700, #ff6b6b, #4ecdc4, #a29bfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 3rem 0;
        padding: 2rem 1rem;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 25px;
        border: 3px solid rgba(255, 215, 0, 0.4);
        box-shadow: 
            0 0 40px rgba(255, 215, 0, 0.3),
            inset 0 0 40px rgba(255, 255, 255, 0.05);
        position: relative;
        letter-spacing: 3px;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }
    
    .phase-indicator::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: sweep 3s infinite;
        border-radius: 25px;
    }
    
    @keyframes sweep {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* DESCRIZIONI MIGLIORIATE */
    
    .phase-description {
        text-align: center;
        font-family: 'Crimson Text', serif;
        font-size: 1.4rem;
        line-height: 1.8;
        color: #f5f5f5;
        margin: 2.5rem 0;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: inset 0 0 30px rgba(255, 255, 255, 0.05);
        font-weight: 500;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    /* TESTO DELLA STORIA MIGLIORATO */
    
    .story-text {
        font-family: 'Crimson Text', serif;
        font-size: 1.4rem;
        line-height: 2;
        color: #f8f8f8;
        text-align: justify;
        margin: 2rem 0;
        padding: 2.5rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%);
        border-radius: 25px;
        border-left: 6px solid #ffd700;
        border-right: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 
            inset 0 0 40px rgba(255, 215, 0, 0.1),
            0 10px 30px rgba(0, 0, 0, 0.3);
        position: relative;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.2);
    }
    
    .story-text::before {
        content: '"';
        position: absolute;
        top: -10px;
        left: 15px;
        font-size: 4rem;
        color: rgba(255, 215, 0, 0.6);
        font-family: 'Cinzel', serif;
    }
    
    .story-text::after {
        content: '"';
        position: absolute;
        bottom: -30px;
        right: 25px;
        font-size: 4rem;
        color: rgba(255, 215, 0, 0.6);
        font-family: 'Cinzel', serif;
    }
    
    /* DISPLAY LORE MIGLIORATO */
    
    .lore-display {
        font-family: 'Crimson Text', serif;
        font-size: 1.3rem;
        line-height: 1.9;
        color: #f0f0f0;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(20, 20, 40, 0.9) 100%);
        padding: 2.5rem;
        border-radius: 20px;
        border: 2px solid rgba(74, 144, 226, 0.5);
        margin: 2rem 0;
        white-space: pre-line;
        max-height: 500px;
        overflow-y: auto;
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.4),
            inset 0 0 40px rgba(74, 144, 226, 0.1);
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
    }
    
    .lore-display::-webkit-scrollbar {
        width: 12px;
    }
    
    .lore-display::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
    }
    
    .lore-display::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #4a90e2, #74b9ff);
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .lore-display::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #74b9ff, #4a90e2);
    }
    
    /* MESSAGGI DI STATO MIGLIORATI */
    
    .status-message {
        padding: 1.5rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        font-family: 'Crimson Text', serif;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .status-loading {
        background: linear-gradient(135deg, rgba(74, 144, 226, 0.25) 0%, rgba(116, 185, 255, 0.25) 100%);
        border: 3px solid rgba(74, 144, 226, 0.6);
        color: #87ceeb;
        animation: pulse 2s infinite;
    }
    
    .status-success {
        background: linear-gradient(135deg, rgba(0, 184, 148, 0.25) 0%, rgba(85, 239, 196, 0.25) 100%);
        border: 3px solid rgba(0, 184, 148, 0.6);
        color: #55efc4;
        animation: successGlow 2s ease-in-out;
    }
    
    .status-error {
        background: linear-gradient(135deg, rgba(255, 65, 108, 0.25) 0%, rgba(255, 118, 117, 0.25) 100%);
        border: 3px solid rgba(255, 65, 108, 0.6);
        color: #ff7675;
        animation: shake 0.5s ease-in-out;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.02); }
    }
    
    @keyframes successGlow {
        0% { box-shadow: 0 0 20px rgba(0, 184, 148, 0.3); }
        50% { box-shadow: 0 0 40px rgba(0, 184, 148, 0.6); }
        100% { box-shadow: 0 0 20px rgba(0, 184, 148, 0.3); }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    /* BOTTONI MIGLIORATI */
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #667eea 75%, #764ba2 100%);
        background-size: 400% 400%;
        color: white;
        border: 4px solid rgba(255, 255, 255, 0.2);
        padding: 1.8rem 2.5rem;
        margin: 1.2rem 0;
        border-radius: 25px;
        font-size: 1.2rem;
        font-family: 'Crimson Text', serif;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.4),
            inset 0 3px 0 rgba(255,255,255,0.3),
            0 0 30px rgba(102, 126, 234, 0.4);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 3px;
        width: 100%;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: backgroundShift 4s ease-in-out infinite;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes backgroundShift {
        0%, 100% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.6),
            0 0 50px rgba(255, 215, 0, 0.6),
            inset 0 3px 0 rgba(255,255,255,0.5);
        border-color: rgba(255, 215, 0, 0.8);
        background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 25%, #4ecdc4 50%, #45b7d1 75%, #ffd700 100%);
        background-size: 400% 400%;
    }
    
    /* TEXTAREA MIGLIORATA */
    
    .stTextArea > div > div > textarea {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(20, 20, 40, 0.8) 100%) !important;
        color: #f5f5f5 !important;
        border: 3px solid rgba(255, 215, 0, 0.4) !important;
        border-radius: 20px !important;
        font-family: 'Crimson Text', serif !important;
        font-size: 1.2rem !important;
        padding: 1.5rem !important;
        line-height: 1.6 !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 
            0 10px 30px rgba(0, 0, 0, 0.3),
            inset 0 0 20px rgba(255, 215, 0, 0.1) !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #ffd700 !important;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.5),
            inset 0 0 30px rgba(255, 215, 0, 0.2) !important;
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(20, 20, 40, 0.9) 100%) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
        font-style: italic !important;
    }
    
    /* SIDEBAR MIGLIORATA (per le fasi successive) */
    
    .sidebar-content {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(20, 20, 40, 0.9) 100%);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 25px;
        margin: 1.5rem 0;
        border: 3px solid rgba(255, 215, 0, 0.5);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.5),
            inset 0 0 50px rgba(255, 215, 0, 0.1);
    }
    
    /* ANIMAZIONI */
    
    .fade-in {
        animation: fadeIn 1.2s ease-out;
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(40px) scale(0.95); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0) scale(1); 
        }
    }
    
    .slide-in {
        animation: slideIn 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateX(-60px) rotateY(-10deg); 
        }
        to { 
            opacity: 1; 
            transform: translateX(0) rotateY(0deg); 
        }
    }
    
    /* PLAN DISPLAY MIGLIORATO */
    
    .plan-item {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.7) 0%, rgba(30, 30, 50, 0.7) 100%);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 15px;
        border-left: 5px solid #ffa500;
        border-right: 2px solid rgba(255, 165, 0, 0.3);
        box-shadow: 
            0 8px 25px rgba(0, 0, 0, 0.3),
            inset 0 0 20px rgba(255, 165, 0, 0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .plan-item:hover {
        transform: translateX(10px) scale(1.02);
        border-left-width: 8px;
        box-shadow: 
            0 12px 35px rgba(0, 0, 0, 0.4),
            inset 0 0 30px rgba(255, 165, 0, 0.2);
    }
    
    .plan-number {
        color: #ffd700;
        font-weight: bold;
        font-size: 1.1rem;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
    }
    
    .plan-text {
        color: #f0f0f0;
        font-size: 1.1rem;
        margin-left: 1rem;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
    }
    
    /* RESPONSIVE IMPROVEMENTS */
    
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
            letter-spacing: 3px;
        }
        
        .phase-indicator {
            font-size: 1.6rem;
            padding: 1.5rem 1rem;
        }
        
        .phase-description {
            font-size: 1.2rem;
            padding: 1.5rem;
        }
        
        .creation-container,
        .validation-container,
        .story-container {
            padding: 2rem 1.5rem;
            margin: 1rem;
        }
        
        .stButton > button {
            font-size: 1rem;
            padding: 1.5rem 2rem;
            min-height: 70px;
            letter-spacing: 2px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Enumero gli stati dell'applicazione
class AppState:
    CREATION = "creation"
    LORE_REVIEW = "lore_review"
    VALIDATION = "validation"
    PLAN_REVIEW = "plan_review"
    STORY_GENERATION = "story_generation"
    GAMEPLAY = "gameplay"

def initialize_app_state():
    """Inizializza lo stato dell'applicazione"""
    if 'app_state' not in st.session_state:
        st.session_state.app_state = AppState.CREATION
    if 'llm' not in st.session_state:
        st.session_state.llm = None
    if 'generated_lore' not in st.session_state:
        st.session_state.generated_lore = ""
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = None
    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = []
    if 'story_generated' not in st.session_state:
        st.session_state.story_generated = False
    
    # Stati per il gameplay 
    if 'current_node' not in st.session_state:
        st.session_state.current_node = 'start'
    if 'story_history' not in st.session_state:
        st.session_state.story_history = []
    if 'choices_made' not in st.session_state:
        st.session_state.choices_made = []
    if 'choice_order_seed' not in st.session_state:
        st.session_state.choice_order_seed = random.randint(1, 1000000)
    if 'original_user_input' not in st.session_state:
        st.session_state.original_user_input = ""

def detect_lore_tone(lore_text):
    """
    Analizza il tono della lore per adattare la voce TTS
    """
    if not lore_text:
        return "neutral"
    
    text_lower = str(lore_text).lower()
    
    # Parole chiave per diversi toni
    dark_words = ['oscuro', 'tenebre', 'morte', 'sangue', 'demone', 'diavolo', 'inferno', 'maledizione', 'vendetta', 'ombra', 'paura', 'terrore']
    epic_words = ['eroe', 'leggenda', 'gloria', 'onore', 'vittoria', 'trionfo', 'destino', 'regno', 'impero', 'battaglia', 'guerra', 'coraggio']
    mystical_words = ['magia', 'incantesimo', 'mago', 'strega', 'cristallo', 'pozione', 'spirito', 'antico', 'mistico', 'arcano', 'elementale']
    adventure_words = ['avventura', 'esplorazione', 'tesoro', 'mappa', 'viaggio', 'scoperta', 'ricerca', 'quest', 'dungeon', 'labirinto']
    
    # Conteggio occorrenze
    dark_count = sum(1 for word in dark_words if word in text_lower)
    epic_count = sum(1 for word in epic_words if word in text_lower)
    mystical_count = sum(1 for word in mystical_words if word in text_lower)
    adventure_count = sum(1 for word in adventure_words if word in text_lower)
    
    # Determina il tono dominante
    max_count = max(dark_count, epic_count, mystical_count, adventure_count)
    
    if max_count == 0 or max_count < 2:
        return "neutral"
    elif dark_count == max_count:
        return "dark"
    elif epic_count == max_count:
        return "epic"
    elif mystical_count == max_count:
        return "mystical"
    else:
        return "adventure"


def clean_text_for_tts(text):
    """
    Pulisce il testo per il TTS rimuovendo emoji, caratteri speciali e formattazione
    """
    if not text:
        return ""
    
    # Converte in stringa se è un dizionario/oggetto
    if not isinstance(text, str):
        text = str(text)
    
    # Rimuove tutte le emoji usando regex Unicode
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U00002600-\U000027BF"  # misc symbols
        "\U000024C2-\U0001F251"  # enclosed characters
        "\U0001F170-\U0001F251"  # enclosed alphanumeric supplement
        "]+", 
        flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    # Rimuove caratteri markdown e formattazione
    text = re.sub(r'[*_`#]', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # Rimuove caratteri speciali comuni nelle liste
    text = re.sub(r'[•◦▪▫▸▹‣⁃]', '', text)
    
    # Sostituisce i pattern di struttura con testo più naturale per TTS
    text = re.sub(r'\*\*(.*?):\*\*', r'\1:', text)  # **Titolo:** -> Titolo:
    text = re.sub(r'Min:\s*(\d+)\s*\|\s*Max:\s*(\d+)', r'da \1 a \2', text)  # Min: 1 | Max: 3 -> da 1 a 3
    
    # Pulisce caratteri speciali rimanenti
    text = re.sub(r'[|\[\]{}]', '', text)
    
    # Sostituisce i bullet points con "punto" per una lettura più naturale
    text = re.sub(r'^\s*\*\s*', 'Punto: ', text, flags=re.MULTILINE)
    
    # Pulisce spazi multipli e caratteri di controllo
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[\n\r\t]+', ' ', text)
    
    # Rimuove spazi prima e dopo i due punti
    text = re.sub(r'\s*:\s*', ': ', text)
    
    # Limita la lunghezza per evitare timeout (aumentato il limite)
    if len(text) > 1500:
        # Trova l'ultimo punto prima del limite per non tagliare a metà frase
        last_period = text.rfind('.', 0, 1500)
        if last_period > 1000:  # Se troviamo un punto ragionevole
            text = text[:last_period + 1]
        else:
            text = text[:1500] + "..."
    
    return text.strip()


def generate_tts_audio(text, tone="neutral"):
    """
    Genera audio TTS con Google TTS o fallback su pyttsx3
    """
    if not text:
        return None
    
    cleaned_text = clean_text_for_tts(text)
    if not cleaned_text:
        return None
    
    audio_data = None
    
    # Prova prima con Google TTS
    if GTTS_AVAILABLE:
        try:
            # Seleziona parametri basati sul tono
            if tone == "dark":
                lang = 'it'
                slow = True
            elif tone == "epic":
                lang = 'it'
                slow = False
            elif tone == "mystical":
                lang = 'it'
                slow = True
            else:  # neutral, adventure
                lang = 'it'
                slow = False
            
            tts = gTTS(text=cleaned_text, lang=lang, slow=slow)
            
            # Salva in memoria
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            audio_data = audio_buffer.getvalue()
            
        except Exception as e:
            print(f"Errore Google TTS: {e}")
            audio_data = None
    
    # Fallback su pyttsx3 (offline)
    if audio_data is None and PYTTSX3_AVAILABLE:
        try:
            engine = pyttsx3.init()
            
            # Configura voce basata sul tono
            voices = engine.getProperty('voices')
            if voices:
                # Seleziona voce femminile per mistico, maschile per epico
                if tone == "mystical" and len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)
                elif tone in ["epic", "dark"] and len(voices) > 0:
                    engine.setProperty('voice', voices[0].id)
            
            # Configura velocità e volume
            rate = engine.getProperty('rate')
            if tone == "dark":
                engine.setProperty('rate', rate - 50)
            elif tone == "epic":
                engine.setProperty('rate', rate + 20)
            else:
                engine.setProperty('rate', rate)
            
            # Salva in file temporaneo
            temp_file = "temp_audio.wav"
            engine.save_to_file(cleaned_text, temp_file)
            engine.runAndWait()
            
            # Leggi il file
            try:
                with open(temp_file, 'rb') as f:
                    audio_data = f.read()
                os.remove(temp_file)  # Pulisci il file temporaneo
            except:
                pass
                
        except Exception as e:
            print(f"Errore pyttsx3: {e}")
            audio_data = None
    
    return audio_data

def create_audio_player(audio_data, tone="neutral"):
    """
    Crea un player audio HTML5 con styling personalizzato
    """
    if not audio_data:
        return ""
    
    # Converti in base64
    audio_base64 = base64.b64encode(audio_data).decode()
    
    # Colori basati sul tono
    if tone == "dark":
        bg_color = "rgba(139, 69, 19, 0.3)"
        accent_color = "#8B4513"
    elif tone == "epic":
        bg_color = "rgba(255, 215, 0, 0.3)"
        accent_color = "#FFD700"
    elif tone == "mystical":
        bg_color = "rgba(138, 43, 226, 0.3)"
        accent_color = "#8A2BE2"
    else:  # neutral, adventure
        bg_color = "rgba(74, 144, 226, 0.3)"
        accent_color = "#4A90E2"
    
    return f"""
    <div style="
        background: {bg_color};
        border: 2px solid {accent_color};
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        text-align: center;
        backdrop-filter: blur(10px);
    ">
        <h4 style="
            color: {accent_color};
            font-family: 'Cinzel', serif;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        ">
            🎵 NARRATORE MAGICO 🎵
        </h4>
        <audio controls style="
            width: 100%;
            max-width: 400px;
            height: 40px;
            border-radius: 20px;
            outline: none;
        ">
            <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
            Il tuo browser non supporta l'audio HTML5.
        </audio>
        <p style="
            color: #f0f0f0;
            font-size: 0.9rem;
            margin-top: 0.8rem;
            font-style: italic;
        ">
            🎭 Tono: <strong style="color: {accent_color};">{tone.title()}</strong> | 
            🔊 Ascolta la tua leggenda prendere vita!
        </p>
    </div>
    """



def setup_llm():
    """Configura il modello LLM"""
    if st.session_state.llm is None:
        load_dotenv()
        API_KEY = os.getenv("API_KEY2")            
        os.environ["GOOGLE_API_KEY"] = API_KEY
        st.session_state.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            temperature=0.6
        )
    return True


def validate_pddl_complete(llm, max_attempts=100):
    """
    Esegue la validazione completa PDDL con FastDownward e VAL.
    
    Args:
        llm: Modello di linguaggio per le correzioni
        max_attempts: Numero massimo di tentativi per evitare loop infiniti
    
    Returns:
        dict: Risultati della validazione finale
    """
    
    attempt = 0
    
    while attempt < max_attempts:
        print(f"\n🔄 Tentativo di validazione {attempt + 1}/{max_attempts}")
        
        # STEP 1: Validazione FastDownward (stampe già gestite dalla classe)
        pddl_validation_output = run_fastdownward_complete()
        
        # Se FastDownward fallisce, correggi e riprova
        if not pddl_validation_output["overall_success"]:
            print("🔄 Correggendo il PDDL per FastDownward...")
            run_correction_workflow(pddl_validation_output["planning_results"]["planning_output"], llm)
            attempt += 1
            continue
        
        # STEP 2: Validazione VAL (stampe già gestite dalla classe)
        validation_results = validate_plan_with_val()
        
        # Se VAL passa, abbiamo finito
        if validation_results["validation_successful"] and validation_results["plan_valid"]:
            print(f"\n🎉 VALIDAZIONE COMPLETA: SUCCESSO! (Tentativi: {attempt + 1}/{max_attempts})")
            return {
                "success": True,
                "pddl_output": pddl_validation_output,
                "val_results": validation_results,
                "attempts": attempt + 1
            }
        
        # Se VAL fallisce, correggi e ricomincia da FastDownward
        print("🔄 Correggendo il PDDL per VAL e riavviando da FastDownward...")
        
        error_message = get_validation_error_for_correction(validation_results)
        print("Sono qui")
        print(f"Errore di validazione: {error_message}")
        run_correction_workflow(error_message, llm)
        
        attempt += 1
    
    # Se arriviamo qui, abbiamo esaurito i tentativi
    print(f"\n❌ VALIDAZIONE FALLITA: Esauriti tutti i {max_attempts} tentativi")
    return {
        "success": False,
        "error": "Numero massimo di tentativi raggiunto",
        "attempts": max_attempts
    }

def render_creation_phase():
    """Renderizza la fase di creazione della lore"""
    st.markdown('<div class="creation-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="phase-indicator">
        🎨 FASE I: FORGIATURA DELLA LEGGENDA 🎨
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="phase-description">
        <strong>🌟 Benvenuto, Narratore Supremo! 🌟</strong><br><br>
        Qui inizia il tuo viaggio epico nella creazione di mondi fantastici. Descrivi con passione 
        l'universo che desideri esplorare: regni incantati, eroi coraggiosi, creature mistiche, 
        antichi segreti e sfide epiche.<br><br>
        <em>✨ Ogni parola che scrivi diventerà realtà nella tua avventura personale ✨</em>
    </div>
    """, unsafe_allow_html=True)
    
    # Sezione di input migliorata
    st.markdown("""
    <div style="background: rgba(255, 215, 0, 0.1); border: 2px solid rgba(255, 215, 0, 0.3); border-radius: 20px; padding: 2rem; margin: 2rem 0;">
        <h3 style="color: #ffd700; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1.5rem; font-size: 1.5rem;">
            📝 CANVAS DELLA CREAZIONE 📝
        </h3>
        <p style="text-align: center; color: #f0f0f0; font-style: italic; margin-bottom: 1rem;">
            Dipingi il tuo mondo con le parole...
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input dell'utente
    user_input = st.text_area(
        "",
        placeholder="🏰 Esempio: Un regno medievale avvolto nella magia, dove sono un cavaliere-mago alla ricerca dell'antica Corona del Destino. Il mio nemico è un drago antico che controlla un esercito di creature delle tenebre. Possiedo poteri elementali e una spada incantata, ma dovrò superare labirinti magici, risolvere enigmi ancestrali e conquistare la fiducia di alleati misteriosi per raggiungere la mia meta...",
        height=200,
        key="story_input",
        label_visibility="collapsed"
    )
    
    # Suggerimenti creativi
    st.markdown("""
    <div style="background: rgba(74, 144, 226, 0.1); border: 2px solid rgba(74, 144, 226, 0.3); border-radius: 15px; padding: 1.5rem; margin: 1.5rem 0;">
        <h4 style="color: #4a90e2; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1rem;">
            💡 SCINTILLE DI ISPIRAZIONE 💡
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; font-size: 0.95rem; color: #e8e8e8;">
            <div>🏛️ <strong>Ambientazione:</strong> Regno, città futuristica, mondo sotterraneo, dimensioni parallele...</div>
            <div>⚔️ <strong>Protagonista:</strong> Cavaliere, mago, esploratore, detective, guerriero cosmico...</div>
            <div>🐉 <strong>Antagonista:</strong> Drago, tiranno, entità cosmica, intelligenza artificiale...</div>
            <div>🎯 <strong>Obiettivo:</strong> Salvare qualcuno, trovare un artefatto, svelare un mistero...</div>
            <div>✨ <strong>Poteri:</strong> Magia elementale, tecnologie avanzate, abilità psichiche...</div>
            <div>🗺️ <strong>Sfide:</strong> Labirinti, enigmi, battaglie, prove di coraggio...</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Bottone principale
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 FORGIA LA LEGGENDA ETERNA", key="create_story"):
            if user_input.strip():
                if setup_llm():
                    with st.spinner("🔮 I fili del destino si intrecciano per dare vita al tuo mondo... ⭐"):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            # Salva l'input originale dell'utente
                            st.session_state.original_user_input = user_input
                            
                            status_text.text("📜 Evocando gli spiriti della creatività...")
                            progress_bar.progress(25)
                            time.sleep(1)
                            
                            status_text.text("🏗️ Costruendo i pilastri del tuo universo...")
                            progress_bar.progress(50)
                            
                            generate_lore(user_input, st.session_state.llm)
                            
                            status_text.text("✨ Infondendo vita nei personaggi...")
                            progress_bar.progress(75)
                            time.sleep(1)
                            
                            st.session_state.generated_lore = load_example_json("file_generati/lore_generata_per_utente.json")
                            
                            progress_bar.progress(100)
                            status_text.text("🎉 La tua leggenda è nata!")
                            time.sleep(1)
                            
                            st.session_state.app_state = AppState.LORE_REVIEW
                            st.rerun()
                        except Exception as e:
                            st.error(f"⚠️ Gli spiriti della creazione sono temporaneamente indisponibili: {e}")
            else:
                st.markdown("""
                <div class="status-error">
                    ⚠️ Il canvas della creazione è vuoto! Condividi la tua visione per dare vita al mondo dei tuoi sogni.
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_lore_review():
    """Renderizza la fase di revisione della lore con TTS"""
    st.markdown('<div class="creation-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="phase-indicator">
        📚 FASE II: LA LEGGENDA PRENDE FORMA 📚
    </div>
    """, unsafe_allow_html=True)
    
    # Mostra la lore generata
    if st.session_state.generated_lore:
        st.markdown("""
        <div class="phase-description">
            <strong>🎭 Ecco la tua leggenda forgiata! 🎭</strong><br><br>
            Ogni parola è stata tessuta con cura per creare un mondo ricco e coinvolgente. 
            Esamina attentamente ogni dettaglio: questo sarà il fondamento della tua avventura epica.<br><br>
            <em>🔍 Se qualcosa non rispecchia la tua visione, possiamo perfezionarla insieme</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Contenitore per la lore con header decorativo
        st.markdown("""
        <div style="background: rgba(255, 215, 0, 0.1); border: 3px solid rgba(255, 215, 0, 0.4); border-radius: 25px; padding: 2rem; margin: 2rem 0;">
            <h3 style="color: #ffd700; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 2rem; font-size: 2rem; text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);">
                📜 IL CODICE DELLA TUA LEGGENDA 📜
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # AGGIUNTA TTS: Genera e mostra il player audio
        lore_text = print_lore()
        
        # Controlla se TTS è disponibile
        if GTTS_AVAILABLE or PYTTSX3_AVAILABLE:
            # Genera audio se non esiste o se la lore è cambiata
            if ('lore_audio' not in st.session_state or 
                'last_lore_text' not in st.session_state or 
                st.session_state.last_lore_text != lore_text):
                
                with st.spinner("🎵 Il narratore sta preparando la sua voce magica... ✨"):
                    tone = detect_lore_tone(lore_text)
                    audio_data = generate_tts_audio(lore_text, tone)
                    
                    if audio_data:
                        st.session_state.lore_audio = audio_data
                        st.session_state.lore_tone = tone
                        st.session_state.last_lore_text = lore_text
                        st.success("🎭 Il narratore è pronto a dare voce alla tua leggenda!")
                    else:
                        st.warning("⚠️ Il narratore magico è temporaneamente indisponibile. Puoi comunque leggere la tua leggenda qui sotto.")
            
            # Mostra il player se l'audio è disponibile
            if hasattr(st.session_state, 'lore_audio') and st.session_state.lore_audio:
                audio_player = create_audio_player(
                    st.session_state.lore_audio, 
                    getattr(st.session_state, 'lore_tone', 'neutral')
                )
                st.markdown(audio_player, unsafe_allow_html=True)
        else:
            # Messaggio se TTS non è disponibile
            st.markdown("""
            <div style="background: rgba(255, 165, 0, 0.1); border: 2px solid rgba(255, 165, 0, 0.3); border-radius: 15px; padding: 1.5rem; margin: 1.5rem 0; text-align: center;">
                <p style="color: #ffa500; font-family: 'Crimson Text', serif; font-size: 1rem; margin: 0;">
                    🔇 <strong>Narratore Magico non disponibile</strong><br>
                    <em style="color: #f0f0f0; font-size: 0.9rem;">Per attivare la lettura audio, installa: pip install gtts pyttsx3</em>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Mostra il testo della lore (come prima)
        st.markdown(f"""
        <div class="lore-display">
            {lore_text}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Sezione di controllo migliorata (resto della funzione rimane uguale)
        st.markdown("""
        <div style="background: rgba(162, 155, 254, 0.1); border: 2px solid rgba(162, 155, 254, 0.3); border-radius: 20px; padding: 2rem; margin: 2rem 0;">
            <h4 style="color: #a29bfe; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1.5rem; font-size: 1.4rem;">
                ⚖️ GIUDIZIO DEL CREATORE ⚖️
            </h4>
            <p style="text-align: center; color: #f0f0f0; font-size: 1.1rem; margin-bottom: 2rem;">
                La leggenda rispecchia la tua visione? Ogni dettaglio è come lo avevi immaginato?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Opzioni per modifiche
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ PERFETTO! PROCEDIAMO ALL'ETERNITÀ", key="approve_lore"):
                st.markdown("""
                <div class="status-success">
                    🌟 Eccellente! La tua leggenda è stata sigillata negli annali del destino!
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)
                st.session_state.app_state = AppState.VALIDATION
                st.rerun()
        
        with col2:
            if st.button("✏️ AFFINARE LA PERFEZIONE", key="modify_lore"):
                st.session_state.show_modification_form = True
                
        # Form per modifiche (se richiesto)
        if hasattr(st.session_state, 'show_modification_form') and st.session_state.show_modification_form:
            st.markdown("---")
            
            st.markdown("""
            <div style="background: rgba(255, 165, 0, 0.1); border: 2px solid rgba(255, 165, 0, 0.3); border-radius: 20px; padding: 2rem; margin: 2rem 0;">
                <h4 style="color: #ffa500; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1.5rem; font-size: 1.3rem;">
                    🎨 LABORATORIO DELLE MODIFICHE 🎨
                </h4>
                <p style="text-align: center; color: #f0f0f0; margin-bottom: 1rem;">
                    Descrivi le modifiche che desideri apportare alla tua leggenda
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            modification_request = st.text_area(
                "",
                placeholder="🎯 Esempi di modifiche:\n• Rendere l'ambientazione più oscura e misteriosa\n• Aggiungere un compagno di avventure fedele\n• Cambiare il villain in una strega malvagia\n• Includere più elementi magici e creature fantastiche\n• Modificare l'obiettivo finale dell'avventura...",
                height=120,
                key="modification_input",
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 RIFORGIA LA LEGGENDA", key="apply_modifications"):
                    if modification_request.strip():
                        with st.spinner("🎨 I maestri artigiani stanno rimodellando la tua opera... ✨"):
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.text("🔧 Analizzando le tue richieste...")
                                progress_bar.progress(33)
                                time.sleep(1)
                                
                                status_text.text("⚒️ Riforgiando gli elementi narrativi...")
                                progress_bar.progress(66)
                                
                                update_lore_with_corrections(modification_request, st.session_state.llm)
                                st.session_state.generated_lore = load_example_json("file_generati/lore_generata_per_utente.json")
                                
                                # AGGIUNTA TTS: Cancella l'audio precedente per rigenerarlo
                                if 'lore_audio' in st.session_state:
                                    del st.session_state.lore_audio
                                if 'last_lore_text' in st.session_state:
                                    del st.session_state.last_lore_text
                                
                                progress_bar.progress(100)
                                status_text.text("✨ Modifiche completate con maestria!")
                                time.sleep(1)
                                
                                st.session_state.show_modification_form = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"⚠️ Errore durante la riforgiatura: {e}")
                    else:
                        st.markdown("""
                        <div class="status-error">
                            ⚠️ Descrivi le modifiche che desideri per affinare la tua leggenda!
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                if st.button("❌ MANTIENI L'ORIGINALE", key="cancel_modifications"):
                    st.session_state.show_modification_form = False
                    st.rerun()
    else:
        st.error("❌ Errore: La leggenda sembra essere svanita nel nulla!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_validation_phase():
    """Renderizza la fase di validazione PDDL"""
    st.markdown('<div class="validation-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="phase-indicator">
        ⚙️ FASE III: FORGIATURA DELLE LEGGI UNIVERSALI ⚙️
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="phase-description">
        <strong>🏛️ Il Tempio delle Regole Cosmiche 🏛️</strong><br><br>
        Ora inizia la fase più misteriosa: la trasformazione della tua leggenda in leggi universali precise. 
        Gli antichi algoritmi tessono le regole che governeranno ogni azione, ogni scelta, ogni conseguenza 
        del tuo mondo.<br><br>
        <em>⚡ Questo processo garantisce che la tua avventura sia logicamente perfetta e priva di paradossi</em>
    </div>
    """, unsafe_allow_html=True)
    
    # Sezione informativa sul processo
    st.markdown("""
    <div style="background: rgba(255, 165, 0, 0.1); border: 2px solid rgba(255, 165, 0, 0.4); border-radius: 20px; padding: 2rem; margin: 2rem 0;">
        <h4 style="color: #ffa500; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1.5rem; font-size: 1.4rem;">
            🔬 ALCHIMIA COMPUTAZIONALE 🔬
        </h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; font-size: 1rem; color: #f0f0f0;">
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">📐</div>
                <strong>Creazione del Dominio</strong><br>
                <em>Definizione delle regole fondamentali</em>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎯</div>
                <strong>Generazione del Problema</strong><br>
                <em>Impostazione degli obiettivi</em>
            </div>
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧪</div>
                <strong>Validazione Quantica</strong><br>
                <em>Verifica della coerenza logica</em>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.validation_results is None:
        # Sezione di avvio processo
        st.markdown("""
        <div style="background: rgba(162, 155, 254, 0.1); border: 2px solid rgba(162, 155, 254, 0.3); border-radius: 20px; padding: 2rem; margin: 2rem 0; text-align: center;">
            <h4 style="color: #a29bfe; font-family: 'Cinzel', serif; margin-bottom: 1.5rem; font-size: 1.5rem;">
                ⚡ ATTIVAZIONE DEL MOTORE COSMICO ⚡
            </h4>
            <p style="color: #f0f0f0; font-size: 1.1rem; margin-bottom: 2rem;">
                Tutto è pronto per invocare le forze primordiali che daranno struttura logica al tuo universo.<br>
                <em>⏳ Il processo richiederà alcuni momenti di concentrazione cosmica...</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔥 INIZIA LA FORGIATURA DELLE LEGGI", key="start_validation"):
                
                # Container per il progresso
                progress_container = st.container()
                
                with progress_container:
                    st.markdown("""
                    <div class="status-loading">
                        🌌 PROCESSO DI FORGIATURA IN CORSO 🌌
                    </div>
                    """, unsafe_allow_html=True)
                    
                    overall_progress = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Creazione dominio
                    with st.spinner("📐 Creando l'architettura del dominio universale..."):
                        try:
                            status_text.text("🏗️ Fase 1/3: Costruendo le fondamenta del mondo...")
                            overall_progress.progress(15)
                            
                            create_domain_pddl(st.session_state.llm)
                            
                            overall_progress.progress(33)
                            st.success("✅ Dominio creato con maestria!")
                            time.sleep(1)
                        except Exception as e:
                            st.error(f"❌ Errore nella creazione del dominio: {e}")
                            return
                    
                    # Step 2: Creazione problema
                    with st.spinner("🎯 Definendo gli obiettivi e le sfide..."):
                        try:
                            status_text.text("🎲 Fase 2/3: Tessendo la trama delle sfide...")
                            overall_progress.progress(50)
                            
                            create_problem_pddl(st.session_state.llm)
                            
                            overall_progress.progress(66)
                            st.success("✅ Problema strutturato perfettamente!")
                            time.sleep(1)
                        except Exception as e:
                            st.error(f"❌ Errore nella creazione del problema: {e}")
                            return
                    
                    # Step 3: Validazione completa
                    with st.spinner("🧪 Validando la coerenza delle leggi cosmiche... (Momento di massima concentrazione)"):
                        try:
                            status_text.text("⚡ Fase 3/3: Invocando gli spiriti della logica suprema...")
                            overall_progress.progress(80)
                            
                            validation_results = validate_pddl_complete(st.session_state.llm)
                            st.session_state.validation_results = validation_results
                            
                            overall_progress.progress(100)
                            
                            if validation_results["success"]:
                                st.session_state.current_plan = validation_results["pddl_output"]["solution_results"]["actions"]
                                
                                st.markdown("""
                                <div class="status-success">
                                    🎉 TRIONFO ASSOLUTO! Le leggi del tuo universo sono state forgiate con perfezione divina! 🎉
                                </div>
                                """, unsafe_allow_html=True)
                                
                                time.sleep(2)
                                st.session_state.app_state = AppState.PLAN_REVIEW
                            else:
                                st.markdown(f"""
                                <div class="status-error">
                                    ⚠️ Le forze cosmiche hanno incontrato resistenza: {validation_results.get('error', 'Perturbazione sconosciuta nel tessuto spazio-temporale')}
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Turbolenza nel processo di validazione: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_plan_review():
    """Renderizza la fase di revisione del piano"""
    st.markdown('<div class="validation-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="phase-indicator">
        📋 FASE IV: MAPPA DEL DESTINO EROICO 📋
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_plan:
        st.markdown("""
        <div class="phase-description">
            <strong>🗺️ La Strada verso la Gloria è Tracciata! 🗺️</strong><br><br>
            Ecco la sequenza epica che guiderà il tuo eroe verso il trionfo. Ogni azione è stata calcolata 
            con precisione matematica per garantire una progressione logica e coinvolgente.<br><br>
            <em>⚔️ Questo è il blueprint della tua leggenda: ogni passo verso l'immortalità</em>
        </div>
        """, unsafe_allow_html=True)
        
        num_azioni = len(st.session_state.current_plan)

        html = f"""
            <div style="background: rgba(255, 165, 0, 0.1); border: 3px solid rgba(255, 165, 0, 0.4); border-radius: 25px; padding: 2rem; margin: 2rem 0;">
                <h3 style="color: #ffa500; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1rem; font-size: 2rem; text-shadow: 0 0 20px rgba(255, 165, 0, 0.8);">
                    ⚔️ CODICE DELLE GESTA EROICHE ⚔️
                </h3>
                <p style="text-align: center; color: #f0f0f0; font-size: 1.1rem; font-style: italic;">
                    Sequenza di {num_azioni} azioni magistrali verso la vittoria
                </p>
            </div>
        """
        st.markdown(html, unsafe_allow_html=True)
            
        # Mostra il piano con styling migliorato
        st.markdown("### 📜 La Cronaca delle Tue Gesta:")
        
        for i, action in enumerate(st.session_state.current_plan, 1):
            # Icone diverse per diverse fasi dell'avventura
            if i <= len(st.session_state.current_plan) // 3:
                phase_icon = "🌅"  # Inizio
                phase_color = "#4a90e2"
            elif i <= 2 * len(st.session_state.current_plan) // 3:
                phase_icon = "⚡"  # Sviluppo
                phase_color = "#ffa500"
            else:
                phase_icon = "👑"  # Climax
                phase_color = "#ff6b6b"
            
            st.markdown(f"""
            <div class="plan-item">
                <span class="plan-number">{phase_icon} Atto {i:2d}:</span>
                <span class="plan-text">{action}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Statistiche del piano
        st.markdown(f"""
        <div style="background: rgba(0, 184, 148, 0.1); border: 2px solid rgba(0, 184, 148, 0.4); border-radius: 20px; padding: 2rem; margin: 2rem 0; text-align: center;">
            <h4 style="color: #00b894; font-family: 'Cinzel', serif; margin-bottom: 1rem; font-size: 1.3rem;">
                📊 ANALISI DELL'EPOPEA 📊
            </h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; font-size: 1rem; color: #f0f0f0;">
                <div><strong style="color: #55efc4;">🎯 Azioni Totali:</strong> {len(st.session_state.current_plan)}</div>
                <div><strong style="color: #55efc4;">⚡ Complessità:</strong> {"Epica" if len(st.session_state.current_plan) > 8 else "Leggendaria" if len(st.session_state.current_plan) > 5 else "Classica"}</div>
                <div><strong style="color: #55efc4;">🏆 Probabilità Gloria:</strong> 100%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Sezione di controllo migliorata
        st.markdown("""
        <div style="background: rgba(162, 155, 254, 0.1); border: 2px solid rgba(162, 155, 254, 0.3); border-radius: 20px; padding: 2rem; margin: 2rem 0;">
            <h4 style="color: #a29bfe; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1.5rem; font-size: 1.4rem;">
                ⚖️ APPROVAZIONE DEL MAESTRO ⚖️
            </h4>
            <p style="text-align: center; color: #f0f0f0; font-size: 1.1rem; margin-bottom: 1rem;">
                La sequenza delle gesta rispecchia il percorso eroico che avevi immaginato?
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Opzioni per il piano
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ PERFETTO! VERSO L'IMMORTALITÀ!", key="approve_plan"):
                st.markdown("""
                <div class="status-success">
                    🌟 Eccellente! Il destino ha approvato la tua mappa verso la gloria eterna!
                </div>
                """, unsafe_allow_html=True)
                time.sleep(1)
                st.session_state.app_state = AppState.STORY_GENERATION
                st.rerun()
        
        with col2:
            if st.button("🔧 RIDISEGNARE IL DESTINO", key="modify_plan"):
                st.session_state.show_plan_modification = True
        
        # Form per correzioni del piano
        if hasattr(st.session_state, 'show_plan_modification') and st.session_state.show_plan_modification:
            st.markdown("---")
            
            st.markdown("""
            <div style="background: rgba(255, 65, 108, 0.1); border: 2px solid rgba(255, 65, 108, 0.3); border-radius: 20px; padding: 2rem; margin: 2rem 0;">
                <h4 style="color: #ff416c; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1.5rem; font-size: 1.3rem;">
                    🎭 ATELIER DELLE CORREZIONI EPICHE 🎭
                </h4>
                <p style="text-align: center; color: #f0f0f0; margin-bottom: 1rem;">
                    Descrivi come vorresti modificare il percorso della tua leggenda
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            plan_correction = st.text_area(
                "",
                placeholder="🎯 Esempi di correzioni del piano:\n• Il protagonista dovrebbe prima ottenere un'arma magica\n• Aggiungere un incontro con un mentore saggio\n• Il boss finale dovrebbe essere affrontato dopo aver raccolto più alleati\n• Includere una fase di esplorazione di un tempio antico\n• Modificare l'ordine delle sfide per una progressione più naturale...",
                height=120,
                key="plan_correction_input",
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 RIDEFINISCI IL DESTINO", key="apply_plan_corrections"):
                    if plan_correction.strip():
                        with st.spinner("🔧 Gli architetti del fato stanno ridisegnando il tuo percorso... ⭐"):
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            try:
                                status_text.text("📐 Analizzando le tue visioni correttive...")
                                progress_bar.progress(25)
                                time.sleep(1)
                                
                                status_text.text("⚒️ Riorganizzando le sfere del destino...")
                                progress_bar.progress(50)
                                
                                run_user_correction_pddl(plan_correction, st.session_state.llm)
                                
                                status_text.text("🧪 Rivalidando le nuove leggi cosmiche...")
                                progress_bar.progress(75)
                                
                                # Rivalidazione
                                validation_results = validate_pddl_complete(st.session_state.llm)
                                
                                if validation_results["success"]:
                                    st.session_state.current_plan = validation_results["pddl_output"]["solution_results"]["actions"]
                                    st.session_state.show_plan_modification = False
                                    
                                    progress_bar.progress(100)
                                    status_text.text("✨ Destino ridefinito con maestria!")
                                    
                                    st.markdown("""
                                    <div class="status-success">
                                        🎉 Il piano è stato riforgiato secondo la tua volontà suprema!
                                    </div>
                                    """, unsafe_allow_html=True)
                                    time.sleep(2)
                                    st.rerun()
                                else:
                                    st.markdown("""
                                    <div class="status-error">
                                        ⚠️ Le forze cosmiche resistono alle modifiche. Prova con correzioni diverse o accetta il piano attuale.
                                    </div>
                                    """, unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"❌ Turbulenza nella correzione del destino: {e}")
                    else:
                        st.markdown("""
                        <div class="status-error">
                            ⚠️ Descrivi le correzioni che desideri per ridefinire il tuo percorso eroico!
                        </div>
                        """, unsafe_allow_html=True)
            
            with col2:
                if st.button("❌ MANTIENI IL PIANO ORIGINALE", key="cancel_plan_corrections"):
                    st.session_state.show_plan_modification = False
                    st.rerun()
    
    else:
        st.markdown("""
        <div class="status-error">
            ❌ Errore: La mappa del destino sembra essere svanita nelle nebbie del tempo!
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_story_generation():
    """Renderizza la fase di generazione della storia interattiva"""
    st.markdown('<div class="story-container fade-in">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="phase-indicator">
        📖 FASE V: NASCITA DELL'AVVENTURA INTERATTIVA 📖
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.story_generated:
        st.markdown("""
        <div class="phase-description">
            <strong>🎭 Il Momento della Trasformazione Suprema! 🎭</strong><br><br>
            Ora avviene la magia finale: la tua leggenda si trasforma in un'avventura vivente e interattiva. 
            Ogni scelta che farai influenzerà il corso degli eventi, ogni decisione plasmerà il destino 
            del tuo eroe.<br><br>
            <em>✨ Preparati a diventare il protagonista della storia che hai creato ✨</em>
        </div>
        """, unsafe_allow_html=True)
        
        # Sezione informativa sul processo
        st.markdown("""
        <div style="background: rgba(162, 155, 254, 0.1); border: 2px solid rgba(162, 155, 254, 0.4); border-radius: 20px; padding: 2rem; margin: 2rem 0;">
            <h4 style="color: #a29bfe; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1.5rem; font-size: 1.4rem;">
                🌟 METAMORFOSI NARRATIVA 🌟
            </h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; font-size: 1rem; color: #f0f0f0;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🎲</div>
                    <strong>Scelte Multiple</strong><br>
                    <em>Ogni decisione conta</em>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌈</div>
                    <strong>Finali Diversi</strong><br>
                    <em>Il tuo destino nelle tue mani</em>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚡</div>
                    <strong>Azione e Conseguenza</strong><br>
                    <em>Ogni gesto ha un risultato</em>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Sezione di attivazione
        st.markdown("""
        <div style="background: rgba(255, 215, 0, 0.1); border: 2px solid rgba(255, 215, 0, 0.3); border-radius: 20px; padding: 2rem; margin: 2rem 0; text-align: center;">
            <h4 style="color: #ffd700; font-family: 'Cinzel', serif; margin-bottom: 1.5rem; font-size: 1.5rem;">
                🔮 INVOCAZIONE DELL'INTERATTIVITÀ 🔮
            </h4>
            <p style="color: #f0f0f0; font-size: 1.1rem; margin-bottom: 2rem;">
                È giunto il momento di dare vita alla tua creazione. L'algoritmo narrativo tessserà 
                una rete di scelte e conseguenze basata sulla tua leggenda.<br>
                <em>⏳ Questo rituale richiederà alcuni momenti di concentrazione...</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ DAI VITA ALLA LEGGENDA INTERATTIVA", key="generate_story"):
                
                # Container per il progresso
                progress_container = st.container()
                
                with progress_container:
                    st.markdown("""
                    <div class="status-loading">
                        🌌 PROCESSO DI VIVIFICAZIONE IN CORSO 🌌
                    </div>
                    """, unsafe_allow_html=True)
                    
                    overall_progress = st.progress(0)
                    status_text = st.empty()
                    
                    with st.spinner("🎭 Gli spiriti della narrativa stanno tessendo la tua avventura interattiva... ⭐"):
                        try:
                            status_text.text("📝 Fase 1/4: Creando i capitoli della tua saga...")
                            overall_progress.progress(25)
                            time.sleep(1)
                            
                            status_text.text("🎲 Fase 2/4: Forgiando le scelte cruciali...")
                            overall_progress.progress(50)
                            time.sleep(1)
                            
                            status_text.text("🌈 Fase 3/4: Intrecciando i fili del destino...")
                            overall_progress.progress(75)
                            
                            generate_story(st.session_state.llm)
                            
                            status_text.text("✨ Fase 4/4: Infondendo l'anima interattiva...")
                            overall_progress.progress(100)
                            time.sleep(1)
                            
                            st.session_state.story_generated = True
                            
                            st.markdown("""
                            <div class="status-success">
                                🎉 MIRACOLO COMPIUTO! La tua avventura interattiva pulsa di vita propria! 🎉
                            </div>
                            """, unsafe_allow_html=True)
                            time.sleep(2)
                            st.session_state.app_state = AppState.GAMEPLAY
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Perturbazione nel tessuto narrativo: {e}")
    else:
        st.markdown("""
        <div class="phase-description">
            <strong>🎊 La Trasformazione è Completa! 🎊</strong><br><br>
            La tua leggenda ha acquisito vita propria ed è pronta per essere vissuta. 
            Ogni pagina ti aspetta, ogni scelta ti chiama.<br><br>
            <em>🚀 È tempo di diventare l'eroe della tua stessa creazione!</em>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="status-success">
            🌟 La tua avventura interattiva è stata forgiata con successo divino! 🌟
        </div>
        """, unsafe_allow_html=True)
        
        # Statistiche della storia generata
        st.markdown("""
        <div style="background: rgba(0, 184, 148, 0.1); border: 2px solid rgba(0, 184, 148, 0.4); border-radius: 20px; padding: 2rem; margin: 2rem 0; text-align: center;">
            <h4 style="color: #00b894; font-family: 'Cinzel', serif; margin-bottom: 1rem; font-size: 1.3rem;">
                📊 CARATTERISTICHE DELL'AVVENTURA 📊
            </h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; font-size: 1rem; color: #f0f0f0;">
                <div><strong style="color: #55efc4;">🎭 Tipo:</strong> Avventura Interattiva</div>
                <div><strong style="color: #55efc4;">🎲 Scelte:</strong> Multiple per Capitolo</div>
                <div><strong style="color: #55efc4;">🌈 Finali:</strong> Diversi Possibili</div>
                <div><strong style="color: #55efc4;">⚡ Rigiocabilità:</strong> Infinita</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎮 INIZIA L'AVVENTURA EPICA!", key="start_gameplay"):
                st.session_state.app_state = AppState.GAMEPLAY
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Funzioni per il gameplay (mantenute identiche)
def load_story() -> List[Dict[str, Any]]:
    """Carica la storia dal file JSON"""
    try:
        with open(Path("file_generati/storia_generata.json"), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("📁 File della storia non trovato!")
        return []
    except json.JSONDecodeError:
        st.error("⚠️ Errore nel formato del file JSON!")
        return []

def find_node_by_id(story_data: List[Dict], node_id: str) -> Dict[str, Any]:
    """Trova un nodo specifico nella storia"""
    for node in story_data:
        if node.get('node_id') == node_id:
            return node
    return {}

def reset_game():
    """Resetta il gioco allo stato iniziale"""
    for key in ['current_node', 'story_history', 'choices_made', 'choice_order_seed']:
        if key in st.session_state:
            del st.session_state[key]
    
    st.session_state.current_node = 'start'
    st.session_state.story_history = []
    st.session_state.choices_made = []
    st.session_state.choice_order_seed = random.randint(1, 1000000)

def shuffle_choices(choices: List[Dict], seed: int) -> List[Dict]:
    """Mescola le scelte mantenendo traccia dell'ordine originale"""
    choices_with_index = [(i, choice) for i, choice in enumerate(choices)]
    random.seed(seed + hash(str(choices)))
    random.shuffle(choices_with_index)
    random.seed()
    return [choice for _, choice in choices_with_index]

def make_choice(next_node: str, choice_text: str):
    """Gestisce la scelta dell'utente"""
    st.session_state.choices_made.append({
        'from_node': st.session_state.current_node,
        'choice': choice_text,
        'to_node': next_node
    })
    st.session_state.current_node = next_node

def display_progress_bar():
    """Mostra una barra di progresso basata sul numero di scelte fatte"""
    if st.session_state.choices_made:
        progress = min(len(st.session_state.choices_made) * 10, 100)
        st.markdown(f"""
        <div class="progress-container slide-in">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
            <p style="text-align: center; color: #ffd700; font-family: 'Cinzel', serif; margin-top: 10px; font-size: 0.95rem;">
                ⚡ Progresso: {len(st.session_state.choices_made)} decisioni
            </p>
        </div>
        """, unsafe_allow_html=True)

# Restituisce un'icona diversa per ogni scelta
def get_choice_icon(index: int) -> str:
    icons = [
        "⚔️", "🛡️", "🏃‍♂️", "🧠", "💎", "🗝️", "🔍", "💀", 
        "🌟", "🔥", "❄️", "⚡", "🌙", "☀️", "🌊", "🍃",
        "🎭", "🏰", "🗡️", "🏹", "🪄", "📜", "🔮", "⚖️"
    ]
    return icons[index % len(icons)]


def save_adventure_log():
    """Crea un log completo dell'avventura e lo salva in locale"""
    from datetime import datetime
    import json
    
    # Genera timestamp per il nome del file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Raccoglie tutti i dati dell'avventura
    adventure_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "completion_date": datetime.now().strftime("%d/%m/%Y alle %H:%M"),
            "total_choices": len(st.session_state.choices_made),
            "final_outcome": "Vittoria" if st.session_state.current_node == 'victory' else "Game Over" if st.session_state.current_node == 'game_over' else "In corso"
        },
        "original_input": getattr(st.session_state, 'original_user_input', 'Input originale non disponibile'),
        "generated_lore": st.session_state.generated_lore,
        "story_path": st.session_state.choices_made,
        "final_node": st.session_state.current_node
    }
    
    # Carica la storia completa per i dettagli
    try:
        story_data = load_story()
        adventure_data["story_details"] = story_data
    except:
        adventure_data["story_details"] = []
    
    # Crea il log in formato JSON
    filename = f"avventura_{timestamp}.json"
    filepath = Path("salvataggi") / filename
    
    # Crea la cartella se non esiste
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(adventure_data, f, indent=2, ensure_ascii=False)
    
    return filepath, adventure_data

def create_adventure_report(adventure_data):
    """Crea un report leggibile dell'avventura"""
    report_lines = []
    
    # Header del report
    report_lines.append("🎭 CRONACHE DELLA LEGGENDA VISSUTA 🎭")
    report_lines.append("=" * 60)
    report_lines.append(f"📅 Completata il: {adventure_data['metadata']['completion_date']}")
    report_lines.append(f"🎯 Esito finale: {adventure_data['metadata']['final_outcome']}")
    report_lines.append(f"⚔️ Decisioni totali: {adventure_data['metadata']['total_choices']}")
    report_lines.append("")
    
    # Input originale
    report_lines.append("📝 LA TUA VISIONE ORIGINALE:")
    report_lines.append("-" * 40)
    report_lines.append(adventure_data['original_input'])
    report_lines.append("")
    
    # Lore generata (estratto)
    if adventure_data['generated_lore']:
        lore_text = str(adventure_data['generated_lore'])
        lore_preview = lore_text[:300] + "..." if len(lore_text) > 300 else lore_text
        report_lines.append("🏰 MONDO CREATO:")
        report_lines.append("-" * 40)
        report_lines.append(lore_preview)
        report_lines.append("")
    
    # Percorso delle scelte
    report_lines.append("🛤️ IL TUO CAMMINO EROICO:")
    report_lines.append("-" * 40)
    
    for i, choice in enumerate(adventure_data['story_path'], 1):
        report_lines.append(f"⚡ Atto {i:2d}: {choice['choice']}")
    
    if not adventure_data['story_path']:
        report_lines.append("Nessuna scelta registrata")
    
    report_lines.append("")
    report_lines.append("✨ Fine delle Cronache ✨")
    
    return "\n".join(report_lines)

def download_adventure_files(adventure_data, filepath):
    """Prepara i file per il download"""
    import zipfile
    from io import BytesIO
    
    # Crea un archivio ZIP in memoria
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Aggiungi il file JSON completo
        zip_file.writestr(f"{filepath.stem}.json", 
                         json.dumps(adventure_data, indent=2, ensure_ascii=False))
        
        # Aggiungi il report leggibile
        report_content = create_adventure_report(adventure_data)
        zip_file.writestr(f"{filepath.stem}_report.txt", report_content)
        
        # Aggiungi un file markdown formattato
        markdown_content = create_markdown_report(adventure_data)
        zip_file.writestr(f"{filepath.stem}_report.md", markdown_content)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

def create_markdown_report(adventure_data):
    """Crea un report in formato Markdown"""
    md_lines = []
    
    md_lines.append("# 🎭 Cronache della Leggenda Vissuta")
    md_lines.append("")
    md_lines.append("## 📊 Informazioni Generali")
    md_lines.append(f"- **Completata il**: {adventure_data['metadata']['completion_date']}")
    md_lines.append(f"- **Esito finale**: {adventure_data['metadata']['final_outcome']}")
    md_lines.append(f"- **Decisioni totali**: {adventure_data['metadata']['total_choices']}")
    md_lines.append("")
    
    md_lines.append("## 📝 La Tua Visione Originale")
    md_lines.append("```")
    md_lines.append(adventure_data['original_input'])
    md_lines.append("```")
    md_lines.append("")
    
    if adventure_data['story_path']:
        md_lines.append("## 🛤️ Il Tuo Cammino Eroico")
        for i, choice in enumerate(adventure_data['story_path'], 1):
            md_lines.append(f"{i}. **{choice['choice']}**")
            md_lines.append(f"   - *Da: {choice['from_node']} → A: {choice['to_node']}*")
            md_lines.append("")
    
    md_lines.append("---")
    md_lines.append("*Generato dal Maestro delle Leggende*")
    
    return "\n".join(md_lines)

# Renderizza la fase di gameplay

def render_gameplay():
    # Carica i dati della storia
    story_data = load_story()
    if not story_data:
        st.error("❌ Impossibile caricare la storia. Torna alla fase di creazione.")
        if st.button("🔄 Torna alla Creazione", key="back_to_creation"):
            st.session_state.app_state = AppState.CREATION
            st.rerun()
        return
    
    # Sidebar per il gameplay
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-content">
            <h2 style="color: #ffd700; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1rem; font-size: 1.4rem;">
                ⚔️ PANNELLO AVVENTURA ⚔️
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Ricomincia Avventura", key="new_adventure", use_container_width=True):
            reset_game()
            st.rerun()
        
        if st.button("🏠 Crea una nuova storia", key="back_to_creation_from_game", use_container_width=True):
            # Reset completo dell'applicazione
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        # Cronologia delle scelte
        if st.session_state.choices_made:
            st.markdown("""
            <div class="sidebar-content">
                <h3 style="color: #ffd700; font-family: 'Cinzel', serif; text-align: center; font-size: 1.2rem;">
                    📚 CRONACHE
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            display_progress_bar()
            
            with st.expander("📖 Le tue gesta", expanded=False):
                for i, choice in enumerate(st.session_state.choices_made, 1):
                    st.markdown(f"""
                    <div style="background: rgba(0, 0, 0, 0.7); border-left: 4px solid #ffd700; padding: 1rem; margin: 0.8rem 0; border-radius: 0 10px 10px 0; font-family: 'Crimson Text', serif; color: #f0f0f0;">
                        <strong style="color: #ffd700; font-size: 1rem;">Atto {i}:</strong><br>
                        <em style="font-size: 0.9rem; line-height: 1.3;">{choice['choice'][:60]}{'...' if len(choice['choice']) > 60 else ''}</em>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sidebar-content">
                <h3 style="color: #ffd700; font-family: 'Cinzel', serif; text-align: center; font-size: 1.2rem;">
                    🌟 LA TUA AVVENTURA INIZIA 🌟
                </h3>
                <p style="text-align: center; color: #f0f0f0; font-style: italic; margin-top: 0.8rem; font-size: 0.9rem;">
                    Le tue gesta appariranno qui...
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Istruzioni
        st.markdown("""
        <div style="background: rgba(255, 215, 0, 0.15); border: 2px solid rgba(255, 215, 0, 0.4); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; font-family: 'Crimson Text', serif;">
            <h3 style="color: #ffd700; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1rem; font-size: 1.2rem;">🗡️ REGOLE</h3>
            <ul style="list-style: none; padding: 0; font-size: 0.9rem;">
                <li style="margin: 0.6rem 0;">📖 Immergiti nel racconto</li>
                <li style="margin: 0.6rem 0;">🤔 Ogni scelta conta</li>
                <li style="margin: 0.6rem 0;">⚡ Solo UNA via alla gloria</li>
                <li style="margin: 0.6rem 0;">🔄 Scelte riorganizzate ogni partita</li>
                <li style="margin: 0.6rem 0;">🏆 Conquista l'immortalità</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
        st.markdown("---")
        
        # Opzione di salvataggio in qualsiasi momento
        if st.session_state.choices_made:  # Solo se ci sono scelte fatte
            st.markdown("""
            <div style="background: rgba(0, 184, 148, 0.15); border: 2px solid rgba(0, 184, 148, 0.4); border-radius: 15px; padding: 1.5rem; margin: 1rem 0; font-family: 'Crimson Text', serif;">
                <h3 style="color: #00b894; font-family: 'Cinzel', serif; text-align: center; margin-bottom: 1rem; font-size: 1.2rem;">💾 SALVATAGGIO</h3>
                <p style="text-align: center; color: #f0f0f0; font-size: 0.9rem; margin-bottom: 1rem;">
                    Salva il progresso attuale della tua avventura
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💾 Salva Avventura", key="save_current_progress", use_container_width=True):
                try:
                    filepath, adventure_data = save_adventure_log()
                    zip_data = download_adventure_files(adventure_data, filepath)
                    
                    st.success("✅ Avventura salvata!")
                    
                    st.download_button(
                        label="📥 Scarica",
                        data=zip_data,
                        file_name=f"avventura_in_corso_{filepath.stem}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Errore: {e}")


    # Contenuto principale del gioco
    current_node = find_node_by_id(story_data, st.session_state.current_node)
    
    if not current_node:
        st.error("⚠️ Errore: capitolo della leggenda non trovato!")
        return
    
    # Contenitore principale della storia
    st.markdown('<div class="story-container fade-in">', unsafe_allow_html=True)
    
    # Mostra il testo della storia
    st.markdown(f'<div class="story-text">{current_node.get("description", "")}</div>', 
                unsafe_allow_html=True)
    
    # Gestisci i diversi tipi di nodi
    choices = current_node.get('choices', [])
    
    if not choices:
        # Nodo finale (vittoria)
        if not choices and st.session_state.current_node != 'game_over':
            # Schermata di vittoria semplificata
            st.balloons()  # Effetto palloncini di Streamlit
                        
                        # Messaggio finale
            st.markdown("""
            <div style="
                background: linear-gradient(45deg, #ffd700, #ff6b6b);
                color: white;
                padding: 2rem;
                border-radius: 20px;
                text-align: center;
                margin: 2rem 0;
                border: 2px solid #ffffff;
            ">
                <h4 style="margin-bottom: 1rem; font-family: 'Cinzel', serif;">
                    🏛️ IL TUO NOME NEGLI ANNALI DELL'ETERNITÀ 🏛️
                </h4>
                <p style="font-size: 1.1rem; font-style: italic;">
                    "Nei tempi che verranno, i cantastorie narreranno delle tue gesta.<br>
                    Il tuo coraggio risuonerà attraverso i secoli, Campione delle Scelte Sagge!"
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Emojis finali
            st.markdown("""
            <div style="text-align: center; font-size: 2rem; margin: 2rem 0;">
                🎉 ✨ 🎊 ⭐ 🌟 💫 🏆 👑
            </div>
            """, unsafe_allow_html=True)

            # Statistiche della vittoria
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.9); 
                    border-radius: 15px; 
                    padding: 2rem; 
                    margin: 2rem 0;
                    color: #333333;
                    text-align: center;
                ">
                    <h3 style="color: #ffd700; margin-bottom: 1rem; font-family: 'Cinzel', serif;">
                        📊 STATISTICHE DELLA GLORIA 📊
                    </h3>
                    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        ⚔️ Decisioni Magistrali: <strong style="color: #ff6b6b; font-size: 1.4rem;">{len(st.session_state.choices_made)}</strong>
                    </p>
                    <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        🎯 Tasso di Successo: <strong style="color: #00b894; font-size: 1.4rem;">100%</strong>
                    </p>
                    <p style="font-size: 1.2rem;">
                        👑 Titolo Conquistato: <strong style="color: #a29bfe; font-size: 1.4rem;">LEGGENDA IMMORTALE</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Opzioni di gioco        
        # Opzioni post-vittoria
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 SALVA LE CRONACHE DELLA GLORIA", key="save_victory_adventure", use_container_width=True):
                try:
                    filepath, adventure_data = save_adventure_log()
                    zip_data = download_adventure_files(adventure_data, filepath)
                    
                    st.markdown("""
                    <div class="status-success">
                        📚 Le tue gesta eroiche sono state immortalate negli annali!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Bottone per il download
                    st.download_button(
                        label="📥 Scarica Archivio Completo",
                        data=zip_data,
                        file_name=f"cronache_vittoria_{filepath.stem}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                    # Anteprima del report
                    with st.expander("👁️ Anteprima delle Cronache", expanded=False):
                        report_preview = create_adventure_report(adventure_data)
                        st.text(report_preview[:1000] + "..." if len(report_preview) > 1000 else report_preview)
                        
                except Exception as e:
                    st.error(f"⚠️ Errore nel salvataggio delle cronache: {e}")
        
        with col2:
            if st.button("🌟 Forgia una Nuova Leggenda", key="play_again_victory", use_container_width=True):
                reset_game()
                st.rerun()
    
    elif st.session_state.current_node == 'game_over':
        # Schermata di game over
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff416c, #ff4757, #c44569, #8e44ad); background-size: 300% 300%; color: white; padding: 3rem; border-radius: 25px; text-align: center; margin: 2rem 0; animation: backgroundShift 3s ease-in-out infinite;">
            <h2 style="font-family: 'Cinzel', serif; font-size: 2.5rem; margin-bottom: 1.5rem;">
                ⚰️ LA LEGGENDA SI INTERROMPE ⚰️
            </h2>
            <p style="font-size: 1.3rem; margin-bottom: 1.5rem; font-weight: 600;">
                Il fato ha scritto un epilogo diverso per la tua saga...
            </p>
            <p style="font-size: 1.1rem; color: rgba(255,255,255,0.95); margin-bottom: 1rem;">
                Hai intessuto <strong style="color: #ff6b6b;">{len(st.session_state.choices_made)}</strong> atti prima che il destino calasse il sipario.
            </p>
            <p style="font-size: 1rem; margin-top: 2rem; font-style: italic; color: rgba(255,255,255,0.9);">
                Ma ogni grande eroe può riscrivere la propria storia! 🔥
            </p>
        </div>
        """, unsafe_allow_html=True)
        

        # Opzioni di salvataggio anche per game over
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 SALVA LE CRONACHE DEL TENTATIVO", key="save_gameover_adventure", use_container_width=True):
                try:
                    filepath, adventure_data = save_adventure_log()
                    zip_data = download_adventure_files(adventure_data, filepath)
                    
                    st.markdown("""
                    <div class="status-success">
                        📚 Anche i tentativi coraggiosi meritano di essere ricordati!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Bottone per il download
                    st.download_button(
                        label="📥 Scarica Archivio del Tentativo",
                        data=zip_data,
                        file_name=f"cronache_tentativo_{filepath.stem}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                        
                except Exception as e:
                    st.error(f"⚠️ Errore nel salvataggio: {e}")
        
        st.markdown("---")

        # Mostra le scelte disponibili
        shuffled_choices = shuffle_choices(choices, st.session_state.choice_order_seed)
        
        for i, choice in enumerate(shuffled_choices):
            icon = get_choice_icon(i)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"{icon} {choice['text']}", key=f"choice_gameover_{i}", use_container_width=True):
                    if choice.get('next_node') == 'start' or 'ricomincia' in choice['text'].lower():
                        reset_game()
                    else:
                        make_choice(choice['next_node'], choice['text'])
                    st.rerun()
    
    else:
        # Nodo normale con scelte
        st.markdown("""
        <div style="text-align: center; font-family: 'Cinzel', serif; font-size: 1.8rem; background: linear-gradient(45deg, #ffd700, #ff6b6b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 1.5rem 0; animation: pulse 2s infinite;">
            🎯 Il Destino Attende la Tua Decisione 🎯
        </div>
        """, unsafe_allow_html=True)
        
        # Mescola le scelte
        shuffled_choices = shuffle_choices(choices, st.session_state.choice_order_seed + hash(st.session_state.current_node))
        
        # Crea le scelte
        for i, choice in enumerate(shuffled_choices):
            icon = get_choice_icon(i)
            
            if st.button(f"{icon} {choice['text']}", key=f"choice_{st.session_state.current_node}_{i}", use_container_width=True):
                make_choice(choice['next_node'], choice['text'])
                time.sleep(0.1)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; color: rgba(255, 215, 0, 0.8); font-family: 'Cinzel', serif; font-style: italic; margin-top: 3rem; padding: 2.5rem; border-top: 2px solid rgba(255, 215, 0, 0.4); background: rgba(0,0,0,0.3); border-radius: 20px 20px 0 0;">
        <p style="font-size: 1.2rem; margin-bottom: 1rem;">⭐ Che la saggezza illumini il tuo cammino, Maestro del Destino! ⭐</p>
        <p style="font-size: 0.95rem; opacity: 0.8; margin-bottom: 0.5rem;">Ogni scelta è un pennello che dipinge il tuo futuro...</p>
        <p style="font-size: 0.85rem; opacity: 0.6;">🎲 Le opzioni si riorganizzano ad ogni nuova avventura 🎲</p>
    </div>
    """, unsafe_allow_html=True)

def main():

    initialize_app_state()
    
    # Header principale
    st.markdown('<h1 class="main-header fade-in">🎭 MAESTRO DELLE LEGGENDE 🎭</h1>', unsafe_allow_html=True)
    
    # Routing basato sullo stato dell'app
    if st.session_state.app_state == AppState.CREATION:
        render_creation_phase()
    elif st.session_state.app_state == AppState.LORE_REVIEW:
        render_lore_review()
    elif st.session_state.app_state == AppState.VALIDATION:
        render_validation_phase()
    elif st.session_state.app_state == AppState.PLAN_REVIEW:
        render_plan_review()
    elif st.session_state.app_state == AppState.STORY_GENERATION:
        render_story_generation()
    elif st.session_state.app_state == AppState.GAMEPLAY:
        render_gameplay()

if __name__ == "__main__":
    main()