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