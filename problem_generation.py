
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
    {load_example_pddl("file_esempio/domain.pddl")}

    Output problem.pddl:
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
