import os 
import subprocess
from utils import load_example_pddl

def run_fastdownward_planning():
   
    domain_file = load_example_pddl("file_generati/domain_generato.pddl")
    problem_file = load_example_pddl("file_generati/problem_generato.pddl")

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
    
    output_dir = "fastdownward_output"
    
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
            
            # Salva la soluzione in un file locale
            os.makedirs(output_dir, exist_ok=True)
            solution_file = os.path.join(output_dir, "solution.txt")
            
            # Processa le azioni (ogni linea del sas_plan rappresenta un'azione)
            lines = solution_content.split('\n')
            actions = []
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith(';'):  # Ignora commenti
                    actions.append(line)
            
            # Salva la soluzione
            with open(solution_file, 'w') as f:
                for action in actions:
                    f.write(action + '\n')
            
            results["solution_retrieved"] = True
            results["solution_path"] = solution_file
            results["actions"] = actions
            
            print(f"Soluzione salvata in: {solution_file}")
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