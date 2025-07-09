# import streamlit as st
# import json
# import os
# from typing import Dict, List, Any
# from datetime import datetime

# # Configurazione della pagina
# st.set_page_config(
#     page_title="Storia Interattiva",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # CSS personalizzato per l'interfaccia moderna
# st.markdown("""
# <style>
#     /* Stile principale */
#     .main {
#         padding: 1rem;
#     }
    
#     /* Card per la descrizione */
#     .story-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         border-radius: 20px;
#         padding: 2rem;
#         margin: 1rem 0;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.3);
#         color: white;
#         text-align: center;
#         animation: fadeIn 0.6s ease-in;
#     }
    
#     @keyframes fadeIn {
#         from { opacity: 0; transform: translateY(20px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
    
#     .story-description {
#         font-size: 1.2rem;
#         line-height: 1.6;
#         margin-bottom: 1.5rem;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
#     }
    
#     /* Bottoni delle scelte */
#     .choice-button {
#         background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
#         border: none;
#         border-radius: 15px;
#         padding: 1rem 2rem;
#         margin: 0.5rem;
#         color: white;
#         font-weight: bold;
#         font-size: 1.1rem;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.2);
#         width: 100%;
#         text-align: center;
#     }
    
#     .choice-button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 6px 20px rgba(0,0,0,0.3);
#     }
    
#     /* Traccia del percorso */
#     .path-tracker {
#         background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
#         border-radius: 15px;
#         padding: 1rem;
#         margin: 1rem 0;
#         color: white;
#         box-shadow: 0 5px 15px rgba(0,0,0,0.2);
#     }
    
#     .path-step {
#         background: rgba(255,255,255,0.2);
#         border-radius: 10px;
#         padding: 0.5rem 1rem;
#         margin: 0.3rem 0;
#         backdrop-filter: blur(10px);
#     }
    
#     /* Statistiche */
#     .stats-container {
#         display: flex;
#         justify-content: space-around;
#         margin: 1rem 0;
#     }
    
#     .stat-item {
#         background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
#         border-radius: 15px;
#         padding: 1rem;
#         text-align: center;
#         color: #333;
#         font-weight: bold;
#         box-shadow: 0 5px 15px rgba(0,0,0,0.1);
#         min-width: 120px;
#     }
    
#     /* Game Over */
#     .game-over {
#         background: linear-gradient(135deg, #ff7e7e 0%, #ff4757 100%);
#         border-radius: 20px;
#         padding: 2rem;
#         margin: 1rem 0;
#         color: white;
#         text-align: center;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.3);
#         animation: shake 0.5s ease-in-out;
#     }
    
#     @keyframes shake {
#         0%, 100% { transform: translateX(0); }
#         25% { transform: translateX(-5px); }
#         75% { transform: translateX(5px); }
#     }
    
#     /* Vittoria */
#     .victory {
#         background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
#         border-radius: 20px;
#         padding: 2rem;
#         margin: 1rem 0;
#         color: white;
#         text-align: center;
#         box-shadow: 0 10px 30px rgba(0,0,0,0.3);
#         animation: celebration 1s ease-in-out;
#     }
    
#     @keyframes celebration {
#         0%, 100% { transform: scale(1); }
#         50% { transform: scale(1.05); }
#     }
    
#     /* Responsive */
#     @media (max-width: 768px) {
#         .story-card {
#             padding: 1rem;
#             margin: 0.5rem 0;
#         }
        
#         .story-description {
#             font-size: 1rem;
#         }
        
#         .choice-button {
#             padding: 0.8rem 1.5rem;
#             font-size: 1rem;
#         }
        
#         .stats-container {
#             flex-direction: column;
#             gap: 0.5rem;
#         }
#     }
# </style>
# """, unsafe_allow_html=True)

# def load_story_json(file_path: str) -> Dict[str, Any]:
#     """Carica il file JSON della storia"""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         st.error(f"❌ File non trovato: {file_path}")
#         return None
#     except json.JSONDecodeError:
#         st.error(f"❌ Errore nel parsing del JSON: {file_path}")
#         return None

# def initialize_game_state():
#     """Inizializza lo stato del gioco"""
#     if 'current_node' not in st.session_state:
#         st.session_state.current_node = 'start'
#     if 'story_path' not in st.session_state:
#         st.session_state.story_path = []
#     if 'choices_made' not in st.session_state:
#         st.session_state.choices_made = 0
#     if 'game_started' not in st.session_state:
#         st.session_state.game_started = False
#     if 'start_time' not in st.session_state:
#         st.session_state.start_time = None

# def find_node_by_id(story_data: List[Dict], node_id: str) -> Dict:
#     """Trova un nodo tramite il suo ID"""
#     for node in story_data:
#         if node['node_id'] == node_id:
#             return node
#     return None

# def make_choice(next_node: str, choice_text: str):
#     """Gestisce la scelta dell'utente"""
#     st.session_state.story_path.append({
#         'node': st.session_state.current_node,
#         'choice': choice_text,
#         'timestamp': datetime.now().strftime("%H:%M:%S")
#     })
#     st.session_state.current_node = next_node
#     st.session_state.choices_made += 1
    
