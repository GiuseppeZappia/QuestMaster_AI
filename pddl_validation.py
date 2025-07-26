import os 
import subprocess
from utils import load_example_pddl

def run_fastdownward_planning():
   
    domain_file = load_example_pddl("file_generati/domain_generato.pddl")
    problem_file = load_example_pddl("file_generati/problem_generato.pddl")
    
    # domain_file = load_example_pddl("file_esempio/domain.pddl")
    # problem_file = load_example_pddl("file_esempio/problem.pddl")

    results = {
        "planning_success": False,
        "solution_found": False,
        "error_message": None,
        "planning_output": None
    }
    
    try:
        
        if domain_file is None:
            results["error_message"] = f"Errore nel caricamento del dominio"
            return results
            
        if problem_file is None:
            results["error_message"] = f"Errore nel caricamento del problema"
            return results

        print(f"Avvio Fast Downward via WSL...")
        
        # Leggi le variabili d'ambiente WSL
        domain_wsl = os.getenv('WSL_DOMAIN_PATH')
        problem_wsl = os.getenv('WSL_PROBLEM_PATH')
        fd_path = os.getenv('WSL_DOWNWARD_PATH')
        
        # Verifica configurazione variabili d'ambiente
        if not domain_wsl or not problem_wsl or not fd_path:
            results["error_message"] = "Variabili WSL non configurate correttamente."
            print("Variabili WSL non configurate correttamente.")
            return results
        
        # Crea il comando per Fast Downward (solo pianificazione)
        command_str = f'python3 "{fd_path}" "{domain_wsl}" "{problem_wsl}" --search "astar(blind())"'
        
        # Esegui Fast Downward via WSL
        result = subprocess.run(
            [
                "wsl",
                "-d", "Ubuntu",
                "bash", "-c", command_str
            ],
            capture_output=True,
            text=True,
            timeout=300 
        )
        
        # Combina output e errori
        output = result.stdout + result.stderr
        results["planning_output"] = output
        
        # Stampa sempre l'output per debugging
        print(f"Fast Downward exit code: {result.returncode}")
        if output.strip():
            print("Output di Fast Downward (Pianificazione):")
            print("-" * 50)
            print(output)
            print("-" * 50)
        
        # Verifica se è stata trovata una soluzione
        if "Solution found" in output or "Plan found" in output:
            results["planning_success"] = True
            results["solution_found"] = True
            print("Piano trovato con Fast Downward!")
        else:
            print("Nessun piano trovato.")
            if result.returncode != 0:
                results["error_message"] = f"Fast Downward fallito con exit code: {result.returncode}"
                
    except subprocess.TimeoutExpired:
        results["error_message"] = "Timeout: Fast Downward ha impiegato troppo tempo"
        print("Timeout: Fast Downward ha impiegato troppo tempo")
        
    except Exception as e:
        results["error_message"] = f"Errore nell'esecuzione di Fast Downward: {str(e)}"
        print(f"Errore nella pianificazione Fast Downward: {e}")
    
    return results


