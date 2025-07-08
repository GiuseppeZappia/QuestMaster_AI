from utils import load_example_pddl, load_example_json
from langgraph.types import Command, interrupt


def correct_pddl(pddl_problem, llm):
    """
    Corregge problemi PDDL con human-in-the-loop usando interrupt e resume.
    """
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
    ```
    """

    # Invoca l'LLM per ottenere la correzione
    llm_response = llm.invoke(prompt)
    response_text = llm_response.content.strip()
    print ("---------------------------------------------STAMPO RISPOSTA LLM------------------------------------------------")
    print(response_text)
    # Determina se è una correzione al domain o al problem
    is_domain_correction = False
    is_problem_correction = False
    
    # Prima controlla per le parole chiave esplicite nella risposta
    if "CORREZIONE: DOMAIN" in response_text.upper():
        print("sono nel domain lettere maiuscole")
        is_domain_correction = True
    elif "CORREZIONE: PROBLEM" in response_text.upper():
        print("sono nel problem lettere maiuscole")
        is_problem_correction = True
    else:
        # Fallback: cerca nelle prime righe della risposta per evitare falsi positivi
        first_lines = '\n'.join(response_text.split('\n')[:3]).upper()
        if "DOMAIN" in first_lines:
            print("sono nel domain lettere sotto")
            is_domain_correction = True
        elif "PROBLEM" in first_lines:
            print("sono nel problem lettere sotto")
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
    
    # Pulisci ulteriormente da eventuali residui
    corrected_pddl = corrected_pddl.replace("correzione: problem", "").replace("CORREZIONE: PROBLEM", "").strip()

    
    # Se non è possibile determinare automaticamente il tipo, usa interrupt
    if not is_domain_correction and not is_problem_correction:
        # Prepara il messaggio per l'utente
        query_message = f"""⚠️  Non è possibile determinare automaticamente se si tratta di una correzione al domain o al problem

Risposta dell'LLM:
{"-" * 50}
{response_text}
{"-" * 50}

Si tratta di una correzione al DOMAIN o al PROBLEM? (D/P):"""
        
        # Interrompe l'esecuzione e chiede input umano
        human_choice = interrupt({
            "query": query_message,
            "type": "file_type_choice",
            "options": ["D", "P", "DOMAIN", "PROBLEM"]
        })
        
        # Processa la scelta dell'utente con loop infinito fino a input valido
        while True:
            user_input = human_choice.get("data", "").strip().upper()
            
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
                human_choice = interrupt({
                    "query": error_message + "\n" + query_message,
                    "type": "file_type_choice_retry",
                    "options": ["D", "P", "DOMAIN", "PROBLEM"]
                })
    
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


def run_correction_workflow(pddl_problem, llm):
    """
    Esegue il workflow di correzione PDDL con gestione di interrupt/resume.
    """
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
    
def run_correction_workflow(pddl_problem, llm):
    """
    Esegue il workflow di correzione PDDL con gestione di interrupt/resume.
    """
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
    





def run_user_correction_pddl(user_corrections, llm):
    """
    Rigenerazione PDDL basata sui suggerimenti dell'utente.
    Dopo i feedback dell'utente, rigenera completamente domain e problem dalla lore.
    """
    try:
        # Carica i file necessari
        lore = load_example_json("file_generati/lore_generata_per_utente.json")
        domain = load_example_pddl("file_generati/domain_generato.pddl")
        problem = load_example_pddl("file_generati/problem_generato.pddl")
        
        # Carica la soluzione attuale
        solution = ""
        try:
            with open("fastdownward_output/solution.txt", 'r', encoding='utf-8') as f:
                solution = f.read().strip()
        except FileNotFoundError:
            solution = "Soluzione non disponibile"
        
        # Genera il prompt per rigenerare il DOMAIN
        domain_prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

        L'utente ha visto il piano generato (ovvero, la SOLUZIONE ATTUALE) e ha suggerito le seguenti correzioni/modifiche:
        "{user_corrections}"

        SOLUZIONE ATTUALE:
        {solution}

        LORE:
        {lore}

        domain.pddl ATTUALE:
        {domain}

        Il tuo compito è rigenerare completamente il file domain.pddl tenendo conto dei suggerimenti dell'utente.
        
        ISTRUZIONI:
        1. Analizza i suggerimenti dell'utente relativi al piano
        2. Rigenera il domain.pddl dalla lore incorporando le modifiche necessarie
        3. Assicurati che le azioni siano coerenti con i feedback dell'utente
        4. Mantieni la coerenza con la lore fornita

        OUTPUT:
        Fornisci solo il codice PDDL del domain completo, senza commenti aggiuntivi.
        """

        # Genera il DOMAIN
        print("🔄 Rigenerando domain.pddl basandosi sui suggerimenti dell'utente...")
        domain_response = llm.invoke(domain_prompt)
        domain_content = domain_response.content.strip()
        
        # Pulisci il domain da eventuali marker markdown
        if "```" in domain_content:
            parts = domain_content.split("```")
            if len(parts) >= 3:
                domain_content = parts[1]
                lines = domain_content.split('\n')
                if lines and ('pddl' in lines[0].lower() or lines[0].strip() == ''):
                    domain_content = '\n'.join(lines[1:]).strip()
                else:
                    domain_content = domain_content.strip()
        
        # Salva il domain
        domain_filename = "file_generati/domain_generato.pddl"
        with open(domain_filename, 'w', encoding='utf-8') as f:
            f.write(domain_content)
        print(f"✅ Domain rigenerato e salvato in: {domain_filename}")

        # Genera il prompt per rigenerare il PROBLEM
        problem_prompt = f"""Sei un esperto di pianificazione automatica e PDDL (Planning Domain Definition Language).

        L'utente ha visto il piano generato e ha suggerito le seguenti correzioni/modifiche:
        "{user_corrections}"

        SOLUZIONE ATTUALE:
        {solution}

        LORE:
        {lore}

        DOMAIN RIGENERATO:
        {domain_content}

        problem.pddl ATTUALE:
        {problem}

        Il tuo compito è rigenerare completamente il file problem.pddl tenendo conto dei suggerimenti dell'utente.
        
        ISTRUZIONI:
        1. Analizza i suggerimenti dell'utente relativi al piano
        2. Rigenera il problem.pddl dalla lore incorporando le modifiche necessarie
        3. Assicurati che stati iniziali e goal siano coerenti con i feedback dell'utente
        4. Mantieni la coerenza con la lore e il domain forniti

        OUTPUT:
        Fornisci solo il codice PDDL del problem completo, senza commenti aggiuntivi.
        """

        # Genera il PROBLEM
        print("🔄 Rigenerando problem.pddl basandosi sui suggerimenti dell'utente...")
        problem_response = llm.invoke(problem_prompt)
        problem_content = problem_response.content.strip()
        
        # Pulisci il problem da eventuali marker markdown
        if "```" in problem_content:
            parts = problem_content.split("```")
            if len(parts) >= 3:
                problem_content = parts[1]
                lines = problem_content.split('\n')
                if lines and ('pddl' in lines[0].lower() or lines[0].strip() == ''):
                    problem_content = '\n'.join(lines[1:]).strip()
                else:
                    problem_content = problem_content.strip()
        
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


def run_user_correction_workflow(user_corrections, llm):
    """
    Esegue il workflow di rigenerazione PDDL basato sui suggerimenti dell'utente.
    """
    try:
        # Avvia il processo di rigenerazione
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