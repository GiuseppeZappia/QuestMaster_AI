import streamlit as st
import json
from pathlib import Path
from typing import Dict, List, Any
import time
import random

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
    """Resetta il gioco allo stato iniziale - FUNZIONE CORRETTA"""
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
        
        # Mostra la cronologia delle scelte e Controllo se ci sono effettivamente scelte per mostrare il progresso
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
    
    # Trova il nodo corrente
    current_node = find_node_by_id(story_data, st.session_state.current_node)
    
    if not current_node:
        st.error("⚠️ Errore: capitolo della leggenda non trovato!")
        return
    
    # Contenitore principale della storia con animazione migliorata
    st.markdown('<div class="story-container fade-in">', unsafe_allow_html=True)
    
    # Mostra il testo della storia con effetti tipografici migliorati
    st.markdown(f'<div class="story-text">{current_node.get("description", "")}</div>', 
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
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🌟 Forgia una Nuova Leggenda", key="play_again_victory", use_container_width=True):
                # Debug per vittoria
                st.write(f"DEBUG VITTORIA - Prima: {len(st.session_state.get('choices_made', []))}")
                reset_game()
                st.write(f"DEBUG VITTORIA - Dopo: {len(st.session_state.get('choices_made', []))}")
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
        
        # Mostra le scelte disponibili (dovrebbe essere solo "Ricomincia")
        shuffled_choices = shuffle_choices(choices, st.session_state.choice_order_seed)
        
        for i, choice in enumerate(shuffled_choices):
            icon = get_choice_icon(i)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(f"{icon} {choice['text']}", key=f"choice_gameover_{i}", use_container_width=True):
                    # Se è il bottone ricomincia dal game over
                    if choice.get('next_node') == 'start' or 'ricomincia' in choice['text'].lower():
                        st.write(f"DEBUG GAME OVER - Prima: {len(st.session_state.get('choices_made', []))}")
                        reset_game()
                        st.write(f"DEBUG GAME OVER - Dopo: {len(st.session_state.get('choices_made', []))}")
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