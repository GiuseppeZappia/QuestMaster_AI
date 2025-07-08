from lore_generation import generate_lore
import os ,json
from langchain_google_genai import ChatGoogleGenerativeAI
from domain_generation import create_domain_pddl
from problem_generation import create_problem_pddl
from reflective_agent import run_correction_workflow,run_user_correction_pddl,update_lore_with_corrections
# from pddl_validation import run_fastdownward_and_validate
from pddl_validation import run_fastdownward_complete
from dotenv import load_dotenv
from utils import print_lore, print_plan, loop_until_valid_pddl

load_dotenv() #Per la chiave API


def main():
    API_KEY=os.getenv("API_KEY")
    # Configurazione API key
    os.environ["GOOGLE_API_KEY"] = API_KEY

    # Inizializza il modello Gemini 2.0 Flash
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.6
    )

    user_input= input("Inserisci la tua richiesta per generare la lore: ")
    
    
    # # #crea e salva la lore 
    generate_lore(user_input,llm)

    # # #chiede all'utente se vuole modificare la lore generata
    print("Di seguito la lore generata:")
    
    print_lore() #in utils
    
    #HITL
    while(True):
        scelta_modifica = input("\n\nVuoi modificare la lore? (S/N): ").strip().upper()
        if scelta_modifica == 'N':
            break
        elif scelta_modifica == 'S':
            user_input = input("Inserisci la tua richiesta per modificare la lore: ")
            #IL REFLECITVE AGENT FA LE MODIFICHE
            update_lore_with_corrections(user_input,llm)
            print("Ecco la lore aggiornata:")
            print_lore()
            print("Vuoi fare altre modifiche? (S/N)")
            continue  # Torna all'inizio del ciclo per chiedere di nuovo
        else:
            print("Scelta non valida, riprova.")
        

    # # #crea il dominio della lore generata
    create_domain_pddl(llm)

    # # #crea il problema della lore generata
    create_problem_pddl(llm)

    pddl_validation_output=run_fastdownward_complete()

    #CAMBIARE IN BASE A LOGICA ANASTASIA
    if not pddl_validation_output["planning_results"]["planning_success"]:
        loop_until_valid_pddl(llm)  # Funzione che continua a correggere fino a validazione riuscita

    
    #HUMAN IN THE LOOP PER VALIDARE IL PIANO GENERATO
    plan_accepted = False
    
    
    while not plan_accepted:
        # Mostra il piano all'utente e chiede approvazione
        plan_accepted = human_plan_validation(pddl_validation_output["planning_results"]["planning_output"])
        if plan_accepted:
            print("Piano accettato, procedo con la pianificazione...")
            break
        # Opzione per permettere all'utente di suggerire correzioni
        user_correction = input("Descrivi il problema o la correzione desiderata: ")
        print("🔄 Applicando le correzioni suggerite...")
        run_user_correction_pddl(user_correction, llm) 
        # Rivalidare
        pddl_validation_output = run_fastdownward_complete()
        if not pddl_validation_output["planning_results"]["planning_success"]:
            loop_until_valid_pddl(llm)
 
        

def human_plan_validation(planning_output):
    
    print("Di seguito il piano generato:")
    print_plan()
    
    while True:
        scelta = input("\n✅ Il piano generato è soddisfacente? (S/N): ").strip().upper()
        
        if scelta == 'S':
            print("✅ Piano accettato!")
            return True
        elif scelta == 'N':
            print("🔄 Il piano verrà rigenerato...")
            return False
        else:
            print("❌ Scelta non valida, inserisci 'S' per Sì o 'N' per No.")

if __name__ == "__main__":
    main()