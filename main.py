from lore_generation import generate_lore
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from domain_generation import create_domain_pddl
from problem_generation import create_problem_pddl
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

    user_input= input("Inserisci la tua richiesta per generare la lore: ")
    
    
    #crea e salva la lore 
    generate_lore(user_input,llm)

    #crea il dominio della lore generata
    create_domain_pddl(llm)

    #crea il problema della lore generata
    create_problem_pddl(llm)

    results = run_fastdownward_complete()
    


    

if __name__ == "__main__":
    main()