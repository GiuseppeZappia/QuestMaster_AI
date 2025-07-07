from utils import load_example_json
from utils import load_example_pddl
import json

# QUESTO POI DA TOGLIERE TANTO GLIELO PASSIAMO NOI NON SE LO DEVE CARICARE
# with open("lore_generata_per_utente.json", 'r', encoding='utf-8') as f:
#     user_lore_json=json.load(f)        

# with open("loreDiProva.json", 'r', encoding='utf-8') as f:
#     lore_esempio_json=json.load(f)    
# 
# 
# INCLUDERE   - Rispetta i vincoli di branching factor e depth constraints della lore nelle istruzioni 

def create_domain_pddl(llm):
    esempio_domain_pddl = load_example_pddl("file_esempio/domain.pddl")

    # Prompt per generare PDDL domain
    pddl_prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

    Il tuo compito è convertire una lore in formato JSON in un file domain.pddl valido per Fast Downward.

    REQUISITI PER IL DOMAIN.PDDL:
    - Deve essere **pieno PDDL-STRIPS**, compatibile con Fast Downward (nessuna estensione numerica, temporale o fluents)
    - :requirements deve essere esattamente  
        (:requirements :strips :typing :negative-preconditions :equality)
    - **Non** usare costrutti come `:numeric-fluents`, `:durative-actions`, `increase`, `decrease`, funzioni numeriche, o operatori `<` `>` su valori numerici
    - Includi unicamente **predicati booleani** e **effetti/add e delete lists**
    - Definisci azioni con precondizioni ed effetti chiari, tipizzati, e **senza condizionali o effetti numerici**
    - Usa commenti per spiegare ogni sezione
    - Segui rigorosamente la sintassi standard PDDL-STRIPS
    - Rispetta i vincoli di branching factor e depth constraints della lore
    - Rispondi **soltanto** con il codice PDDL valido, senza testo introduttivo o spiegazioni esterne

    ISTRUZIONI:
    1. Analizza la lore JSON e identifica stati, oggetti, personaggi e azioni possibili.
    2. Crea solo predicati booleani per rappresentare lo stato del mondo narrativo.
    3. Definisci azioni STRIPS—ognuna con:
    - Parametri tipizzati
    - Precondizioni in forma congiuntiva di predicati booleani
    - Effetti sotto forma di liste di aggiunta (`(pred ...)`) e rimozione (`(not (pred ...))`)
    4. **Non** usare costrutti ADL avanzati (disjunction, quantificatori, condizionali) né alcuna notazione numerica.
    5. Rispondi **solo** con il codice PDDL, ogni riga commentata con `;`.

    ESEMPIO DI INPUT E OUTPUT:

    Input JSON della lore:
    {json.dumps(load_example_json("file_esempio/loreDiProva.json"), indent=2, ensure_ascii=False)}

    Output domain.pddl:
    {esempio_domain_pddl}

    LORE JSON ATTUALE DA CONVERTIRE:
    {json.dumps(load_example_json("file_generati/lore_generata_per_utente.json"), indent=2, ensure_ascii=False)}

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
        pddl_output_filename = "file_generati/domain_generato.pddl"
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