#     if not st.session_state.game_started:
#         st.session_state.game_started = True
#         st.session_state.start_time = datetime.now()

# def restart_game():
#     """Riavvia il gioco"""
#     st.session_state.current_node = 'start'
#     st.session_state.story_path = []
#     st.session_state.choices_made = 0
#     st.session_state.game_started = False
#     st.session_state.start_time = None

# def render_stats():
#     """Renderizza le statistiche del gioco"""
#     st.markdown("""
#     <div class="stats-container">
#         <div class="stat-item">
#             <div style="font-size: 1.5rem;">🎯</div>
#             <div>Scelte Fatte</div>
#             <div style="font-size: 1.2rem;">{}</div>
#         </div>
#         <div class="stat-item">
#             <div style="font-size: 1.5rem;">📍</div>
#             <div>Nodo Attuale</div>
#             <div style="font-size: 1.2rem;">{}</div>
#         </div>
#         <div class="stat-item">
#             <div style="font-size: 1.5rem;">⏱️</div>
#             <div>Tempo</div>
#             <div style="font-size: 1.2rem;">{}</div>
#         </div>
#     </div>
#     """.format(
#         st.session_state.choices_made,
#         st.session_state.current_node,
#         f"{int((datetime.now() - st.session_state.start_time).total_seconds())}s" if st.session_state.start_time else "0s"
#     ), unsafe_allow_html=True)

# def render_path_tracker():
#     """Renderizza il tracciatore del percorso"""
#     if st.session_state.story_path:
#         st.markdown('<div class="path-tracker">', unsafe_allow_html=True)
#         st.markdown('<h4>📋 Percorso Seguito:</h4>', unsafe_allow_html=True)
        
#         for i, step in enumerate(st.session_state.story_path[-5:]):  # Mostra solo gli ultimi 5 passi
#             st.markdown(f'''
#             <div class="path-step">
#                 <strong>Passo {len(st.session_state.story_path) - 4 + i}:</strong> {step['choice']} 
#                 <span style="float: right; opacity: 0.7;">{step['timestamp']}</span>
#             </div>
#             ''', unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)

# def main():
#     # Titolo principale
#     st.markdown("""
#     <div style="text-align: center; margin-bottom: 2rem;">
#         <h1 style="background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: bold;">
#             📚 Storia Interattiva
#         </h1>
#         <p style="font-size: 1.2rem; color: #666; margin-top: -1rem;">
#             Vivi un'avventura epica attraverso le tue scelte!
#         </p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Carica la storia
#     story_file_path = "file_generati/storia_generata.json"
#     story_data = load_story_json(story_file_path)
    
#     if story_data is None:
#         st.markdown("""
#         <div class="story-card">
#             <h2>🚫 Storia non trovata</h2>
#             <p>Il file della storia non è stato trovato. Assicurati che il file esista nel percorso:</p>
#             <code>file_generati/storia_generata.json</code>
#         </div>
#         """, unsafe_allow_html=True)
#         return
    
#     # Inizializza lo stato del gioco
#     initialize_game_state()
    
#     # Trova il nodo attuale
#     current_node = find_node_by_id(story_data, st.session_state.current_node)
    
#     if current_node is None:
#         st.error(f"❌ Nodo non trovato: {st.session_state.current_node}")
#         return
    
#     # Layout principale
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         # Determina il tipo di nodo
#         is_game_over = current_node['node_id'] == 'game_over'
#         is_victory = (len(current_node['choices']) == 0 and 
#                      current_node['node_id'] != 'game_over')
        
#         # Renderizza la card della storia
#         if is_game_over:
#             st.markdown(f"""
#             <div class="game-over">
#                 <h2>💀 Game Over!</h2>
#                 <div class="story-description">{current_node['description']}</div>
#             </div>
#             """, unsafe_allow_html=True)
#         elif is_victory:
#             st.markdown(f"""
#             <div class="victory">
#                 <h2>🎉 Vittoria!</h2>
#                 <div class="story-description">{current_node['description']}</div>
#                 <p style="margin-top: 1rem; font-size: 1.1rem;">
#                     Congratulazioni! Hai completato la storia con {st.session_state.choices_made} scelte!
#                 </p>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown(f"""
#             <div class="story-card">
#                 <div class="story-description">{current_node['description']}</div>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Renderizza le scelte
#         if current_node['choices']:
#             st.markdown("<h3 style='text-align: center; margin: 2rem 0 1rem 0;'>🤔 Cosa vuoi fare?</h3>", unsafe_allow_html=True)
            
#             for i, choice in enumerate(current_node['choices']):
#                 if st.button(
#                     choice['text'], 
#                     key=f"choice_{i}", 
#                     use_container_width=True,
#                     type="primary" if i == 0 else "secondary"
#                 ):
#                     make_choice(choice['next_node'], choice['text'])
#                     st.rerun()
        