def get_fastdownward_solution():
    
    results = {
        "solution_retrieved": False,
        "solution_path": None,
        "actions": [],
        "error_message": None
    }
    
    try:
        print("Recupero della soluzione da sas_plan...")
        
        # Comando per leggere il file sas_plan
        command_str = "cat sas_plan"
        
        # Esegui il comando via WSL
        result = subprocess.run(
            [
                "wsl",
                "-d", "Ubuntu",
                "bash", "-c", command_str
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            # Parsea l'output del sas_plan
            solution_content = result.stdout.strip()
            
            print("Output di sas_plan:")
            print("-" * 50)
            print(solution_content)
            print("-" * 50)
            
            # Processa le azioni (ogni linea del sas_plan rappresenta un'azione)
            lines = solution_content.split('\n')
            actions = []
            
            for line in lines:
                line = line.strip()
                # Ignora righe vuote, commenti (;) e righe che iniziano con "cost"
                if line and not line.startswith(';') and not line.startswith('cost'):
                    actions.append(line)
            
            results["solution_retrieved"] = True
            results["solution_path"] = "sas_plan"  # Punta al file originale
            results["actions"] = actions
            
            print(f"Soluzione letta da: sas_plan")
            print(f"Numero totale di azioni: {len(actions)}")
            
            # Mostra anteprima della soluzione
            print("\nPrime azioni della soluzione:")
            for i, action in enumerate(actions[:5]):
                print(f"  {i+1}. {action}")
            if len(actions) > 5:
                print(f"  ... e altre {len(actions) - 5} azioni")
                
        else:
            results["error_message"] = "File sas_plan non trovato o vuoto"
            print("File sas_plan non trovato o vuoto")
            
    except subprocess.TimeoutExpired:
        results["error_message"] = "Timeout nel recupero della soluzione"
        print("Timeout nel recupero della soluzione")
        
    except Exception as e:
        results["error_message"] = f"Errore nel recupero della soluzione: {str(e)}"
        print(f"Errore nel recupero della soluzione: {e}")
    
    return results


def run_fastdownward_complete():

    print("Avvio processo FastDownward completo...")
    
    # Fase 1: Pianificazione
    print("\n" + "="*60)
    print("FASE 1: PIANIFICAZIONE")
    print("="*60)
    
    planning_results = run_fastdownward_planning()
    
    if not planning_results["planning_success"]:
        print(f"Pianificazione fallita: {planning_results['error_message']}")
        return {
            "overall_success": False,
            "planning_results": planning_results,
            "solution_results": None
        }
    
    # Fase 2: Recupero soluzione
    print("\n" + "="*60)
    print("FASE 2: RECUPERO SOLUZIONE")
    print("="*60)
    
    solution_results = get_fastdownward_solution()
    
    if not solution_results["solution_retrieved"]:
        print(f"Recupero soluzione fallito: {solution_results['error_message']}")
    
    # Risultati finali
    overall_success = planning_results["planning_success"] and solution_results["solution_retrieved"]
    
    final_results = {
        "overall_success": overall_success,
        "planning_results": planning_results,
        "solution_results": solution_results
    }
    
    print("\n" + "="*60)
    print("RISULTATI FINALI")
    print("="*60)
    print(f"Pianificazione: {'SUCCESS' if planning_results['planning_success'] else 'FAILED'}")
    print(f"Recupero soluzione: {'SUCCESS' if solution_results['solution_retrieved'] else 'FAILED'}")
    print(f"Processo completo: {'SUCCESS' if overall_success else 'FAILED'}")
    
    return final_results



def validate_plan_with_val():
    """
    Valida il piano generato (sas_plan) utilizzando il validatore VAL.
    
    Returns:
        dict: Risultato della validazione con informazioni dettagliate
    """
    
    results = {
        "validation_successful": False,
        "plan_valid": False,
        "validation_output": "",
        "error_message": None,
        "validation_details": {}
    }
    
    try:
        # Leggi le variabili d'ambiente WSL
        domain_wsl = os.getenv('WSL_DOMAIN_PATH')
        problem_wsl = os.getenv('WSL_PROBLEM_PATH')
        val_path = os.getenv('WSL_VAL_PATH')
        sas_plan_wsl = os.getenv('WSL_SAS_PLAN_PATH')
        
        # Verifica configurazione variabili d'ambiente
        if not domain_wsl or not problem_wsl or not val_path or not sas_plan_wsl:
            results["error_message"] = "Variabili WSL per VAL non configurate correttamente."
            print("❌ Variabili WSL per VAL non configurate correttamente.")
            print("Assicurati di aver configurato: WSL_DOMAIN_PATH, WSL_PROBLEM_PATH, WSL_VAL_PATH, WSL_SAS_PLAN_PATH")
            return results
        
        # Verifica che i file necessari esistano localmente
        required_files = [
            "file_generati/domain_generato.pddl",
            "file_generati/problem_generato.pddl", 
            "sas_plan"
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                results["error_message"] = f"File mancante: {file_path}"
                return results
        
        print("🔍 Validazione del piano con VAL...")
        
        # Comando per eseguire VAL tramite WSL
        # Validate usa: validate <domain> <problem> <plan>
        command_str = f'"{val_path}" "{domain_wsl}" "{problem_wsl}" "{sas_plan_wsl}"'
        
        # Esegui VAL
        result = subprocess.run(
            [
                "wsl", "-d", "Ubuntu",
                "bash", "-c", command_str
            ],
            capture_output=True,
            text=True,
            timeout=60  # Timeout di 60 secondi
        )
        
        # Cattura l'output
        validation_output = result.stdout + result.stderr
        results["validation_output"] = validation_output
        
        print("Output di VAL:")
        print(validation_output)
        print("-" * 50)
        
        # Analizza l'output per determinare se il piano è valido
        if result.returncode == 0:
            results["validation_successful"] = True
            
            # Controlla specifici indicatori di validità nel output
            if "Plan valid" in validation_output or "Plan is valid" in validation_output or "Plan Valid" in validation_output:
                results["plan_valid"] = True
                print("✅ Piano validato con successo!")
            elif "Plan invalid" in validation_output or "Plan is invalid" in validation_output or "Plan Invalid" in validation_output:
                results["plan_valid"] = False
                print("❌ Piano non valido!")
            else:
                # Analisi più dettagliata dell'output
                if "Error" in validation_output or "error" in validation_output or "ERROR" in validation_output or "Bad" in validation_output:
                    results["plan_valid"] = False
                    print("❌ Errori rilevati durante la validazione!")
                else:
                    results["plan_valid"] = True
                    print("✅ Piano sembra valido (nessun errore rilevato)")
        else:
            results["validation_successful"] = False
            results["error_message"] = f"VAL ha restituito codice di errore: {result.returncode}"
            print(f"❌ Errore nell'esecuzione di VAL: {result.returncode}")
        
        # Estrai dettagli aggiuntivi dall'output
        results["validation_details"] = parse_val_output(validation_output)
        
    except subprocess.TimeoutExpired:
        results["error_message"] = "Timeout durante la validazione con VAL"
        print("❌ Timeout durante la validazione")
        
    except Exception as e:
        results["error_message"] = f"Errore durante la validazione: {str(e)}"
        print(f"❌ Errore durante la validazione: {e}")
    
    return results


def parse_val_output(output):
    """
    Analizza l'output di VAL per estrarre informazioni dettagliate.
    
    Args:
        output (str): Output completo di VAL
        
    Returns:
        dict: Dettagli parsed dall'output
    """
    details = {
        "goals_achieved": [],
        "preconditions_satisfied": True,
        "execution_errors": [],
        "warnings": [],
        "plan_execution_trace": []
    }
    
    lines = output.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Cerca goal raggiunti
        if "Goal" in line and ("achieved" in line or "satisfied" in line):
            details["goals_achieved"].append(line)
        
        # Cerca errori di precondizioni
        if "Precondition" in line and ("not satisfied" in line or "false" in line or "failed" in line):
            details["preconditions_satisfied"] = False
            details["execution_errors"].append(line)
        
        # Cerca altri errori comuni
        if any(keyword in line for keyword in ["Error:", "ERROR:", "Failed:", "Invalid:", "Cannot"]):
            details["execution_errors"].append(line)
        
        # Cerca warning
        if "Warning:" in line or "WARNING:" in line:
            details["warnings"].append(line)
        
        # Cerca tracce di esecuzione
        if line.startswith("Checking action") or line.startswith("Action:"):
            details["plan_execution_trace"].append(line)
    
    return details

def get_validation_error_for_correction(validation_results):
    """
    Restituisce gli errori di validazione in un formato utilizzabile per la correzione PDDL.
    Include sia il codice di errore che la descrizione completa.
    """
    if validation_results["validation_successful"]:
        return "Non ci sono errori di validazione. Il piano è valido."

    if not validation_results["validation_successful"]:
        # Costruisci un messaggio di errore più dettagliato
        error_message = "ERRORI DI VALIDAZIONE VAL:\n"
        
        # Includi l'output completo di validazione se disponibile
        if "validation_output" in validation_results and validation_results["validation_output"]:
            error_message += f"Output VAL:\n{validation_results['validation_output']}\n\n"
        
        # Includi il messaggio di errore base
        if "error_message" in validation_results:
            error_message += f"Errore: {validation_results['error_message']}\n"
        
        # Includi dettagli aggiuntivi se disponibili
        if "validation_details" in validation_results:
            details = validation_results["validation_details"]
            if details.get("execution_errors"):
                error_message += "\nErrori di esecuzione:\n"
                for error in details["execution_errors"]:
                    error_message += f"- {error}\n"
            
            if details.get("warnings"):
                error_message += "\nWarning:\n"
                for warning in details["warnings"]:
                    error_message += f"- {warning}\n"
        
        return error_message
    
    if validation_results.get("plan_valid"):
        return None  # Nessun errore
    
    # Costruisci un messaggio di errore dettagliato per piani non validi
    error_message = "ERRORI DI VALIDAZIONE VAL:\n"
    
    # Includi l'output completo di validazione (codice + descrizione)
    if "validation_output" in validation_results and validation_results["validation_output"]:
        error_message += f"Output VAL:\n{validation_results['validation_output']}\n"
    
    error_message += "\nDETTAGLI:\n"
    
    if "validation_details" in validation_results:
        details = validation_results["validation_details"]
        if details.get("execution_errors"):
            error_message += "Errori di esecuzione:\n"
            for error in details["execution_errors"]:
                error_message += f"- {error}\n"
        
        if details.get("warnings"):
            error_message += "Warning:\n"
            for warning in details["warnings"]:
                error_message += f"- {warning}\n"
    
    return error_message
