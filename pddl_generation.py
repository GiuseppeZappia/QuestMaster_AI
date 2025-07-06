from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
import os
import json


API_KEY=os.getenv("API_KEY")
# Configurazione API key
os.environ["GOOGLE_API_KEY"] = API_KEY

# Inizializza il modello Gemini 2.0 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1
)



# QUESTO POI DA TOGLIERE TANTO GLIELO PASSIAMO NOI NON SE LO DEVE CARICARE
with open("lore_generata_per_utente.json", 'r', encoding='utf-8') as f:
    user_lore_json=json.load(f)        

with open("lore_generata_per_utente.json", 'r', encoding='utf-8') as f:
    lore_esempio_json=json.load(f)     

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

esempio_domain_pddl = load_example_pddl("domain.pddl")

# Prompt per generare PDDL domain
pddl_prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

Il tuo compito è convertire una lore in formato JSON in un file domain.pddl valido per Fast Downward.

REQUISITI PER IL DOMAIN.PDDL:
- Deve essere compatibile con Fast Downward
- Includi predicati per rappresentare stati del mondo, posizioni, oggetti, condizioni
- Definisci azioni con precondizioni ed effetti chiari
- Ogni azione deve avere parametri tipizzati se necessario
- Usa commenti per spiegare ogni sezione
- Segui la sintassi PDDL standard: (define (domain nome-dominio) ...)
- Includi types, predicates, e actions
- Le azioni devono rispecchiare le possibili scelte narrative della lore

ISTRUZIONI:
- Analizza la lore JSON e identifica: stati, oggetti, personaggi, azioni possibili
- Crea predicati che rappresentino lo stato del mondo narrativo
- Definisci azioni che corrispondano alle scelte del giocatore
- Rispetta i vincoli di branching factor e depth constraints della lore
- Rispondi SOLO con il codice PDDL valido, senza testo aggiuntivo
- Ogni riga deve avere un commento che spiega cosa fa

ESEMPIO DI INPUT E OUTPUT:

Input JSON della lore:
{json.dumps(lore_esempio_json, indent=2, ensure_ascii=False)}

Output domain.pddl:
{esempio_domain_pddl}


LORE JSON ATTUALE DA CONVERTIRE:
{json.dumps(user_lore_json, indent=2, ensure_ascii=False)}

OUTPUT DOMAIN.PDDL:"""

# Genera il domain.pddl 
pddl_response = llm.invoke(pddl_prompt)

# Estrai e pulisci la risposta PDDL
pddl_text = pddl_response.content.strip()

# Prova a estrarre il PDDL dalla risposta
if "```" in pddl_text:
    # Rimuovi i code blocks se presenti
    start_idx = pddl_text.find("```")
    if start_idx != -1:
        # Trova la fine del primo ```
        first_end = pddl_text.find("\n", start_idx)
        if first_end != -1:
            # Trova l'ultimo ```
            last_start = pddl_text.rfind("```")
            if last_start != start_idx:
                pddl_text = pddl_text[first_end+1:last_start].strip()
try:
    # Salva il domain.pddl generato
    pddl_output_filename = "domain_generato.pddl"
    with open(pddl_output_filename, 'w', encoding='utf-8') as f:
        f.write(pddl_text)
    
    print(f"✅ Domain.pddl generato con successo e salvato in: {pddl_output_filename}")
    
    # Mostra anteprima
    lines = pddl_text.split('\n')
    print(f"\n🎯 Anteprima domain.pddl:")
    for i, line in enumerate(lines[:10]):  # Mostra le prime 10 righe
        print(f"{i+1:2d}: {line}")
    if len(lines) > 10:
        print(f"... e altre {len(lines)-10} righe")
    
except Exception as e:
    print(f"❌ Errore nel salvataggio del domain.pddl: {e}")
    print(f"Risposta ricevuta:\n{pddl_text}")





#Prompt per generare PDDL problem
problem_prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

Il tuo compito è creare un file problem.pddl che sia compatibile con il domain.pddl generato e che rappresenti lo scenario specifico della lore.

REQUISITI PER IL PROBLEM.PDDL:
- Deve essere compatibile con Fast Downward
- Deve usare gli stessi predicati e oggetti definiti nel domain
- Definisci gli objects specifici per questa istanza del problema
- Imposta lo stato iniziale (:init) basato sulla lore
- Definisci il goal basato sull'obiettivo della quest
- Usa la sintassi PDDL standard: (define (problem nome-problema) ...)
- Includi: problem name, domain reference, objects, init, goal
- Ogni riga deve avere un commento che spiega cosa fa

ESEMPIO DI INPUT E OUTPUT:

Input JSON della lore:
{json.dumps(lore_esempio_json, indent=2, ensure_ascii=False) }

Domain.pddl corrispondente:
{load_example_pddl("domain.pddl")}

Output problem.pddl:
{load_example_pddl("problem.pddl")}



LORE JSON ATTUALE DA CONVERTIRE:
{json.dumps(user_lore_json, indent=2, ensure_ascii=False)}

DOMAIN.PDDL GENERATO:
{load_example_pddl("domain_generato.pddl")}

OUTPUT PROBLEM.PDDL:"""

# Genera il problem.pddl
print("Generazione problem.pddl in corso...")
problem_response = llm.invoke(problem_prompt)

# Estrai e pulisci la risposta PROBLEM
problem_text = problem_response.content.strip()

# Prova a estrarre il PDDL dalla risposta
if "```" in problem_text:
    # Rimuovi i code blocks se presenti
    start_idx = problem_text.find("```")
    if start_idx != -1:
        # Trova la fine del primo ```
        first_end = problem_text.find("\n", start_idx)
        if first_end != -1:
            # Trova l'ultimo ```
            last_start = problem_text.rfind("```")
            if last_start != start_idx:
                problem_text = problem_text[first_end+1:last_start].strip()

try:
    # Salva il problem.pddl generato
    problem_output_filename = "problem_generato.pddl"
    with open(problem_output_filename, 'w', encoding='utf-8') as f:
        f.write(problem_text)
    
    print(f"✅ Problem.pddl generato con successo e salvato in: {problem_output_filename}")
    
    # Mostra anteprima
    lines = problem_text.split('\n')
    print(f"\n🎯 Anteprima problem.pddl:")
    for i, line in enumerate(lines[:10]):  # Mostra le prime 10 righe
        print(f"{i+1:2d}: {line}")
    if len(lines) > 10:
        print(f"... e altre {len(lines)-10} righe")
    
    print(f"\n🎉 GENERAZIONE COMPLETATA!")
    print(f"📁 File generati:")
    print(f"   - lore_generata.json")
    print(f"   - domain_generato.pddl") 
    print(f"   - problem_generato.pddl")
    
except Exception as e:
    print(f"❌ Errore nel salvataggio del problem.pddl: {e}")
    print(f"Risposta ricevuta:\n{problem_text}")
