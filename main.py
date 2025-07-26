import sys
from pathlib import Path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))
from file_generation.lore_generation import generate_lore
import os ,json
from langchain_google_genai import ChatGoogleGenerativeAI
from file_generation.domain_generation import create_domain_pddl
from file_generation.problem_generation import create_problem_pddl
from correction_and_validation.reflective_agent import run_correction_workflow,run_user_correction_pddl,update_lore_with_corrections
from correction_and_validation.pddl_validation import run_fastdownward_complete
from dotenv import load_dotenv
from utils import print_lore, print_plan
from file_generation.story_generation import generate_story
import subprocess
from correction_and_validation.pddl_validation import validate_plan_with_val, get_validation_error_for_correction

load_dotenv() #Per la chiave API


def main():
    API_KEY=os.getenv("API_KEY")

    # Configurazione API key
    os.environ["GOOGLE_API_KEY"] = API_KEY

    # Inizializza il modello Gemini 
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.6
    )

    user_input= input("Inserisci la tua richiesta per generare la lore: ")
    
    
    # crea e salva la lore 
    generate_lore(user_input,llm)

    # chiede all'utente se vuole modificare la lore generata
    print("Di seguito la lore generata:")
    print_lore() #in utils
    
    # HITL per modifiche lore
    while(True):
        scelta_modifica = input("\n\nVuoi modificare la lore? (S/N): ").strip().upper()
        if scelta_modifica == 'N':
            break
        elif scelta_modifica == 'S':
            user_input = input("Inserisci la tua richiesta per modificare la lore: ")
            update_lore_with_corrections(user_input,llm)
            print("Ecco la lore aggiornata:")
            print_lore()
            continue
        else:
            print("Scelta non valida, riprova.")

    # crea il dominio e il problema della lore generata
    create_domain_pddl(llm)
    create_problem_pddl(llm)

    # VALIDAZIONE COMPLETA (FastDownward + VAL)
    validation_final_results = validate_pddl_complete(llm)
    
    if not validation_final_results["success"]:
        print(f"Errore: {validation_final_results['error']}")
        return validation_final_results
    
    # Estrai i risultati finali
    pddl_validation_output = validation_final_results["pddl_output"]
    
    # Human in the Loop (HITL) per la validazione del piano
    plan_accepted = False
    
    while not plan_accepted:
        # Mostra il piano all'utente e chiede approvazione
        plan_accepted = human_plan_validation(pddl_validation_output["solution_results"]["actions"])
        if plan_accepted:
            break

        # Opzione per permettere all'utente di suggerire correzioni
        user_correction = input("Descrivi il problema o la correzione desiderata: ")
        print("🔄 Applicando le correzioni suggerite...")
        run_user_correction_pddl(user_correction, llm) 

        # Rivalidare completamente
        validation_final_results = validate_pddl_complete(llm)
        
        if not validation_final_results["success"]:
            print("❌ Riprova con correzioni diverse...")
            continue
        
        pddl_validation_output = validation_final_results["pddl_output"]
        
    print("Generando la storia...")
    generate_story(llm)
    subprocess.run(["streamlit", "run", "gui_solo_fase_2.py"])

# Esegue la validazione completa PDDL con FastDownward e VAL
def validate_pddl_complete(llm, max_attempts=100):
    attempt = 0
    
    while attempt < max_attempts:
        print(f"\n🔄 Tentativo di validazione {attempt + 1}/{max_attempts}")
        
        # STEP 1: Validazione FastDownward (stampe già gestite dalla classe)
        pddl_validation_output = run_fastdownward_complete()
        
        # Se FastDownward fallisce, correggi e riprova
        if not pddl_validation_output["overall_success"]:
            print("🔄 Correggendo il PDDL per FastDownward...")
            run_correction_workflow(pddl_validation_output["planning_results"]["planning_output"], llm)
            attempt += 1
            continue
        
        # STEP 2: Validazione VAL (stampe già gestite dalla classe)
        validation_results = validate_plan_with_val()
        
        # Se VAL passa, abbiamo finito
        if validation_results["validation_successful"] and validation_results["plan_valid"]:
            print(f"\n🎉 VALIDAZIONE COMPLETA: SUCCESSO! (Tentativi: {attempt + 1}/{max_attempts})")
            return {
                "success": True,
                "pddl_output": pddl_validation_output,
                "val_results": validation_results,
                "attempts": attempt + 1
            }
        
        # Se VAL fallisce, correggi e ricomincia da FastDownward
        print("🔄 Correggendo il PDDL per VAL e riavviando da FastDownward...")
        
        error_message = get_validation_error_for_correction(validation_results)
        print(f"Errore di validazione: {error_message}")
        run_correction_workflow(error_message, llm)
        
        attempt += 1
    
    # Se arriviamo qui, abbiamo esaurito i tentativi
    print(f"\n❌ VALIDAZIONE FALLITA: Esauriti tutti i {max_attempts} tentativi")
    return {
        "success": False,
        "error": "Numero massimo di tentativi raggiunto",
        "attempts": max_attempts
    }


def human_plan_validation(actions_list):
    
    print("\n📋 PIANO GENERATO:")
    print("-" * 50)
    
    if actions_list and len(actions_list) > 0:
        print(f"Numero totale di azioni: {len(actions_list)}")
        print("\nSequenza delle azioni:")
        for i, action in enumerate(actions_list, 1):
            print(f"  {i:2d}. {action}")
        
        # Mostra statistiche
        print(f"\n📊 Statistiche del piano:")
        print(f"   - Lunghezza: {len(actions_list)} azioni")
        
    else:
        print("❌ Nessuna azione trovata nel piano!")
        return False
    
    print("-" * 50)
    
    while True:
        scelta = input("\n✅ Il piano generato è soddisfacente? (S/N): ").strip().upper()
        
        if scelta == 'S':
            print("✅ Piano accettato dall'utente!")
            return True
        elif scelta == 'N':
            print("🔄 Il piano verrà rigenerato con le tue correzioni...")
            return False
        else:
            print("❌ Scelta non valida, inserisci 'S' per Sì o 'N' per No.")

if __name__ == "__main__":
    main()

          