#         # Bottone per ricominciare
#         if is_victory or is_game_over:
#             st.markdown("<br>", unsafe_allow_html=True)
#             col_restart1, col_restart2, col_restart3 = st.columns([1, 1, 1])
#             with col_restart2:
#                 if st.button("🔄 Ricomincia", use_container_width=True, type="primary"):
#                     restart_game()
#                     st.rerun()
    
#     with col2:
#         # Statistiche
#         render_stats()
        
#         # Tracciatore del percorso
#         render_path_tracker()
        
#         # Bottone di reset (sempre disponibile)
#         st.markdown("<br>", unsafe_allow_html=True)
#         if st.button("🔄 Reset Gioco", use_container_width=True, type="secondary"):
#             restart_game()
#             st.rerun()
        
#         # Informazioni sul file
#         st.markdown("""
#         <div style="background: #f0f2f6; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
#             <h4>ℹ️ Info</h4>
#             <p style="font-size: 0.9rem; margin: 0;">
#                 Storia caricata da:<br>
#                 <code>file_generati/storia_generata.json</code>
#             </p>
#         </div>
#         """, unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()


import streamlit as st
import json
import random
from pathlib import Path
import time

# Configurazione della pagina
st.set_page_config(
    page_title="Storia Interattiva",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizzato per migliorare l'aspetto
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .story-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .story-text {
        font-size: 1.2rem;
        line-height: 1.8;
        color: white;
        text-align: justify;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
    }
    
    .choice-button {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        border: none;
        padding: 1rem 2rem;
        margin: 0.5rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .choice-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .game-over {
        background: linear-gradient(135deg, #ff4757 0%, #ff3742 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .victory {
        background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.3rem;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .progress-container {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .step-indicator {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
    }
    
    .step-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin: 0 5px;
        background: rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }
    
    .step-dot.active {
        background: #4ECDC4;
        transform: scale(1.3);
    }
    
    .step-dot.completed {
        background: #2ed573;
    }
    
    .sidebar-info {
        background: rgba(46, 134, 171, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_story_json(file_path):
    """Carica il file JSON della storia"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"❌ File {file_path} non trovato!")
        return None
    except json.JSONDecodeError:
        st.error(f"❌ Errore nel parsing del file JSON!")
        return None

def find_node_by_id(story_data, node_id):
    """Trova un nodo specifico nell'array JSON"""
    for node in story_data:
        if node['node_id'] == node_id:
            return node
    return None

def shuffle_choices(choices):
    """Mescola le scelte mantenendo traccia dell'ordine originale"""
    if not choices:
        return []
    
    # Crea una lista di tuple (indice_originale, scelta)
    indexed_choices = [(i, choice) for i, choice in enumerate(choices)]
    
    # Mescola mantenendo il riferimento all'indice originale
    random.shuffle(indexed_choices)
    
    return indexed_choices

def initialize_session_state():
    """Inizializza le variabili di sessione"""
    if 'current_node' not in st.session_state:
        st.session_state.current_node = 'start'
    if 'story_history' not in st.session_state:
        st.session_state.story_history = []
    if 'step_count' not in st.session_state:
        st.session_state.step_count = 0
    if 'game_completed' not in st.session_state:
        st.session_state.game_completed = False
    if 'choice_seed' not in st.session_state:
        st.session_state.choice_seed = random.randint(1, 1000000)

def reset_game():
    """Resetta il gioco allo stato iniziale"""
    st.session_state.current_node = 'start'
    st.session_state.story_history = []
    st.session_state.step_count = 0
    st.session_state.game_completed = False
    st.session_state.choice_seed = random.randint(1, 1000000)

def display_progress_indicator(current_step, max_steps=10):
    """Mostra un indicatore di progresso"""
    st.markdown('<div class="step-indicator">', unsafe_allow_html=True)
    
    dots_html = ""
    for i in range(max_steps):
        if i < current_step:
            dots_html += '<div class="step-dot completed"></div>'
        elif i == current_step:
            dots_html += '<div class="step-dot active"></div>'
        else:
            dots_html += '<div class="step-dot"></div>'
    
    st.markdown(dots_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Inizializza lo stato della sessione
    initialize_session_state()
    
    # Titolo principale
    st.markdown('<h1 class="main-title">🏰 Storia Interattiva 🏰</h1>', unsafe_allow_html=True)
    
    # Carica la storia
    story_path = Path("file_generati/storia_generata.json")
    story_data = load_story_json(story_path)
    
    if story_data is None:
        st.error("❌ Impossibile caricare la storia. Assicurati che il file esista e sia valido.")
        return
    
    # Sidebar con informazioni
    with st.sidebar:
        st.markdown("## 📊 Statistiche")
        st.markdown(f"**Passo corrente:** {st.session_state.step_count + 1}")
        st.markdown(f"**Nodi visitati:** {len(st.session_state.story_history)}")
        
        if st.button("🔄 Ricomincia Gioco", use_container_width=True):
            reset_game()
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 📖 Cronologia")
        if st.session_state.story_history:
            for i, step in enumerate(st.session_state.story_history[-5:], 1):
                st.markdown(f"**{i}.** {step[:50]}...")
    
    # Trova il nodo corrente
    current_node = find_node_by_id(story_data, st.session_state.current_node)
    
    if current_node is None:
        st.error(f"❌ Nodo '{st.session_state.current_node}' non trovato!")
        return
    
    # Mostra indicatore di progresso
    display_progress_indicator(st.session_state.step_count)
    
    # Determina il tipo di nodo
    is_game_over = current_node['node_id'] == 'game_over'
    is_victory = not current_node['choices'] and current_node['node_id'] != 'game_over'
    
    # Mostra il contenuto del nodo
    if is_game_over:
        st.markdown(f'<div class="game-over">💀 {current_node["description"]} 💀</div>', unsafe_allow_html=True)
    elif is_victory:
        st.markdown(f'<div class="victory">🎉 {current_node["description"]} 🎉</div>', unsafe_allow_html=True)
        st.balloons()
        st.session_state.game_completed = True
    else:
        st.markdown(f'''
        <div class="story-container">
            <div class="story-text">
                {current_node["description"]}
            </div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Aggiungi la descrizione corrente alla cronologia se non è già presente
    if not st.session_state.story_history or st.session_state.story_history[-1] != current_node["description"]:
        st.session_state.story_history.append(current_node["description"])
    
    # Gestisci le scelte
    if current_node['choices']:
        st.markdown("### 🎯 Cosa vuoi fare?")
        
        # Usa un seed fisso per mantenere lo stesso ordine durante la sessione
        random.seed(st.session_state.choice_seed + hash(st.session_state.current_node))
        shuffled_choices = shuffle_choices(current_node['choices'])
        
        # Crea i bottoni per le scelte
        cols = st.columns(min(len(shuffled_choices), 3))
        
        for i, (original_index, choice) in enumerate(shuffled_choices):
            with cols[i % len(cols)]:
                if st.button(
                    choice['text'], 
                    key=f"choice_{original_index}_{st.session_state.choice_seed}",
                    use_container_width=True
                ):
                    # Aggiorna lo stato
                    st.session_state.current_node = choice['next_node']
                    st.session_state.step_count += 1
                    
                    # Aggiungi un piccolo effetto di transizione
                    with st.spinner("🔄 Caricamento..."):
                        time.sleep(0.5)
                    
                    # Rerun per aggiornare la pagina
                    st.rerun()
    
    # Mostra messaggio di completamento
    if is_victory and st.session_state.game_completed:
        st.markdown("---")
        st.markdown("### 🏆 Congratulazioni!")
        st.markdown("Hai completato con successo la storia interattiva!")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🎮 Gioca di Nuovo", use_container_width=True):
                reset_game()
                st.rerun()

if __name__ == "__main__":
    main()

# import streamlit as st
# import json
# import random
# from pathlib import Path
# import time
# import os
# from datetime import datetime
# import base64
# from typing import Dict, List, Any, Optional
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import hashlib

# # Carica le variabili d'ambiente
# load_dotenv()

# # Configurazione della pagina
# st.set_page_config(
#     page_title="Quest Interattiva",
#     page_icon="🏰",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # CSS personalizzato per un'interfaccia da gioco
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Roboto:wght@300;400;500&display=swap');
    
#     .main {
#         background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
#         color: #ffffff;
#         font-family: 'Roboto', sans-serif;
#     }
    
#     .main-title {
#         font-family: 'Cinzel', serif;
#         font-size: 3.5rem;
#         font-weight: 600;
#         text-align: center;
#         background: linear-gradient(45deg, #ffd700, #ff6b35, #f7931e);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         background-clip: text;
#         text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
#         margin-bottom: 2rem;
#         animation: glow 2s ease-in-out infinite alternate;
#     }
    
#     @keyframes glow {
#         from { text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
#         to { text-shadow: 0 0 30px rgba(255, 215, 0, 0.8), 0 0 40px rgba(255, 107, 53, 0.6); }
#     }
    
#     .quest-container {
#         background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%);
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(255, 255, 255, 0.2);
#         border-radius: 20px;
#         padding: 2.5rem;
#         margin: 1.5rem 0;
#         box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
#         position: relative;
#         overflow: hidden;
#     }
    
#     .quest-container::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: 0;
#         right: 0;
#         height: 3px;
#         background: linear-gradient(90deg, #ffd700, #ff6b35, #f7931e);
#         animation: shimmer 2s linear infinite;
#     }
    
#     @keyframes shimmer {
#         0% { transform: translateX(-100%); }
#         100% { transform: translateX(100%); }
#     }
    
#     .story-text {
#         font-size: 1.3rem;
#         line-height: 1.9;
#         color: #e0e0e0;
#         text-align: justify;
#         margin-bottom: 2rem;
#         text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
#         animation: fadeIn 1s ease-in;
#     }
    
#     @keyframes fadeIn {
#         from { opacity: 0; transform: translateY(20px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
    
#     .choice-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
#         gap: 1rem;
#         margin-top: 2rem;
#     }
    
#     .choice-card {
#         background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#         border: 2px solid transparent;
#         border-radius: 15px;
#         padding: 1.5rem;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         position: relative;
#         overflow: hidden;
#         box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
#     }
    
#     .choice-card:hover {
#         transform: translateY(-5px) scale(1.02);
#         box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
#         border-color: #ffd700;
#     }
    
#     .choice-card::before {
#         content: '';
#         position: absolute;
#         top: 0;
#         left: -100%;
#         width: 100%;
#         height: 100%;
#         background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
#         transition: left 0.5s ease;
#     }
    
#     .choice-card:hover::before {
#         left: 100%;
#     }
    
#     .choice-text {
#         font-size: 1.1rem;
#         font-weight: 500;
#         color: white;
#         text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
#         z-index: 1;
#         position: relative;
#     }
    
#     .game-over {
#         background: linear-gradient(135deg, #ff4757 0%, #c44569 100%);
#         color: white;
#         padding: 3rem;
#         border-radius: 20px;
#         text-align: center;
#         font-size: 1.5rem;
#         font-weight: bold;
#         margin: 2rem 0;
#         box-shadow: 0 20px 40px rgba(255, 71, 87, 0.3);
#         animation: shake 0.5s ease-in-out, fadeIn 1s ease-in;
#     }
    
#     @keyframes shake {
#         0%, 100% { transform: translateX(0); }
#         25% { transform: translateX(-5px); }
#         75% { transform: translateX(5px); }
#     }
    
#     .victory {
#         background: linear-gradient(135deg, #2ed573 0%, #1e90ff 100%);
#         color: white;
#         padding: 3rem;
#         border-radius: 20px;
#         text-align: center;
#         font-size: 1.5rem;
#         font-weight: bold;
#         margin: 2rem 0;
#         box-shadow: 0 20px 40px rgba(46, 213, 115, 0.3);
#         animation: celebration 1s ease-in-out, fadeIn 1s ease-in;
#     }
    
#     @keyframes celebration {
#         0%, 100% { transform: scale(1); }
#         50% { transform: scale(1.05); }
#     }
    
#     .sidebar-panel {
#         background: rgba(255, 255, 255, 0.05);
#         backdrop-filter: blur(10px);
#         border: 1px solid rgba(255, 255, 255, 0.1);
#         border-radius: 15px;
#         padding: 1.5rem;
#         margin: 1rem 0;
#         box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
#     }
    
#     .stat-item {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         padding: 0.8rem 0;
#         border-bottom: 1px solid rgba(255, 255, 255, 0.1);
#     }
    
#     .stat-item:last-child {
#         border-bottom: none;
#     }
    
#     .stat-label {
#         font-weight: 500;
#         color: #b0b0b0;
#     }
    
#     .stat-value {
#         font-weight: bold;
#         color: #ffd700;
#         font-size: 1.1rem;
#     }
    
#     .progress-bar {
#         width: 100%;
#         height: 8px;
#         background: rgba(255, 255, 255, 0.1);
#         border-radius: 4px;
#         overflow: hidden;
#         margin: 1rem 0;
#     }
    
#     .progress-fill {
#         height: 100%;
#         background: linear-gradient(90deg, #ffd700, #ff6b35);
#         transition: width 0.3s ease;
#         border-radius: 4px;
#     }
    
#     .history-item {
#         background: rgba(255, 255, 255, 0.05);
#         border-left: 3px solid #ffd700;
#         padding: 1rem;
#         margin: 0.5rem 0;
#         border-radius: 0 10px 10px 0;
#         font-size: 0.9rem;
#         color: #d0d0d0;
#     }
    
#     .image-container {
#         display: flex;
#         justify-content: center;
#         align-items: center;
#         margin: 1.5rem 0;
#         border-radius: 15px;
#         overflow: hidden;
#         box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
#     }
    
#     .generated-image {
#         max-width: 100%;
#         height: auto;
#         border-radius: 15px;
#         animation: fadeIn 1s ease-in;
#     }
    
#     .loading-spinner {
#         display: inline-block;
#         width: 20px;
#         height: 20px;
#         border: 3px solid rgba(255, 255, 255, 0.3);
#         border-radius: 50%;
#         border-top-color: #ffd700;
#         animation: spin 1s ease-in-out infinite;
#     }
    
#     @keyframes spin {
#         to { transform: rotate(360deg); }
#     }
    
#     .action-button {
#         background: linear-gradient(135deg, #ffd700 0%, #ff6b35 100%);
#         color: #1a1a2e;
#         border: none;
#         padding: 1rem 2rem;
#         border-radius: 25px;
#         font-size: 1.1rem;
#         font-weight: bold;
#         cursor: pointer;
#         transition: all 0.3s ease;
#         box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);
#         text-transform: uppercase;
#         letter-spacing: 1px;
#     }
    
#     .action-button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 15px 35px rgba(255, 215, 0, 0.5);
#     }
    
#     .node-indicator {
#         position: absolute;
#         top: 1rem;
#         right: 1rem;
#         background: rgba(255, 215, 0, 0.2);
#         color: #ffd700;
#         padding: 0.5rem 1rem;
#         border-radius: 20px;
#         font-size: 0.9rem;
#         font-weight: bold;
#     }
    
#     .watermark {
#         position: fixed;
#         bottom: 1rem;
#         right: 1rem;
#         background: rgba(0, 0, 0, 0.5);
#         color: rgba(255, 255, 255, 0.7);
#         padding: 0.5rem 1rem;
#         border-radius: 20px;
#         font-size: 0.8rem;
#         backdrop-filter: blur(5px);
#         z-index: 1000;
#     }
    
#     .hidden-button {
#         display: none;
#     }
# </style>
# """, unsafe_allow_html=True)

# class QuestManager:
#     def __init__(self):
#         self.api_key = os.getenv("API_KEY")
#         if self.api_key:
#             os.environ["GOOGLE_API_KEY"] = self.api_key
#             # Usa il modello corretto per la generazione di immagini
#             self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
#         else:
#             self.llm = None
    
#     # # def generate_image(self, prompt: str, node_id: str) -> Optional[str]:
#     #     from google import genai
#     #     from google.genai import types
#     #     from PIL import Image
#     #     from io import BytesIO
#     #     import base64

#     #     client = genai.Client()



#     #     """Genera un'immagine usando Gemini 2.0 Flash"""
#     #     if not self.llm:
#     #         return None
            
#     #     try:
#     #         # Crea un prompt più specifico per l'immagine
#     #         image_prompt = f"Genera un'immagine fantasy epica per una quest interattiva: {prompt}. Stile: fantasy art, dettagliato, atmosferico, colori vivaci."
            

#     #         response = client.models.generate_content(
#     #                 model="gemini-2.0-flash-preview-image-generation",
#     #                 contents=image_prompt,
#     #                 config=types.GenerateContentConfig(
#     #                 response_modalities=['TEXT', 'IMAGE']
#     #                 )
#     #             )

#     #         for part in response.candidates[0].content.parts:
#     #             if part.text is not None:
#     #                 print(part.text)
#     #             elif part.inline_data is not None:
#     #                 image = Image.open(BytesIO((part.inline_data.data)))
#     #                 image.save('gemini-native-image.png')
#     #                 image.show()
#     #                 return part.inline_data.data

            
#     #         # Estrai l'immagine dalla risposta
#     #         # if hasattr(response, 'content'):
#     #         #     # Controlla se la risposta contiene un'immagine
#     #         #     if hasattr(response.content, 'parts'):
#     #         #         for part in response.content.parts:
#     #         #             if hasattr(part, 'inline_data') and part.inline_data:
#     #         #                 return part.inline_data.data
                
#     #         #     # Se non c'è un'immagine, prova a cercare nel contenuto direttamente
#     #         #     if hasattr(response.content, 'data'):
#     #         #         return response.content.data
            
#     #         # return None
            
#     #     except Exception as e:
#     #         st.error(f"Errore nella generazione dell'immagine: {str(e)}")
#     #         return None
    
#     # def get_image_cache_key(self, node_id: str, description: str) -> str:
#     #     """Genera una chiave cache per l'immagine"""
#     #     content = f"{node_id}_{description}"
#     #     return hashlib.md5(content.encode()).hexdigest()

# def load_story_json(file_path: Path) -> Optional[List[Dict]]:
#     """Carica il file JSON della storia"""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         st.error(f"❌ File {file_path} non trovato!")
#         return None
#     except json.JSONDecodeError:
#         st.error(f"❌ Errore nel parsing del file JSON!")
#         return None

# def find_node_by_id(story_data: List[Dict], node_id: str) -> Optional[Dict]:
#     """Trova un nodo specifico nell'array JSON"""
#     for node in story_data:
#         if node['node_id'] == node_id:
#             return node
#     return None

# def initialize_session_state():
#     """Inizializza le variabili di sessione"""
#     if 'current_node' not in st.session_state:
#         st.session_state.current_node = 'start'
#     if 'story_history' not in st.session_state:
#         st.session_state.story_history = []
#     if 'choice_history' not in st.session_state:
#         st.session_state.choice_history = []
#     if 'step_count' not in st.session_state:
#         st.session_state.step_count = 0
#     if 'game_completed' not in st.session_state:
#         st.session_state.game_completed = False
#     if 'choice_seed' not in st.session_state:
#         st.session_state.choice_seed = random.randint(1, 1000000)
#     if 'start_time' not in st.session_state:
#         st.session_state.start_time = datetime.now()
#     if 'total_nodes' not in st.session_state:
#         st.session_state.total_nodes = 0
#     if 'image_cache' not in st.session_state:
#         st.session_state.image_cache = {}
#     if 'current_image' not in st.session_state:
#         st.session_state.current_image = None
#     if 'selected_choice' not in st.session_state:
#         st.session_state.selected_choice = None

# def reset_game():
#     """Resetta completamente il gioco allo stato iniziale"""
#     st.session_state.current_node = 'start'
#     st.session_state.story_history = []
#     st.session_state.choice_history = []
#     st.session_state.step_count = 0
#     st.session_state.game_completed = False
#     st.session_state.choice_seed = random.randint(1, 1000000)
#     st.session_state.start_time = datetime.now()
#     st.session_state.current_image = None
#     st.session_state.selected_choice = None
#     # Mantieni la cache delle immagini per performance

# def calculate_progress(current_step: int, total_nodes: int) -> float:
#     """Calcola la percentuale di progresso"""
#     if total_nodes == 0:
#         return 0.0
#     return min((current_step / total_nodes) * 100, 100.0)

# def format_time_elapsed(start_time: datetime) -> str:
#     """Formatta il tempo trascorso"""
#     elapsed = datetime.now() - start_time
#     minutes = int(elapsed.total_seconds() // 60)
#     seconds = int(elapsed.total_seconds() % 60)
#     return f"{minutes:02d}:{seconds:02d}"

# def display_story_image(quest_manager: QuestManager, node: Dict):
#     """Mostra l'immagine generata per il nodo corrente"""
#     if not quest_manager.llm:
#         return
    
#     cache_key = quest_manager.get_image_cache_key(node['node_id'], node['description'])
    
#     # Controlla se l'immagine è già in cache
#     if cache_key in st.session_state.image_cache:
#         image_data = st.session_state.image_cache[cache_key]
#         if image_data:
#             st.markdown('<div class="image-container">', unsafe_allow_html=True)
#             # Decodifica l'immagine base64
#             try:
#                 image_bytes = base64.b64decode(image_data)
#                 st.image(image_bytes, use_column_width=True)
#             except:
#                 st.image(image_data, use_column_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)
#         return
    
#     # Genera nuova immagine
#     with st.spinner("🎨 Generando immagine..."):
#         # Crea un prompt per l'immagine basato sulla descrizione
#         image_prompt = f"Scena fantasy basata su: {node['description'][:200]}..."
        
#         image_data = quest_manager.generate_image(image_prompt, node['node_id'])
        
#         # Salva in cache
#         st.session_state.image_cache[cache_key] = image_data
        
#         if image_data:
#             st.markdown('<div class="image-container">', unsafe_allow_html=True)
#             try:
#                 image_bytes = base64.b64decode(image_data)
#                 st.image(image_bytes, use_column_width=True)
#             except:
#                 st.image(image_data, use_column_width=True)
#             st.markdown('</div>', unsafe_allow_html=True)

# def render_sidebar(story_data: List[Dict], current_node: Dict):
#     """Renderizza la sidebar con statistiche e controlli"""
#     st.sidebar.markdown("# 🎮 Pannello di Controllo")
    
#     # Statistiche principali
#     st.sidebar.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
#     st.sidebar.markdown("## 📊 Statistiche")
    
#     # Calcola progresso
#     progress = calculate_progress(st.session_state.step_count, len(story_data))
    
#     st.sidebar.markdown(f'''
#     <div class="stat-item">
#         <span class="stat-label">Nodo Attuale:</span>
#         <span class="stat-value">{current_node['node_id']}</span>
#     </div>
#     <div class="stat-item">
#         <span class="stat-label">Passi Completati:</span>
#         <span class="stat-value">{st.session_state.step_count}</span>
#     </div>
#     <div class="stat-item">
#         <span class="stat-label">Tempo Trascorso:</span>
#         <span class="stat-value">{format_time_elapsed(st.session_state.start_time)}</span>
#     </div>
#     <div class="stat-item">
#         <span class="stat-label">Progresso:</span>
#         <span class="stat-value">{progress:.1f}%</span>
#     </div>
#     ''', unsafe_allow_html=True)
    
#     # Barra di progresso
#     st.sidebar.markdown(f'''
#     <div class="progress-bar">
#         <div class="progress-fill" style="width: {progress}%"></div>
#     </div>
#     ''', unsafe_allow_html=True)
    
#     st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
#     # Controlli del gioco
#     st.sidebar.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
#     st.sidebar.markdown("## 🎲 Controlli")
    
#     col1, col2 = st.sidebar.columns(2)
    
#     with col1:
#         if st.button("🔄 Restart", use_container_width=True, key="restart_btn"):
#             reset_game()
#             st.rerun()
    
#     with col2:
#         if st.button("💾 Salva", use_container_width=True, key="save_btn"):
#             save_game_state()
#             st.success("Gioco salvato!", icon="✅")
    
#     st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
#     # Cronologia scelte
#     if st.session_state.choice_history:
#         st.sidebar.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
#         st.sidebar.markdown("## 📜 Cronologia Scelte")
        
#         # Mostra solo le ultime 5 scelte
#         recent_choices = st.session_state.choice_history[-5:]
#         for i, choice in enumerate(recent_choices, 1):
#             st.sidebar.markdown(f'''
#             <div class="history-item">
#                 <strong>{len(st.session_state.choice_history) - len(recent_choices) + i}.</strong> {choice[:60]}{"..." if len(choice) > 60 else ""}
#             </div>
#             ''', unsafe_allow_html=True)
        
#         st.sidebar.markdown('</div>', unsafe_allow_html=True)

# def save_game_state():
#     """Salva lo stato del gioco"""
#     game_state = {
#         'current_node': st.session_state.current_node,
#         'story_history': st.session_state.story_history,
#         'choice_history': st.session_state.choice_history,
#         'step_count': st.session_state.step_count,
#         'start_time': st.session_state.start_time.isoformat(),
#         'timestamp': datetime.now().isoformat()
#     }
    
#     # Salva in un file JSON
#     save_path = Path("game_saves")
#     save_path.mkdir(exist_ok=True)
    
#     filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
#     with open(save_path / filename, 'w', encoding='utf-8') as f:
#         json.dump(game_state, f, indent=2, ensure_ascii=False)

# def handle_choice_selection(choice, choice_index):
#     """Gestisce la selezione di una scelta"""
#     # Aggiorna lo stato
#     st.session_state.current_node = choice['next_node']
#     st.session_state.step_count += 1
#     st.session_state.choice_history.append(choice['text'])
#     st.session_state.selected_choice = choice_index
    
#     # Effetto di caricamento
#     with st.spinner("🔄 Elaborando la tua scelta..."):
#         time.sleep(0.8)
    
#     st.rerun()

# def main():
#     # Inizializza lo stato della sessione
#     initialize_session_state()
    
#     # Inizializza il manager delle quest
#     quest_manager = QuestManager()
    
#     # Titolo principale
#     st.markdown('<h1 class="main-title">🏰 QUEST INTERATTIVA 🏰</h1>', unsafe_allow_html=True)
    
#     # Carica la storia
#     story_path = Path("file_generati/storia_generata.json")
#     story_data = load_story_json(story_path)
    
#     if story_data is None:
#         st.error("❌ Impossibile caricare la storia. Assicurati che il file esista e sia valido.")
#         st.stop()
    
#     # Aggiorna il conteggio totale nodi
#     if st.session_state.total_nodes == 0:
#         st.session_state.total_nodes = len(story_data)
    
#     # Trova il nodo corrente
#     current_node = find_node_by_id(story_data, st.session_state.current_node)
    
#     if current_node is None:
#         st.error(f"❌ Nodo '{st.session_state.current_node}' non trovato!")
#         st.stop()
    
#     # Renderizza la sidebar
#     render_sidebar(story_data, current_node)
    
#     # Layout principale
#     main_col, _ = st.columns([4, 1])
    
#     with main_col:
#         # Determina il tipo di nodo
#         is_game_over = current_node['node_id'] == 'game_over'
#         is_victory = not current_node['choices'] and current_node['node_id'] != 'game_over'
        
#         # Container principale della quest
#         st.markdown('<div class="quest-container">', unsafe_allow_html=True)
        
#         # Indicatore del nodo corrente
#         st.markdown(f'<div class="node-indicator">📍 {current_node["node_id"]}</div>', unsafe_allow_html=True)
        
#         # Mostra l'immagine generata (disabilitata temporaneamente per evitare errori)
#         # if quest_manager.llm and not is_game_over and not is_victory:
#         #     display_story_image(quest_manager, current_node)
        
#         # Mostra il contenuto del nodo
#         if is_game_over:
#             st.markdown(f'<div class="game-over">💀 GAME OVER 💀<br><br>{current_node["description"]}</div>', unsafe_allow_html=True)
#             st.session_state.game_completed = True
#         elif is_victory:
#             st.markdown(f'<div class="victory">🎉 VITTORIA! 🎉<br><br>{current_node["description"]}</div>', unsafe_allow_html=True)
#             st.balloons()
#             st.session_state.game_completed = True
#         else:
#             st.markdown(f'<div class="story-text">{current_node["description"]}</div>', unsafe_allow_html=True)
        
#         # Aggiungi alla cronologia se non è già presente
#         if not st.session_state.story_history or st.session_state.story_history[-1] != current_node["description"]:
#             st.session_state.story_history.append(current_node["description"])
        
#         # Gestisci le scelte
#         if current_node['choices'] and not st.session_state.game_completed:
#             st.markdown("### 🎯 Scegli la tua azione:")
            
#             # Mescola le scelte ma mantieni consistenza
#             random.seed(st.session_state.choice_seed + hash(st.session_state.current_node))
#             shuffled_choices = current_node['choices'].copy()
#             random.shuffle(shuffled_choices)
            
#             # Crea bottoni per le scelte
#             for i, choice in enumerate(shuffled_choices):
#                 # Usa un container per ogni scelta
#                 choice_container = st.container()
                
#                 with choice_container:
#                     # Bottone visibile per la scelta
#                     if st.button(
#                         choice['text'],
#                         key=f"choice_btn_{i}",
#                         use_container_width=True,
#                         type="primary"
#                     ):
#                         handle_choice_selection(choice, i)
        
#         # Bottone per ricominciare se il gioco è terminato
#         if st.session_state.game_completed:
#             st.markdown("<br><br>", unsafe_allow_html=True)
#             col1, col2, col3 = st.columns([1, 2, 1])
            
#             with col2:
#                 if st.button("🎮 NUOVA PARTITA", use_container_width=True, key="new_game_btn"):
#                     reset_game()
#                     st.rerun()
        
#         st.markdown('</div>', unsafe_allow_html=True)
        
#     # Watermark
#     st.markdown('<div class="watermark">🎮 Quest Interactive Engine v2.0</div>', unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()