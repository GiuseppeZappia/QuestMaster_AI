
from utils import load_example_json
from utils import load_example_pddl
import json

# QUESTO POI DA TOGLIERE TANTO GLIELO PASSIAMO NOI NON SE LO DEVE CARICARE
# with open("lore_generata_per_utente.json", 'r', encoding='utf-8') as f:
#     user_lore_json=json.load(f)        

# with open("loreDiProva.json", 'r', encoding='utf-8') as f:
#     lore_esempio_json=json.load(f)     

# INCLUDERE: - Deve rispettare i vincoli di branching factor e depth constraints della lore

def create_problem_pddl(llm):

    lore_esempio_json = load_example_json("file_esempio/loreDiProva.json")
    user_lore_json = load_example_json("file_generati/lore_generata_per_utente.json")

    #Prompt per generare PDDL problem
    problem_prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

    Il tuo compito è creare un file problem.pddl che sia compatibile col domain.pddl generato e che rappresenti lo scenario specifico della lore.

    REQUISITI PER IL PROBLEM.PDDL:
    - Deve essere pieno PDDL‑STRIPS, compatibile con Fast Downward (solo costrutti booleani, no numerici, no durative)
    - Usa esattamente gli stessi tipi, predicati e nomi di oggetti definiti nel domain
    - (:objects) elenca tutti gli oggetti usati nella lore, tipizzati correttamente
    - (:init) include solo literal booleani e negazioni semplici, nessun costrutto ADL avanzato
    - (:goal) deve essere una congiunzione di predicati booleani che rappresentano l’obiettivo finale
    - Sintassi rigorosa PDDL‑STRIPS:
        (define (problem ⟨nome⟩)
        (:domain ⟨domain-name⟩)
        (:objects …)
        (:init …)
        (:goal (and …))
        )
    - Ogni riga commentata con `;` per spiegare cosa definisce
    - Rispondi **solo** con il codice PDDL, senza testo aggiuntivo

    ISTRUZIONI:
    1. Mappa la lore JSON su istanze di oggetti e stato iniziale.
    2. In :objects dichiara ogni entità (personaggi, luoghi, prove, ecc.) con il tipo corretto.
    3. In :init, metti tutte le asserzioni vere all’inizio (at, prova-superata negata, sfida, ecc.).
    4. In :goal, unisci con `(and ...)` i predicati che definiscono il successo (es. `(permesso-ottenuto)`).
    5. **Non** usare costrutti non supportati: nessun `:metric`, `:constraints`, `:fluents`, `forall`, `or`, `imply`, o aritmetica.

    ESEMPIO DI INPUT E OUTPUT:

    Input JSON della lore:
    {json.dumps(lore_esempio_json, indent=2, ensure_ascii=False)}

    Domain.pddl di riferimento:
    {load_example_pddl("file_esempio/domain.pddl")}

    Output problem.pddl di esempio:
    {load_example_pddl("file_esempio/problem.pddl")}

    LORE JSON ATTUALE DA CONVERTIRE:
    {json.dumps(user_lore_json, indent=2, ensure_ascii=False)}

    DOMAIN.PDDL GENERATO:
    {load_example_pddl("file_generati/domain_generato.pddl")}

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
        problem_output_filename = "file_generati/problem_generato.pddl"
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
        
        print(f"\n GENERAZIONE COMPLETATA!")
        print(f"File generati:")
        print(f"   - lore_generata.json")
        print(f"   - domain_generato.pddl") 
        print(f"   - problem_generato.pddl")
        
    except Exception as e:
        print(f"Errore nel salvataggio del problem.pddl: {e}")
        print(f"Risposta ricevuta:\n{problem_text}")
