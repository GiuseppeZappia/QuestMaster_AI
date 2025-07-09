import streamlit as st
import json
import os
from typing import Dict, List, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import re

# Carica variabili ambiente
load_dotenv()

class QuestMasterGameEngine:
    """Engine per gestire lo stato del gioco e l'interazione con l'LLM"""
    
    def __init__(self):
        self.llm = self._initialize_llm()
        self.lore = self._load_lore()
        self.solution = self._load_solution()
        self.current_step = 0
        self.story_state = self._initialize_story_state()
        
    def _initialize_llm(self):
        """Inizializza il modello LLM"""
        api_key = os.getenv("API_KEY")
        if not api_key:
            st.error("API Key non trovata! Assicurati di avere un file .env con API_KEY")
            return None
        
        os.environ["GOOGLE_API_KEY"] = api_key
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.7
        )
    
    def _load_lore(self):
        """Carica la lore generata nella Fase 1"""
        try:
            with open("file_generati/lore_generata_per_utente.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error("File lore non trovato! Assicurati di aver completato la Fase 1")
            return None
    
    def _load_solution(self):
        """Carica la soluzione PDDL generata"""
        try:
            with open("fastdownward_output/solution.txt", 'r', encoding='utf-8') as f:
                actions = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith(';'):
                        actions.append(line)
                return actions
        except FileNotFoundError:
            st.warning("Soluzione PDDL non trovata, modalità libera attivata")
            return []
    
    def _initialize_story_state(self):
        """Inizializza lo stato iniziale della storia"""
        if not self.lore:
            return {}
        
        return {
            "current_scene": "initial",
            "story_history": [],
            "available_actions": [],
            "narrative_context": self.lore.get("quest_description", {}).get("initial_state", ""),
            "goal": self.lore.get("quest_description", {}).get("goal", ""),
            "completed": False
        }
    
    def generate_story_scene(self, action_taken=None):
        """Genera una scena narrativa usando l'LLM"""
        
        # Determina l'azione PDDL corrente se disponibile
        current_pddl_action = ""
        if self.solution and self.current_step < len(self.solution):
            current_pddl_action = self.solution[self.current_step]
        
        # Costruisci il prompt per l'LLM
        prompt = f"""Sei un narratore esperto di avventure interattive. 

CONTESTO DELLA QUEST:
- Titolo: {self.lore.get('quest_description', {}).get('title', 'Avventura Sconosciuta')}
- Descrizione: {self.lore.get('quest_description', {}).get('description', '')}
- Obiettivo: {self.story_state['goal']}

STATO ATTUALE:
- Passo della storia: {self.current_step + 1}
- Azione precedente: {action_taken or 'Inizio avventura'}
- Azione PDDL corrente: {current_pddl_action}
- Storia precedente: {' '.join(self.story_state['story_history'][-2:]) if len(self.story_state['story_history']) > 0 else 'Inizio'}

VINCOLI:
- Branching factor: min {self.lore.get('branching_factor', {}).get('min', 2)}, max {self.lore.get('branching_factor', {}).get('max', 4)}
- Lunghezza storia: min {self.lore.get('depth_constraints', {}).get('min', 3)}, max {self.lore.get('depth_constraints', {}).get('max', 10)} passi

ISTRUZIONI:
1. Genera una descrizione narrativa coinvolgente (2-4 paragrafi) della situazione attuale
2. Proponi 2-4 azioni specifiche che il giocatore può intraprendere
3. Mantieni coerenza con la lore e l'azione PDDL se disponibile
4. Usa un tono avvincente e descrittivo

FORMATO OUTPUT:
DESCRIZIONE:
[descrizione della scena corrente]

AZIONI:
1. [azione 1]
2. [azione 2]
3. [azione 3]
4. [azione 4]

STATO:
[CONTINUA/COMPLETATA] - usa COMPLETATA solo se l'obiettivo è raggiunto
"""

        try:
            response = self.llm.invoke(prompt)
            return self._parse_story_response(response.content)
        except Exception as e:
            st.error(f"Errore nella generazione della storia: {e}")
            return self._fallback_story_scene()
    
    def _parse_story_response(self, response_text):
        """Parsing della risposta dell'LLM"""
        
        # Trova le sezioni
        description_match = re.search(r'DESCRIZIONE:\s*\n(.*?)(?=AZIONI:|$)', response_text, re.DOTALL)
        actions_match = re.search(r'AZIONI:\s*\n(.*?)(?=STATO:|$)', response_text, re.DOTALL)
        status_match = re.search(r'STATO:\s*\n(.*?)(?=\n|$)', response_text, re.DOTALL)
        
        description = description_match.group(1).strip() if description_match else "Continua la tua avventura..."
        
        # Estrai le azioni
        actions = []
        if actions_match:
            actions_text = actions_match.group(1).strip()
            for line in actions_text.split('\n'):
                line = line.strip()
                if line and (line.startswith(('1.', '2.', '3.', '4.')) or line.startswith('-')):
                    # Pulisci il numero/bullet point
                    action = re.sub(r'^\d+\.\s*', '', line)
                    action = re.sub(r'^-\s*', '', action)
                    if action:
                        actions.append(action)
        
        # Determina se la quest è completata
        completed = False
        if status_match:
            status_text = status_match.group(1).strip().upper()
            completed = 'COMPLETATA' in status_text
        
        return {
            "description": description,
            "actions": actions,
            "completed": completed
        }
    
    def _fallback_story_scene(self):
        """Scena di fallback in caso di errore"""
        return {
            "description": "Ti trovi in un momento cruciale della tua avventura. Le tue scelte determineranno il corso degli eventi.",
            "actions": [
                "Procedi con cautela",
                "Agisci con determinazione",
                "Cerca maggiori informazioni",
                "Torna indietro"
            ],
            "completed": False
        }
    
    def take_action(self, action_index):
        """Elabora l'azione scelta dal giocatore"""
        if action_index < len(self.story_state["available_actions"]):
            chosen_action = self.story_state["available_actions"][action_index]
            
            # Aggiorna lo stato
            self.story_state["story_history"].append(chosen_action)
            self.current_step += 1
            
            # Genera la prossima scena
            scene_data = self.generate_story_scene(chosen_action)
            
            # Aggiorna lo stato della storia
            self.story_state["narrative_context"] = scene_data["description"]
            self.story_state["available_actions"] = scene_data["actions"]
            self.story_state["completed"] = scene_data["completed"]
            
            return scene_data
        return None

def main():
    """Funzione principale dell'interfaccia Streamlit"""
    
    st.set_page_config(
        page_title="QuestMaster - Fase 2",
        page_icon="🎮",
        layout="wide"
    )
    
    st.title("🎮 QuestMaster - Avventura Interattiva")
    st.markdown("---")
    
    # Inizializza il session state
    if 'game_engine' not in st.session_state:
        st.session_state.game_engine = QuestMasterGameEngine()
        if st.session_state.game_engine.lore:
            initial_scene = st.session_state.game_engine.generate_story_scene()
            st.session_state.game_engine.story_state.update(initial_scene)
    
    engine = st.session_state.game_engine
    
    # Verifica che tutto sia caricato correttamente
    if not engine.lore:
        st.error("⚠️ Errore nel caricamento dei file della Fase 1")
        st.info("Assicurati di aver completato la Fase 1 e che i file siano presenti in:")
        st.code("file_generati/lore_generata_per_utente.json")
        return
    
    # Sidebar con informazioni
    with st.sidebar:
        st.header("📋 Informazioni Quest")
        st.subheader(engine.lore.get("quest_description", {}).get("title", "Avventura"))
        st.write(engine.lore.get("quest_description", {}).get("description", ""))
        
        st.subheader("🎯 Obiettivo")
        st.write(engine.story_state["goal"])
        
        st.subheader("📊 Progresso")
        st.write(f"Passo: {engine.current_step + 1}")
        
        if engine.solution:
            max_steps = len(engine.solution)
            progress = min(engine.current_step / max_steps, 1.0) if max_steps > 0 else 0
            st.progress(progress)
            st.write(f"Passi totali: {max_steps}")
        
        # Bottone per ricominciare
        if st.button("🔄 Ricomincia Avventura"):
            st.session_state.game_engine = QuestMasterGameEngine()
            st.rerun()
    
    # Area principale del gioco
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📖 Narrativa")
        
        # Mostra la descrizione corrente
        if engine.story_state["narrative_context"]:
            st.markdown(f"*{engine.story_state['narrative_context']}*")
        
        # Controlla se la quest è completata
        if engine.story_state["completed"]:
            st.success("🎉 Congratulazioni! Hai completato la quest!")
            st.balloons()
            
            if st.button("🆕 Nuova Avventura"):
                st.session_state.game_engine = QuestMasterGameEngine()
                st.rerun()
        else:
            st.header("⚡ Scegli la tua azione")
            
            # Mostra le azioni disponibili
            if engine.story_state["available_actions"]:
                for i, action in enumerate(engine.story_state["available_actions"]):
                    if st.button(f"🎯 {action}", key=f"action_{i}", use_container_width=True):
                        with st.spinner("Elaborando la tua scelta..."):
                            scene_data = engine.take_action(i)
                            if scene_data:
                                st.rerun()
            else:
                st.info("Generando le prossime azioni disponibili...")
    
    with col2:
        st.header("📚 Storia")
        
        # Mostra la storia delle azioni
        if engine.story_state["story_history"]:
            st.subheader("🔄 Azioni Precedenti")
            for i, action in enumerate(reversed(engine.story_state["story_history"][-5:])):
                st.write(f"**{len(engine.story_state['story_history']) - i}.** {action}")
        
        # Informazioni tecniche (debug)
        with st.expander("🔧 Informazioni Tecniche"):
            st.write("**Stato del gioco:**")
            st.json({
                "current_step": engine.current_step,
                "total_solution_steps": len(engine.solution) if engine.solution else 0,
                "completed": engine.story_state["completed"],
                "actions_count": len(engine.story_state["available_actions"])
            })
            
            if engine.solution and engine.current_step < len(engine.solution):
                st.write(f"**Azione PDDL corrente:** `{engine.solution[engine.current_step]}`")

if __name__ == "__main__":
    main()

# import json
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv

# load_dotenv()

# class HTMLGameGenerator:
#     """Classe per generare un'interfaccia HTML completa per la quest"""
    
#     def __init__(self):
#         self.llm = self._initialize_llm()
#         self.lore = self._load_lore()
#         self.solution = self._load_solution()
        
#     def _initialize_llm(self):
#         """Inizializza il modello LLM"""
#         api_key = os.getenv("API_KEY")
#         if not api_key:
#             print("❌ API Key non trovata!")
#             return None
        
#         os.environ["GOOGLE_API_KEY"] = api_key
#         return ChatGoogleGenerativeAI(
#             model="gemini-2.0-flash",
#             temperature=0.7
#         )
    
#     def _load_lore(self):
#         """Carica la lore generata"""
#         try:
#             with open("file_generati/lore_generata_per_utente.json", 'r', encoding='utf-8') as f:
#                 return json.load(f)
#         except FileNotFoundError:
#             print("❌ File lore non trovato!")
#             return None
    
#     def _load_solution(self):
#         """Carica la soluzione PDDL"""
#         try:
#             with open("fastdownward_output/solution.txt", 'r', encoding='utf-8') as f:
#                 actions = []
#                 for line in f:
#                     line = line.strip()
#                     if line and not line.startswith(';'):
#                         actions.append(line)
#                 return actions
#         except FileNotFoundError:
#             print("⚠️ Soluzione PDDL non trovata, modalità libera attivata")
#             return []
    
#     def generate_html_interface(self):
#         """Genera l'interfaccia HTML completa"""
        
#         if not self.lore:
#             print("❌ Impossibile generare HTML senza lore")
#             return None
        
#         # Prepara i dati per l'LLM
#         quest_title = self.lore.get("quest_description", {}).get("title", "Avventura Misteriosa")
#         quest_description = self.lore.get("quest_description", {}).get("description", "")
#         initial_state = self.lore.get("quest_description", {}).get("initial_state", "")
#         goal = self.lore.get("quest_description", {}).get("goal", "")
        
#         branching_min = self.lore.get("branching_factor", {}).get("min", 2)
#         branching_max = self.lore.get("branching_factor", {}).get("max", 4)
#         depth_min = self.lore.get("depth_constraints", {}).get("min", 3)
#         depth_max = self.lore.get("depth_constraints", {}).get("max", 10)
        
#         # Prompt per generare l'HTML
#         prompt = f"""Sei un esperto sviluppatore web specializzato in giochi interattivi. 

# Il tuo compito è creare un'interfaccia HTML completa e funzionante per un'avventura testuale interattiva basata sulla lore fornita.

# LORE DELLA QUEST:
# - Titolo: {quest_title}
# - Descrizione: {quest_description}
# - Stato Iniziale: {initial_state}
# - Obiettivo: {goal}

# VINCOLI NARRATIVI:
# - Branching factor: {branching_min}-{branching_max} azioni per scena
# - Profondità: {depth_min}-{depth_max} passi per completare la quest

# AZIONI PDDL DISPONIBILI:
# {json.dumps(self.solution, indent=2) if self.solution else "Nessuna soluzione PDDL disponibile"}

# REQUISITI TECNICI:
# 1. HTML5 completo e autonomo (single file)
# 2. CSS embedded per un design moderno e responsive
# 3. JavaScript puro per la logica del gioco
# 4. Interfaccia user-friendly con:
#    - Area narrativa principale
#    - Bottoni per le azioni
#    - Sidebar con informazioni quest
#    - Indicatore di progresso
#    - Storia delle azioni precedenti

# CARATTERISTICHE RICHIESTE:
# - Design responsive e moderno
# - Animazioni CSS smooth
# - Gestione dello stato del gioco in JavaScript
# - Generazione dinamica delle scene narrative
# - Sistema di scelte multiple
# - Possibilità di ricominciare la quest
# - Feedback visivo per le azioni

# STRUTTURA NARRATIVA:
# - Ogni scena deve avere una descrizione coinvolgente
# - Le azioni devono essere specifiche e coerenti con la lore
# - La progressione deve seguire una logica narrativa
# - Il gioco deve culminare nel raggiungimento dell'obiettivo

# ISTRUZIONI:
# 1. Crea un sistema di scene pre-definite basate sulla lore
# 2. Implementa una logica di transizione tra scene
# 3. Usa colori e styling che riflettano l'ambientazione della quest
# 4. Includi effetti sonori testuali o emoticon per immersione
# 5. Assicurati che il gioco sia completamente funzionante

# Genera SOLO il codice HTML completo, senza spiegazioni aggiuntive."""

#         try:
#             print("🎨 Generando interfaccia HTML...")
#             response = self.llm.invoke(prompt)
#             html_content = response.content.strip()
            
#             # Pulisci il contenuto HTML
#             if "```html" in html_content:
#                 start_idx = html_content.find("```html") + 7
#                 end_idx = html_content.rfind("```")
#                 html_content = html_content[start_idx:end_idx].strip()
#             elif "```" in html_content:
#                 start_idx = html_content.find("```") + 3
#                 end_idx = html_content.rfind("```")
#                 html_content = html_content[start_idx:end_idx].strip()
            
#             return html_content
            
#         except Exception as e:
#             print(f"❌ Errore nella generazione HTML: {e}")
#             return None
    
#     def save_html_game(self, html_content):
#         """Salva l'interfaccia HTML generata"""
#         try:
#             # Crea la directory se non esiste
#             os.makedirs("file_generati", exist_ok=True)
            
#             # Salva il file HTML
#             filename = "file_generati/interactive_quest.html"
#             with open(filename, 'w', encoding='utf-8') as f:
#                 f.write(html_content)
            
#             print(f"✅ Interfaccia HTML salvata in: {filename}")
#             print(f"🌐 Apri il file nel browser per giocare!")
            
#             return filename
            
#         except Exception as e:
#             print(f"❌ Errore nel salvataggio HTML: {e}")
#             return None
    
#     def generate_complete_game(self):
#         """Genera e salva l'intero gioco HTML"""
#         print("🎮 Avvio generazione gioco HTML...")
        
#         # Genera HTML
#         html_content = self.generate_html_interface()
#         if not html_content:
#             print("❌ Generazione HTML fallita")
#             return None
        
#         # Salva il file
#         filename = self.save_html_game(html_content)
#         if filename:
#             print(f"🎉 Gioco HTML generato con successo!")
#             print(f"📁 File: {filename}")
#             return filename
        
#         return None

# def main():
#     """Funzione principale per generare l'interfaccia HTML"""
#     generator = HTMLGameGenerator()
    
#     # Controlla se i file necessari esistono
#     if not generator.lore:
#         print("❌ Impossibile continuare senza file lore")
#         print("💡 Assicurati di aver completato la Fase 1 del progetto")
#         return
    
#     # Genera l'interfaccia completa
#     result = generator.generate_complete_game()
    
#     if result:
#         print(f"\n🎯 FASE 2 COMPLETATA CON SUCCESSO!")
#         print(f"📝 Lore caricata: ✅")
#         print(f"🧠 Soluzione PDDL: {'✅' if generator.solution else '⚠️ Modalità libera'}")
#         print(f"🎮 Interfaccia HTML: ✅")
#         print(f"\n🌐 Apri il file '{result}' nel browser per iniziare l'avventura!")
#     else:
#         print("❌ Errore nella generazione del gioco")

# if __name__ == "__main__":
#     main()