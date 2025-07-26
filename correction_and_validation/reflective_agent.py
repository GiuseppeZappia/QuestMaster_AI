from utils import load_example_pddl, load_example_json
import json

# Corregge problemi PDDL con human-in-the-loop
def correct_pddl(pddl_problem, llm):

    # Carica i file necessari
    lore = load_example_json("file_generati/lore_generata_per_utente.json")
    domain = load_example_pddl("file_generati/domain_generato.pddl")
    problem = load_example_pddl("file_generati/problem_generato.pddl")
    
    # Genera il prompt per l'LLM
    prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

    Il tuo compito è risolvere gli errori ottenuti in seguito alla valutazione di file di tipo domain.pddl e problem.pddl con Fast Downward o VAL.
    Gli errori possono riguardare la sintassi, la struttura, la logica del PDDL o ancora l'assenza di un percorso valido da input ad output.

    Gli errori possono riguardare molti aspetti, tra cui:
  - oggetti o predicati non definiti
  - mismatch di tipi
  - errori di sintassi (parentesi, variabili…)
  - incoerenze logiche tra domain e problem
  - mancanza di percorso valido

    ------------------ESEMPIO ERRORE------------------
    Di seguito un esempio di errore FASTDOWNWARD e relativa correzione:
    
    CODICE PDDL ERRATO:
    (:action ricicla-denaro
    :parameters (?s - sacerdote ?l - luogo)
    :precondition (and (at ?s ?l) (risorse culto-nduja medio))
    :effect (risorse culto-nduja alto)
    )

    ERRORE FASTDOWNWARD:
    Undefined object
    Got: culto-nduja

    PROBLEMA:
    "culto-nduja" è un oggetto concreto, definito nel problem,
    e non è un parametro dell'azione. Fast Downward lo considera 
    undefined perché il dominio non deve contenere riferimenti a 
    oggetti specifici.

    SOLUZIONE:
    (:action ricicla-denaro
    :parameters (?s - sacerdote ?l - luogo ?o - organizzazione)
    :precondition (and
        (at ?s ?l)
        (risorse ?o medio))
    :effect (and
        (not (risorse ?o medio))
        (risorse ?o alto))
    )

    Ora l’oggetto culto-nduja verrà passato nel problem file, che è il luogo giusto per oggetti specifici.
    ------------------FINE ESEMPIO ERRORE------------------

    Devi correggere il seguente errore: {pddl_problem} associato a questi file di lore, domain e problem PDDL:
    
    LORE:
    {lore}

    domain.pddl:
    {domain}

    problem.pddl:
    {problem}

    OUTPUT:
    Rispondi specificando chiaramente se stai correggendo il DOMAIN o il PROBLEM, seguito dal codice PDDL corretto.
    Usa il formato:
    CORREZIONE: [DOMAIN/PROBLEM]
    ```
    [codice PDDL corretto]
    ```"""

    # Invoca l'LLM per ottenere la correzione
    llm_response = llm.invoke(prompt)
    response_text = llm_response.content.strip()

    # Determina se è una correzione al domain o al problem
    is_domain_correction = False
    is_problem_correction = False
    
    # Prima controlla per le parole chiave esplicite nella risposta
    if "CORREZIONE: DOMAIN" in response_text.upper():
        is_domain_correction = True
    elif "CORREZIONE: PROBLEM" in response_text.upper():
        is_problem_correction = True
    else:
        # Fallback: cerca nelle prime righe della risposta per evitare falsi positivi
        first_lines = '\n'.join(response_text.split('\n')[:3]).upper()
        if "DOMAIN" in first_lines:
            is_domain_correction = True
        elif "PROBLEM" in first_lines:
            is_problem_correction = True
        else:
            print("sono alla fine non ho trovato nulla")
            # Ultimo fallback: cerca pattern più specifici nel codice PDDL
            if "```" in response_text:
                # Estrai il blocco di codice per l'analisi
                start_idx = response_text.find("```")
                if start_idx != -1:
                    first_end = response_text.find("\n", start_idx)
                    if first_end != -1:
                        last_start = response_text.rfind("```")
                        if last_start != start_idx:
                            code_block = response_text[first_end+1:last_start].strip()
                            # Controlla se il codice è un domain o problem
                            if "(define (domain" in code_block:
                                is_domain_correction = True
                            elif "(define (problem" in code_block:
                                is_problem_correction = True
    
    # Estrai il PDDL dalla risposta
    corrected_pddl = response_text
    if "```" in corrected_pddl:
        # Trova tutti i blocchi di codice
        parts = corrected_pddl.split("```")
        if len(parts) >= 3:
            # Prendi il primo blocco di codice (indice 1)
            code_block = parts[1]
            # Rimuovi la prima riga se contiene "pddl" o altri marker
            lines = code_block.split('\n')
            if lines and ('pddl' in lines[0].lower() or lines[0].strip() == ''):
                corrected_pddl = '\n'.join(lines[1:]).strip()
            else:
                corrected_pddl = code_block.strip()
        else:
            # Fallback se non ci sono abbastanza parti
            corrected_pddl = corrected_pddl.replace("```", "").strip()
    
    # Pulizia ulteriore da eventuali residui
    corrected_pddl = corrected_pddl.replace("correzione: problem", "").replace("CORREZIONE: PROBLEM", "").strip()
    
    # Se non è possibile determinare automaticamente il tipo, chiede all'utente 
    if not is_domain_correction and not is_problem_correction:

        # Prepara il messaggio per l'utente
        query_message = f"""⚠️  Non è possibile determinare automaticamente se si tratta di una correzione al domain o al problem

