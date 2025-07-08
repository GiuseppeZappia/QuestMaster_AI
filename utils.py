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
    """Carica il file domain.pddl di esempio"""
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

    # Estrai le sezioni
    quest = lore_data["lore_document"]["quest_description"]
    branching = lore_data["lore_document"]["branching_factor"]
    depth = lore_data["lore_document"]["depth_constraints"]

    # Componi la narrazione
    narrative = f"""
    🗝️ Titolo della missione: {quest["title"]}

    🌍 Contesto:
    {quest["world_background"]}

    ⚠️ Situazione iniziale:
    {quest["initial_state"]}

    🎯 Obiettivo:
    {quest["goal"]}

    🚧 Ostacoli lungo il cammino:
    """

    for obstacle in quest["obstacles"]:
        narrative += f"  - {obstacle}\n"

    narrative += f"""
    📜 Informazioni contestuali:
    {quest["contextual_information"]}

    🔢 Struttura narrativa prevista:
    - Numero minimo di azioni per stato: {branching["min_actions_per_state"]}
    - Numero massimo di azioni per stato: {branching["max_actions_per_state"]}
    - Passaggi minimi per raggiungere l'obiettivo: {depth["min_steps_to_goal"]}
    - Passaggi massimi per raggiungere l'obiettivo: {depth["max_steps_to_goal"]}
    """
    print(narrative)

def print_plan():
    try:
        with open("fastdownward_output/solution.txt", 'r', encoding='utf-8') as f:
            solution = f.read()
            print(solution)
    except FileNotFoundError:
        print("File solution.txt non trovato nella cartella file_generati.")
    except Exception as e:
        print(f"Errore nel caricamento del piano: {e}")