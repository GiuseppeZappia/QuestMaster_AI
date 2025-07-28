import streamlit as st
import json
from pathlib import Path
from typing import Dict, List, Any
import time
import random
import base64
import re
from io import BytesIO
from datetime import datetime
import zipfile

# Importa le librerie TTS se disponibili
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
    page_title="Avventura Interattiva",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizzato 
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Creepster&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 20% 80%, #0c0c0c 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    /* Effetto stelle animate di sfondo */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #ffd700, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #ffd700, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(2px 2px at 160px 30px, #ffd700, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes sparkle {
        from { transform: translateY(0px); }
        to { transform: translateY(-100px); }
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #ffd700, #ffed4e, #ff6b6b, #4ecdc4, #ffd700);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Cinzel', serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
        animation: glow 2s ease-in-out infinite alternate, gradientShift 5s ease-in-out infinite;
        letter-spacing: 4px;
        position: relative;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.4) 50%, transparent 70%);
        animation: shine 3s infinite;
        pointer-events: none;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 20px rgba(255, 215, 0, 0.5), 0 0 30px rgba(255, 215, 0, 0.3); }
        to { text-shadow: 0 0 30px rgba(255, 215, 0, 1), 0 0 50px rgba(255, 215, 0, 0.7); }
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) skewX(-15deg); }
        100% { transform: translateX(200%) skewX(-15deg); }
    }
    
    .story-container {
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(15px);
        border: 3px solid transparent;
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1rem auto;
        max-width: 1000px;
        box-shadow: 
            0 0 60px rgba(255, 215, 0, 0.3),
            inset 0 0 60px rgba(255, 255, 255, 0.08),
            0 20px 40px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
        transform: perspective(1000px) rotateX(2deg);
        transition: all 0.3s ease;
    }
    
    .story-container:hover {
        transform: perspective(1000px) rotateX(0deg) scale(1.01);
        box-shadow: 
            0 0 80px rgba(255, 215, 0, 0.4),
            inset 0 0 80px rgba(255, 255, 255, 0.1),
            0 30px 60px rgba(0,0,0,0.6);
    }
    
    .story-container::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, #ffd700, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #e17055, #ffd700);
        background-size: 400% 400%;
        border-radius: 25px;
        z-index: -1;
        animation: borderGlow 4s ease-in-out infinite;
    }
    
    @keyframes borderGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .story-text {
        font-family: 'Crimson Text', serif;
        font-size: 1.3rem;
        line-height: 1.8;
        color: #f0f0f0;
        text-align: justify;
        margin-bottom: 2rem;
        text-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
        position: relative;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        border-left: 5px solid #ffd700;
        box-shadow: inset 0 0 30px rgba(255, 215, 0, 0.1);
    }
    
    .story-text::first-letter {
        font-size: 4rem;
        font-weight: bold;
        float: left;
        line-height: 3rem;
        margin: 0.3rem 0.8rem 0 0;
        color: #ffd700;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
        font-family: 'Cinzel', serif;
    }
    
    .choices-header {
        text-align: center;
        font-family: 'Cinzel', serif;
        font-size: 1.8rem;
        background: linear-gradient(45deg, #ffd700, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1.5rem 0;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.7);
        position: relative;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .choices-header::before,
    .choices-header::after {
        content: '⚔️';
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.5rem;
        animation: rotate 4s linear infinite;
    }
    
    .choices-header::before { left: -3rem; }
    .choices-header::after { 
        right: -3rem; 
        animation-direction: reverse;
    }
    
    @keyframes rotate {
        from { transform: translateY(-50%) rotate(0deg); }
        to { transform: translateY(-50%) rotate(360deg); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #667eea 75%, #764ba2 100%);
        background-size: 300% 300%;
        color: white;
        border: 3px solid rgba(255, 255, 255, 0.3);
        padding: 1.2rem 1.8rem;
        margin: 0.8rem 0;
        border-radius: 20px;
        font-size: 1.1rem;
        font-family: 'Crimson Text', serif;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 10px 30px rgba(0,0,0,0.4),
            inset 0 2px 0 rgba(255,255,255,0.3),
            0 0 20px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%;
        min-height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: backgroundShift 3s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.5),
            0 0 40px rgba(255, 215, 0, 0.5),
            inset 0 2px 0 rgba(255,255,255,0.4);
        border-color: #ffd700;
        background: linear-gradient(135deg, #ffd700 0%, #ff6b6b 25%, #4ecdc4 50%, #45b7d1 75%, #ffd700 100%);
        background-size: 300% 300%;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-4px) scale(1.01);
    }
    
    .sidebar-content {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 
            0 10px 30px rgba(0,0,0,0.4),
            inset 0 0 40px rgba(255, 215, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .sidebar-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.1), transparent);
        animation: sidebarShine 4s infinite;
    }
    
    @keyframes sidebarShine {
        0% { left: -100%; }
        50% { left: 100%; }
        100% { left: -100%; }
    }
    
    .game-over {
        background: linear-gradient(135deg, #ff416c, #ff4757, #c44569, #8e44ad);
        background-size: 300% 300%;
        color: white;
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 
            0 0 60px rgba(255, 65, 108, 0.5),
            inset 0 0 60px rgba(255, 255, 255, 0.15),
            0 20px 40px rgba(0,0,0,0.5);
        border: 3px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        animation: backgroundShift 3s ease-in-out infinite;
    }
    
    .game-over::before {
        content: '💀';
        position: absolute;
        font-size: 10rem;
        opacity: 0.15;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(-50%, -50%) rotate(-5deg) scale(1); }
        33% { transform: translate(-50%, -60%) rotate(0deg) scale(1.1); }
        66% { transform: translate(-50%, -40%) rotate(5deg) scale(0.9); }
    }
    
    .victory {
        background: linear-gradient(135deg, #00b894, #00cec9, #74b9ff, #a29bfe);
        background-size: 300% 300%;
        color: white;
        padding: 3rem;
        border-radius: 25px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 
            0 0 60px rgba(0, 184, 148, 0.5),
            inset 0 0 60px rgba(255, 255, 255, 0.15),
            0 20px 40px rgba(0,0,0,0.5);
        border: 3px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
        animation: backgroundShift 3s ease-in-out infinite;
    }
    
    .victory::before {
        content: '👑';
        position: absolute;
        font-size: 8rem;
        opacity: 0.2;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        animation: crown 3s ease-in-out infinite;
    }
    
    @keyframes crown {
        0%, 100% { transform: translate(-50%, -50%) scale(1) rotate(-5deg); }
        33% { transform: translate(-50%, -50%) scale(1.2) rotate(0deg); }
        66% { transform: translate(-50%, -50%) scale(0.9) rotate(5deg); }
    }
    
    .progress-container {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        padding: 10px;
        margin: 1rem 0;
        border: 2px solid rgba(255, 215, 0, 0.4);
        box-shadow: 
            inset 0 0 30px rgba(0,0,0,0.5),
            0 0 20px rgba(255, 215, 0, 0.3);
    }
    
    .progress-bar {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        overflow: hidden;
        height: 20px;
        position: relative;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #ffd700, #ffed4e, #ff6b6b, #4ecdc4, #ffd700);
        background-size: 200% 200%;
        height: 100%;
        transition: width 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        border-radius: 15px;
        box-shadow: 
            0 0 30px rgba(255, 215, 0, 0.7),
            inset 0 0 20px rgba(255,255,255,0.3);
        position: relative;
        overflow: hidden;
        animation: progressGlow 2s infinite;
    }
    
    @keyframes progressGlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .progress-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.5) 50%, transparent 70%);
        animation: shine 2.5s infinite;
    }
    
    .choice-history {
        background: rgba(0, 0, 0, 0.7);
        border-left: 4px solid #ffd700;
        padding: 1rem;
        margin: 0.8rem 0;
        border-radius: 0 10px 10px 0;
        font-family: 'Crimson Text', serif;
        color: #f0f0f0;
        position: relative;
        transition: all 0.4s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        font-size: 0.9rem;
    }
    
    .choice-history:hover {
        background: rgba(255, 215, 0, 0.15);
        transform: translateX(10px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    
    .choice-history::before {
        content: '📜';
        position: absolute;
        left: -15px;
        top: 50%;
        transform: translateY(-50%);
        background: rgba(0, 0, 0, 0.9);
        padding: 5px;
        border-radius: 50%;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
        font-size: 0.8rem;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, rgba(0,0,0,0.95) 0%, rgba(26,26,46,0.95) 100%);
    }
    
    .stSidebar .stMarkdown {
        color: #f0f0f0;
    }
    
    .instructions {
        background: rgba(255, 215, 0, 0.15);
        border: 2px solid rgba(255, 215, 0, 0.4);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Crimson Text', serif;
        box-shadow: 
            inset 0 0 30px rgba(255, 215, 0, 0.1),
            0 0 20px rgba(255, 215, 0, 0.2);
    }
    
    .instructions h3 {
        color: #ffd700;
        font-family: 'Cinzel', serif;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .instructions ul {
        font-size: 0.9rem;
    }
    
    .instructions li {
        margin: 0.6rem 0;
    }
    
    .save-section {
        background: rgba(0, 184, 148, 0.15);
        border: 2px solid rgba(0, 184, 148, 0.4);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        font-family: 'Crimson Text', serif;
    }
    
    .save-section h3 {
        color: #00b894;
        font-family: 'Cinzel', serif;
        text-align: center;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .status-success {
        background: rgba(0, 184, 148, 0.2);
        border: 2px solid rgba(0, 184, 148, 0.6);
        color: #55efc4;
        padding: 1rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        font-family: 'Crimson Text', serif;
        font-weight: 600;
        animation: statusGlow 2s infinite alternate;
    }
    
    @keyframes statusGlow {
        from { box-shadow: 0 0 20px rgba(0, 184, 148, 0.3); }
        to { box-shadow: 0 0 40px rgba(0, 184, 148, 0.6); }
    }
    
    .footer {
        text-align: center;
        color: rgba(255, 215, 0, 0.8);
        font-family: 'Cinzel', serif;
        font-style: italic;
        margin-top: 3rem;
        padding: 2.5rem;
        border-top: 2px solid rgba(255, 215, 0, 0.4);
        background: rgba(0,0,0,0.3);
        border-radius: 20px 20px 0 0;
    }
    
    /* Animazioni per l'ingresso degli elementi */
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-in {
        animation: slideIn 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-50px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Nuovi bottoni del reset */
    .reset-button {
        background: linear-gradient(135deg, #e74c3c, #c0392b, #8e44ad, #9b59b6) !important;
        background-size: 300% 300% !important;
        animation: backgroundShift 3s ease-in-out infinite !important;
    }
    
    .reset-button:hover {
        background: linear-gradient(135deg, #ff6b6b, #ee5a52, #a55eea, #fd79a8) !important;
        transform: translateY(-5px) scale(1.05) !important;
    }

    /* Stili per contenitori compatti */
    .compact-sidebar-header {
        color: #ffd700; 
        font-family: 'Cinzel', serif; 
        text-align: center; 
        margin-bottom: 1rem; 
        font-size: 1.4rem;
        font-weight: 600;
    }

    .compact-progress-text {
        text-align: center; 
        color: #ffd700; 
        font-family: 'Cinzel', serif; 
        margin-top: 10px; 
        font-size: 0.95rem;
    }

    .compact-sidebar-message {
        color: #ffd700; 
        font-family: 'Cinzel', serif; 
        text-align: center; 
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .compact-sidebar-submessage {
        text-align: center; 
        color: #f0f0f0; 
        font-style: italic; 
        margin-top: 0.8rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

def detect_story_tone(story_text):
    """
    Analizza il tono della storia per adattare la voce TTS
    """
    if not story_text:
        return "neutral"
    
    text_lower = str(story_text).lower()
    
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
            
            # Legge il file
            try:
                with open(temp_file, 'rb') as f:
                    audio_data = f.read()
                import os
                os.remove(temp_file)  # Pulisce il file temporaneo
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

def save_adventure_log():
    """Crea un log completo dell'avventura e lo salva in locale"""
    
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
    
    if adventure_data['story_path']:
        md_lines.append("## 🛤️ Il Tuo Cammino Eroico")
        for i, choice in enumerate(adventure_data['story_path'], 1):
            md_lines.append(f"{i}. **{choice['choice']}**")
            md_lines.append(f"   - *Da: {choice['from_node']} → A: {choice['to_node']}*")
            md_lines.append("")
    
    md_lines.append("---")
    md_lines.append("*Generato dal Maestro delle Leggende*")
    
    return "\n".join(md_lines)

def download_adventure_files(adventure_data, filepath):
    """Prepara i file per il download"""
    
    # Crea un archivio ZIP in memoria
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Aggiunge il file JSON completo
        zip_file.writestr(f"{filepath.stem}.json", 
                         json.dumps(adventure_data, indent=2, ensure_ascii=False))
        
        # Aggiunge il report leggibile
        report_content = create_adventure_report(adventure_data)
        zip_file.writestr(f"{filepath.stem}_report.txt", report_content)
        
        # Aggiunge un file markdown formattato
        markdown_content = create_markdown_report(adventure_data)
        zip_file.writestr(f"{filepath.stem}_report.md", markdown_content)
    
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

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

def initialize_game_state():
    """Inizializza lo stato del gioco"""
    if 'current_node' not in st.session_state:
        st.session_state.current_node = 'start'
    if 'story_history' not in st.session_state:
        st.session_state.story_history = []
    if 'choices_made' not in st.session_state:
        st.session_state.choices_made = []
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'choice_order_seed' not in st.session_state:
        st.session_state.choice_order_seed = random.randint(1, 1000000)

def reset_game():
    """Resetta il gioco allo stato iniziale"""
    # Pulisce tutti gli audio in cache prima del reset
    keys_to_remove = []
    for key in st.session_state.keys():
        if (key.startswith('audio_') or 
            key.startswith('tone_') or 
            key.startswith('last_text_')):
            keys_to_remove.append(key)
    
    # Rimuove tutte le chiavi audio dalla cache
    for key in keys_to_remove:
        del st.session_state[key]
    
    # Azzera TUTTO lo stato del gioco - forza il reset completo
    for key in ['current_node', 'story_history', 'choices_made', 'game_started', 'choice_order_seed']:
        if key in st.session_state:
            del st.session_state[key]
    
    # Re-inizializza con valori puliti
    st.session_state.current_node = 'start'
    st.session_state.story_history = []  # Lista vuota garantita
    st.session_state.choices_made = []   # Lista vuota garantita 
    st.session_state.game_started = True
    st.session_state.choice_order_seed = random.randint(1, 1000000)

def shuffle_choices(choices: List[Dict], seed: int) -> List[Dict]:
    """Mescola le scelte mantenendo traccia dell'ordine originale"""
    # Crea una copia delle scelte con indice originale
    choices_with_index = [(i, choice) for i, choice in enumerate(choices)]
    
    # Usa il seed per ottenere sempre lo stesso ordine per lo stesso nodo
    random.seed(seed + hash(str(choices)))
    random.shuffle(choices_with_index)
    
    # Ripristina il generatore random
    random.seed()
    
    return [choice for _, choice in choices_with_index]

def make_choice(next_node: str, choice_text: str):
    """Gestisce la scelta dell'utente"""
    # Aggiunge la scelta alla cronologia
    st.session_state.choices_made.append({
        'from_node': st.session_state.current_node,
        'choice': choice_text,
        'to_node': next_node
    })
    
    # Aggiorna il nodo corrente
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
            <p class="compact-progress-text">
                ⚡ Progresso: {len(st.session_state.choices_made)} decisioni
            </p>
        </div>
        """, unsafe_allow_html=True)

def get_choice_icon(index: int) -> str:
    """Restituisce un'icona diversa per ogni scelta"""
    icons = [
        "⚔️", "🛡️", "🏃‍♂️", "🧠", "💎", "🗝️", "🔍", "💀", 
        "🌟", "🔥", "❄️", "⚡", "🌙", "☀️", "🌊", "🍃",
        "🎭", "🏰", "🗡️", "🏹", "🪄", "📜", "🔮", "⚖️"
    ]
    return icons[index % len(icons)]

def main():
    # Carica i dati della storia
    story_data = load_story()
    if not story_data:
        return
    
    # Inizializza lo stato del gioco
    initialize_game_state()
    
    # Header principale con effetto ancora più drammatico
    st.markdown('<h1 class="main-header fade-in">🎭 AVVENTURA INTERATTIVA EPICA 🎭</h1>', unsafe_allow_html=True)
    
    # Sidebar con design ultra-migliorato e gestione spazio ottimizzata
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-content">
            <h2 class="compact-sidebar-header">
                ⚔️ QUESTMASTER ⚔️
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Mostra la cronologia delle scelte e controlla se ci sono effettivamente scelte per mostrare il progresso
        if st.session_state.choices_made:
            st.markdown("""
            <div class="sidebar-content">
                <h3 class="compact-sidebar-header">
                    📚 CRONACHE
                </h3>
            </div>
            """, unsafe_allow_html=True)
            
            display_progress_bar()
            
            with st.expander("📖 Le tue gesta", expanded=False):
                for i, choice in enumerate(st.session_state.choices_made, 1):
                    st.markdown(f"""
                    <div class="choice-history">
                        <strong style="color: #ffd700; font-size: 1rem;">Atto {i}:</strong><br>
                        <em style="font-size: 0.9rem; line-height: 1.3;">{choice['choice'][:60]}{'...' if len(choice['choice']) > 60 else ''}</em>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            # Mostra un messaggio quando non ci sono ancora scelte
            st.markdown("""
            <div class="sidebar-content">
                <h3 class="compact-sidebar-message">
                    🌟 LA TUA AVVENTURA INIZIA 🌟
                </h3>
                <p class="compact-sidebar-submessage">
                    Le tue gesta appariranno qui...
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Istruzioni 
        st.markdown("""
        <div class="instructions">
            <h3>🗡️ REGOLE</h3>
            <ul style="list-style: none; padding: 0;">
                <li>📖 Immergiti nel racconto</li>
                <li>🤔 Ogni scelta conta</li>
                <li>⚡ Solo UNA via alla gloria</li>
                <li>🔄 Scelte riorganizzate ogni partita</li>
                <li>🏆 Conquista l'immortalità</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Opzione di salvataggio in qualsiasi momento
        if st.session_state.choices_made:  # Solo se ci sono scelte fatte
            st.markdown("""
            <div class="save-section">
                <h3>💾 SALVATAGGIO</h3>
                <p style="text-align: center; color: #f0f0f0; font-size: 0.9rem; margin-bottom: 1rem;">
                    Salva il progresso attuale della tua avventura
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("💾 Salva Avventura", key="save_current_progress", use_container_width=True):
                try:
                    filepath, adventure_data = save_adventure_log()
                    zip_data = download_adventure_files(adventure_data, filepath)
                    
                    st.markdown("""
                    <div class="status-success">
                        ✅ Avventura salvata!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 Scarica",
                        data=zip_data,
                        file_name=f"avventura_in_corso_{filepath.stem}.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Errore: {e}")

    # Trova il nodo corrente
    current_node = find_node_by_id(story_data, st.session_state.current_node)
    
    if not current_node:
        st.error("⚠️ Errore: capitolo della leggenda non trovato!")
        return
    
    # Contenitore principale della storia con animazione migliorata
    st.markdown('<div class="story-container fade-in">', unsafe_allow_html=True)
    
    # Genera e mostra il player audio per il testo della storia
    story_text = current_node.get("description", "")
    
    # Controlla se TTS è disponibile
    if GTTS_AVAILABLE or PYTTSX3_AVAILABLE:
        # Genera audio se non esiste o se il testo è cambiato
        cache_key = f"audio_{st.session_state.current_node}"
        if (cache_key not in st.session_state or 
            f'last_text_{st.session_state.current_node}' not in st.session_state or 
            st.session_state[f'last_text_{st.session_state.current_node}'] != story_text):
            
            with st.spinner("🎵 Il narratore sta preparando la sua voce magica... ✨"):
                tone = detect_story_tone(story_text)
                audio_data = generate_tts_audio(story_text, tone)
                
                if audio_data:
                    st.session_state[cache_key] = audio_data
                    st.session_state[f'tone_{st.session_state.current_node}'] = tone
                    st.session_state[f'last_text_{st.session_state.current_node}'] = story_text
        
        # Mostra il player se l'audio è disponibile
        if cache_key in st.session_state and st.session_state[cache_key]:
            audio_player = create_audio_player(
                st.session_state[cache_key], 
                st.session_state.get(f'tone_{st.session_state.current_node}', 'neutral')
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
    
    # Mostra il testo della storia con effetti tipografici migliorati
    st.markdown(f'<div class="story-text">{story_text}</div>', 
                unsafe_allow_html=True)
    
    # Gestisce i diversi tipi di nodi
    choices = current_node.get('choices', [])
    
    if not choices:
        # Nodo finale (vittoria)
        if not choices and st.session_state.current_node != 'game_over':
            # Schermata di vittoria semplificata
            st.balloons()  # Effetto palloncini di Streamlit
                        
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
        # Schermata di game over ultra-drammatica
        st.markdown(f"""
        <div class="game-over fade-in">
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

        # Mostra le scelte disponibili (dovrebbe essere solo "Ricomincia")
        shuffled_choices = shuffle_choices(choices, st.session_state.choice_order_seed)
        
        for i, choice in enumerate(shuffled_choices):
            icon = get_choice_icon(i)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"{icon} {choice['text']}", key=f"choice_gameover_{i}", use_container_width=True):
                    # Se è il bottone ricomincia dal game over
                    if choice.get('next_node') == 'start' or 'ricomincia' in choice['text'].lower():
                        reset_game()
                    else:
                        make_choice(choice['next_node'], choice['text'])
                    st.rerun()
    
    else:
        # Nodo normale con scelte
        st.markdown('<div class="choices-header fade-in">🎯 Il Destino Attende la Tua Decisione 🎯</div>', 
                   unsafe_allow_html=True)
        
        # Mescola le scelte usando il seed del gioco corrente
        shuffled_choices = shuffle_choices(choices, st.session_state.choice_order_seed + hash(st.session_state.current_node))
        
        # Crea le scelte con design ultra-migliorato e ordine casuale
        for i, choice in enumerate(shuffled_choices):
            icon = get_choice_icon(i)
            
            # Aggiunge una breve pausa tra i bottoni per effetto drammatico
            time.sleep(0.05)
            
            if st.button(f"{icon} {choice['text']}", key=f"choice_{st.session_state.current_node}_{i}", use_container_width=True):
                make_choice(choice['next_node'], choice['text'])
                # Piccola pausa per effetto drammatico
                time.sleep(0.1)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer ultra-elegante
    st.markdown("""
    <div class="footer fade-in">
        <p style="font-size: 1.2rem; margin-bottom: 1rem;">⭐ Che la saggezza illumini il tuo cammino, Maestro del Destino! ⭐</p>
        <p style="font-size: 0.95rem; opacity: 0.8; margin-bottom: 0.5rem;">Ogni scelta è un pennello che dipinge il tuo futuro...</p>
        <p style="font-size: 0.85rem; opacity: 0.6;">🎲 Le opzioni si riorganizzano ad ogni nuova avventura 🎲</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()