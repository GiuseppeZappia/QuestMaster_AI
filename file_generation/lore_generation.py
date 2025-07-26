from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
import os
import json
from utils import load_example_json


# Carica l'esempio JSON 
example_json = load_example_json("file_esempio/loreDiProva.json") 

def generate_lore(user_input,llm):
    # Prompt personalizzato
    prompt = f"""Sei un esperto game designer specializzato nella creazione di avventure narrative interattive per il sistema QuestMaster.

    Il tuo compito è creare una lore dettagliata in formato JSON, a partire dalla richiesta dell'utente che verrà poi convertita in un problema di pianificazione PDDL.

    FORMATO RICHIESTO:
    Devi generare un JSON che segua esattamente la struttura dell'esempio fornito. È fondamentale che includa:
    1. Una descrizione completa della quest con stato iniziale, obiettivo e ostacoli
    2. Il branching factor (numero min/max di azioni disponibili per ogni stato narrativo)
    3. I vincoli di profondità (numero min/max di passi per completare la quest)
    4. Tutti gli elementi necessari per creare un problema PDDL valido 

    ISTRUZIONI:
    - Rispondi SOLO con il JSON valido
    - Non aggiungere testo prima o dopo il JSON
    - Assicurati che la struttura sia identica all'esempio fornito
    - Crea una narrativa coinvolgente e logicamente coerente

    ESEMPIO INPUT UTENTE:
    Crea una quest fantasy dove un erore deve salvare una principessa rapita da un drago. 

    ESEMPIO DI OUTPUT DA PRODURRE:
    {json.dumps(example_json, indent=2, ensure_ascii=False)}

    NUOVO INPUT UTENTE DI CUI DEVI GENERARE IL JSON DELLA LORE:
    {user_input}
    """

    # Genera la lore
    try:
        response = llm.invoke(prompt)
    except Exception as e:
        print(f"❌ Errore durante la generazione della lore: {e}")
        
    # Estrai e pulisci la risposta
    response_text = response.content.strip()

    # Prova a estrarre il JSON dalla risposta
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.rfind("```")
        json_text = response_text[json_start:json_end].strip()
    elif response_text.startswith("{"):
        json_text = response_text
    else:
        # Cerca il primo { e l'ultimo }
        start_idx = response_text.find("{")
        end_idx = response_text.rfind("}") + 1
        if start_idx != -1 and end_idx != 0:
            json_text = response_text[start_idx:end_idx]
        else:
            json_text = response_text

    try:
        # Converti in dizionario per validare
        lore_data = json.loads(json_text)
        
        # Salva la lore generata
        output_filename = "file_generati/lore_generata_per_utente.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(lore_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Lore generata con successo e salvata in: {output_filename}")
        
        
    except json.JSONDecodeError as e:
        print(f"❌ Errore nel parsing JSON: {e}")
        print(f"Risposta ricevuta:\n{response_text}")