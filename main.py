from lore_generation import generate_lore
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from domain_generation import create_domain_pddl
from problem_generation import create_problem_pddl
from reflective_agent import run_correction_workflow
# from pddl_validation import run_fastdownward_and_validate
from pddl_validation import run_fastdownward_complete
from dotenv import load_dotenv

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

    # user_input= input("Inserisci la tua richiesta per generare la lore: ")
    
    
    # # # #crea e salva la lore 
    # generate_lore(user_input,llm)

    # # # #crea il dominio della lore generata
    # create_domain_pddl(llm)

    # # # #crea il problema della lore generata
    # create_problem_pddl(llm)

    #PARTE VALIDAZIONE E GESTIONE ERRORE ANASTASIA

    pddl_validation_output=run_fastdownward_complete()
    # print(pddl_validation_output)

    # print("-----------------------------------------------STAMPO NEL MAINNNNNNN-----------------------------------------------")
    # print(pddl_validation_output["planning_results"]["planning_output"])

    #CAMBIARE IN BASE A LOGICA ANASTASIA
    if not pddl_validation_output["planning_results"]["planning_success"]:
        output=pddl_validation_output
        count_attempts=0
        while(not output["planning_results"]["planning_success"] and count_attempts<8):
            print("❌ Errore nella validazione PDDL")
            print("🔄 Riprovo a correggere il PDDL...")
            run_correction_workflow(output["planning_results"]["planning_output"], llm)
            output=run_fastdownward_complete()
            count_attempts+=1
        #FACCIAMO MIN ATTEMPTS E POI HUMAN IN THE LOOP CON UMANO CHE LEGGE DOMAIN E PROBLEM E 
        #SUGGERISCE CORREZIONE DA FARE? COSI CHIAMEREMMO ANCORA IL METODO  correction_workflow ma con stringa errore passata da utente
        
    


    

if __name__ == "__main__":
    main()