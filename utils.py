import json

# Carica il JSON di esempio dalla stessa cartella
def load_example_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {filename} non trovato nella cartella corrente")
        return None
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing del JSON: {e}")
        return None
    

# Carica il file PDDL di esempio dalla stessa cartella
def load_example_pddl(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {filename} non trovato nella cartella corrente")
        return None
    except Exception as e:
        print(f"Errore nel caricamento del file PDDL: {e}")
        return None
    

def print_lore():
    lore_data = load_example_json("file_generati/lore_generata_per_utente.json")
    # Estrae le sezioni
    quest = lore_data["lore_document"]["quest_description"]
    branching = lore_data["lore_document"]["branching_factor"]
    depth = lore_data["lore_document"]["depth_constraints"]
    
    # Compone la narrazione in Markdown compatto
    narrative = f"""
### 🗝️ Titolo della Missione:
**{quest["title"]}**

### 🌍 Contesto del Mondo:
{quest["world_background"]}

### ⚠️ Situazione Iniziale:
{quest["initial_state"]}

### 🎯 Obiettivo della Quest:
**{quest["goal"]}**

### 🚧 Ostacoli lungo il Cammino:"""
    
    for i, obstacle in enumerate(quest["obstacles"]):
        icons = ["⚔️", "🛡️", "🏃‍♂️", "🧠", "💎", "🗝️", "🔍", "💀"]
        icon = icons[i % len(icons)]
        narrative += f"\n- {icon} {obstacle}"
    
    narrative += f"""

### 📜 Informazioni Contestuali:
*{quest["contextual_information"]}*

### 🔢 Struttura Narrativa Prevista:
- **📊 Azioni per Stato:** Min: {branching["min_actions_per_state"]} | Max: {branching["max_actions_per_state"]}
- **🎯 Passi all'Obiettivo:** Min: {depth["min_steps_to_goal"]} | Max: {depth["max_steps_to_goal"]}"""
    
    # Print finale per console in formato leggibile
    console_story = f"""
{'='*80}
                    🎭 LEGGENDA GENERATA 🎭
{'='*80}

🗝️  TITOLO: {quest["title"]}

🌍 MONDO:
{quest["world_background"]}

⚠️  SITUAZIONE INIZIALE:
{quest["initial_state"]}

🎯 OBIETTIVO:
{quest["goal"]}

🚧 OSTACOLI:"""
    
    for i, obstacle in enumerate(quest["obstacles"], 1):
        console_story += f"\n   {i}. {obstacle}"
    
    console_story += f"""

📜 CONTESTO:
{quest["contextual_information"]}

🔢 PARAMETRI NARRATIVI:
   • Azioni per stato: {branching["min_actions_per_state"]}-{branching["max_actions_per_state"]}
   • Passi all'obiettivo: {depth["min_steps_to_goal"]}-{depth["max_steps_to_goal"]}

{'='*80}
"""
    
    print(console_story)
    return narrative

def print_plan():
    try:
        with open("sas_plan", 'r', encoding='utf-8') as f:
            solution = f.read()
            print(solution)
            return solution
    except FileNotFoundError:
        print("File sas_plan non trovato.")
    except Exception as e:
        print(f"Errore nel caricamento del piano: {e}")