Risposta dell'LLM:
{"-" * 50}
{response_text}
{"-" * 50}

Si tratta di una correzione al DOMAIN o al PROBLEM? (D/P):"""
        
        # Interrompe l'esecuzione e chiede input umano (Human-in-the-loop)
        user_input = input(query_message).strip().upper()
        # Processa la scelta dell'utente con loop infinito fino a input valido
        while True:            
            if user_input in ['D', 'DOMAIN']:
                is_domain_correction = True
                is_problem_correction = False
                break
            elif user_input in ['P', 'PROBLEM']:
                is_domain_correction = False
                is_problem_correction = True
                break
            else:
                # Input non valido, chiedi di nuovo
                error_message = "❌ Scelta non valida. Inserisci 'D' per Domain o 'P' per Problem."

    
    # Determina il nome del file di output
    if is_domain_correction:
        output_filename = "file_generati/domain_generato.pddl"
        file_type = "Domain"
    else:
        output_filename = "file_generati/problem_generato.pddl"
        file_type = "Problem"
    
    # Salva automaticamente il file corretto
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(corrected_pddl)
        
        print(f"✅ {file_type}.pddl corretto con successo e salvato in: {output_filename}")

        
    except Exception as e:
        error_message = f"❌ Errore nel salvataggio del file corretto: {e}"
        print(error_message)
        print(f"Risposta ricevuta:\n{response_text}")
    
    return corrected_pddl, is_domain_correction, is_problem_correction

# Esegue il workflow di correzione PDDL
def run_correction_workflow(pddl_problem, llm):

    try:
        # Avvia il processo di correzione
        corrected_pddl, is_domain, is_problem = correct_pddl(pddl_problem, llm)
        
        return {
            "success": True,
            "corrected_pddl": corrected_pddl,
            "is_domain_correction": is_domain,
            "is_problem_correction": is_problem
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "corrected_pddl": None,
            "is_domain_correction": False,
            "is_problem_correction": False
        }


def update_lore_with_corrections(richieste_utente,llm):
    lore={json.dumps(load_example_json("file_generati/lore_generata_per_utente.json"), indent=2, ensure_ascii=False)}

    prompt =f"""Sei un esperto game designer specializzato nella creazione di avventure narrative interattive per il sistema QuestMaster.

    Il tuo compito è corregere una lore dettagliata in formato JSON, a partire dalle modifiche richieste dell'utente.

    ISTRUZIONI:
    - Devi limitarti a correggere la lore esistentecon le modifiche richieste, senza modificarne la struttura, quindi il formato JSON deve rimanere identico.
    - Rispondi SOLO con il JSON valido
    - Non aggiungere testo prima o dopo il JSON
    - Assicurati che la struttura sia identica all'esempio fornito

    LORE DA MODIFICARE:
    {lore}
    MODIFICHE RICHIESTE DALL'UTENTE:
    {richieste_utente}
    """

    response=llm.invoke(prompt)

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
        
        # Mostra anteprima
        if "quest_description" in lore_data:
            print(f"\n📖 Titolo: {lore_data['quest_description'].get('title', 'N/A')}")
            print(f"📝 Descrizione: {lore_data['quest_description'].get('description', 'N/A')[:150]}...")
        
    except json.JSONDecodeError as e:
        print(f"❌ Errore nel parsing JSON: {e}")
        print(f"Risposta ricevuta:\n{response_text}")


def run_user_correction_pddl(user_corrections, llm):
    try:
        # Carica i file necessari
        lore = load_example_json("file_generati/lore_generata_per_utente.json")
        domain = load_example_pddl("file_generati/domain_generato.pddl")
        problem = load_example_pddl("file_generati/problem_generato.pddl")
        
        # Carica la soluzione attuale
        solution = ""
        try:
            with open("sas_plan", 'r', encoding='utf-8') as f:
                solution = f.read().strip()
        except FileNotFoundError:
            solution = "Soluzione non disponibile"
        
        # Genera il prompt unificato per rigenerare DOMAIN e PROBLEM
        unified_prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

        L'utente ha visto il piano generato (ovvero, la SOLUZIONE ATTUALE) e ha suggerito le seguenti correzioni/modifiche:
        "{user_corrections}"
        
        SOLUZIONE ATTUALE:
        {solution}
        
        LORE:
        {lore}
        
        domain.pddl ATTUALE:
        {domain}
        
        problem.pddl ATTUALE:
        {problem}

        Il tuo compito è rigenerare completamente ENTRAMBI i file domain.pddl e problem.pddl tenendo conto dei suggerimenti dell'utente.

        ISTRUZIONI:
        1. Analizza i suggerimenti dell'utente relativi al piano
        2. Rigenera il domain.pddl dalla lore incorporando le modifiche necessarie
        3. Rigenera il problem.pddl dalla lore incorporando le modifiche necessarie
        4. Assicurati che le azioni siano coerenti con i feedback dell'utente
        5. Assicurati che stati iniziali e goal siano coerenti con i feedback dell'utente
        6. Mantieni la coerenza tra domain e problem
        7. Mantieni la coerenza con la lore fornita

        OUTPUT:
        Fornisci il codice PDDL completo nel seguente formato:

        ===DOMAIN===
        [inserisci qui il codice PDDL del domain completo]

        ===PROBLEM===
        [inserisci qui il codice PDDL del problem completo]

        Non aggiungere commenti aggiuntivi, solo il codice PDDL pulito.
        """

        # Genera DOMAIN e PROBLEM in un'unica chiamata
        unified_response = llm.invoke(unified_prompt)
        response_content = unified_response.content.strip()
        
        # Funzione helper per estrarre contenuto dai blocchi markdown
        def extract_pddl_from_markdown(content):
            """Estrae il contenuto PDDL dai blocchi markdown ```pddl"""
            if "```pddl" in content:
                # Trova tutti i blocchi ```pddl
                parts = content.split("```pddl")
                if len(parts) >= 2:
                    # Prendi il contenuto dopo ```pddl fino al prossimo ```
                    pddl_content = parts[1].split("```")[0].strip()
                    return pddl_content
            elif "```" in content:
                # Blocco generico senza specifica del linguaggio
                parts = content.split("```")
                if len(parts) >= 3:
                    return parts[1].strip()
            return content.strip()
        
        # Separa domain e problem dalla risposta
        if "===DOMAIN===" in response_content and "===PROBLEM===" in response_content:
            # Trova le posizioni dei separatori
            domain_start = response_content.find("===DOMAIN===")
            problem_start = response_content.find("===PROBLEM===")
            
            if domain_start != -1 and problem_start != -1 and domain_start < problem_start:
                # Estrai la sezione domain (da ===DOMAIN=== a ===PROBLEM===)
                domain_section = response_content[domain_start + len("===DOMAIN==="):problem_start].strip()
                # Estrai la sezione problem (da ===PROBLEM=== in poi)
                problem_section = response_content[problem_start + len("===PROBLEM==="):].strip()
                
                
                # Estrai il contenuto PDDL dai blocchi markdown
                domain_content = extract_pddl_from_markdown(domain_section)
                problem_content = extract_pddl_from_markdown(problem_section)
                
    
                
                # Verifica che il contenuto estratto sia valido
                if not domain_content or not problem_content:
                    raise ValueError("Contenuto PDDL estratto vuoto")                
            else:
                raise ValueError("Formato risposta non valido: separatori ===DOMAIN=== e ===PROBLEM=== non trovati nell'ordine corretto")
        else:
            raise ValueError("Formato risposta non valido: mancano i separatori ===DOMAIN=== e ===PROBLEM===")
        
        # Salva il domain
        domain_filename = "file_generati/domain_generato.pddl"
        with open(domain_filename, 'w', encoding='utf-8') as f:
            f.write(domain_content)
        print(f"✅ Domain rigenerato e salvato in: {domain_filename}")

        # Salva il problem
        problem_filename = "file_generati/problem_generato.pddl"
        with open(problem_filename, 'w', encoding='utf-8') as f:
            f.write(problem_content)
        print(f"✅ Problem rigenerato e salvato in: {problem_filename}")

        return {
            "domain_content": domain_content,
            "problem_content": problem_content,
            "success": True
        }
        
    except Exception as e:
        print(f"❌ Errore durante la rigenerazione basata sui suggerimenti dell'utente: {e}")
        return {
            "domain_content": None,
            "problem_content": None,
            "success": False,
            "error": str(e)
        }

# Esegue il workflow di rigenerazione PDDL unificata basato sui suggerimenti dell'utente.
def run_user_correction_workflow(user_corrections, llm):
    
    try:
        # Avvia il processo di rigenerazione unificata
        result = run_user_correction_pddl(user_corrections, llm)
        
        if result["success"]:
            return {
                "success": True,
                "domain_content": result["domain_content"],
                "problem_content": result["problem_content"]
            }
        else:
            return {
                "success": False,
                "error": result.get("error", "Errore sconosciuto"),
                "domain_content": None,
                "problem_content": None
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "domain_content": None,
            "problem_content": None
        }