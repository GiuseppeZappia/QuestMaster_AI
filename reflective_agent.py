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
    
    # Pulizia ulteriore da eventuali residui
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