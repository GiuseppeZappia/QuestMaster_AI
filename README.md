# QuestMaster

**QuestMaster** è un sistema in due fasi che combina tecniche di pianificazione simbolica (PDDL) con modelli di intelligenza artificiale generativa (LLM), per aiutare gli autori a creare esperienze narrative interattive e coerenti.

## ✨ Panoramica

Il progetto si compone di due fasi principali:

1. **Fase 1 – Generazione della Storia:**  
   L'utente fornisce un'idea narrativa e dei vincoli (ramificazione e profondità). Il sistema genera automaticamente:
   - una **lore** coerente
   - i file `domain.pddl` e `problem.pddl`
   - un piano valido per la quest, verificato tramite planner classici (Fast Downward + VAL)

2. **Fase 2 – Avventura Interattiva:**  
   La storia viene trasformata in un'applicazione web interattiva (in Streamlit), dove l’utente gioca la propria avventura attraverso scelte narrative.

---

## ⚙️ Tecnologie utilizzate

- **Linguaggio**: Python
- **Planner**: [Fast Downward](https://www.fast-downward.org/)
- **Validatore**: [VAL](https://github.com/KCL-Planning/VAL)
- **Modello generativo**: `gemini-2.5-pro` (via `ChatGoogleGenerativeAI`)
- **Frontend**: Streamlit (interfaccia web)
- **Prompting**: Few-Shot Prompting, Human-in-the-Loop, Reflective Agent, RAG

---

## 🚀 Come eseguire il progetto

### 1. Prerequisiti

- Python ≥ 3.9
- Ambiente Linux o WSL (per eseguire planner)
- Librerie: installabili con `pip install -r requirements.txt`
- Fast Downward e VAL installati in WSL

### 2. Avvio GUI

```bash
streamlit run gui/gui_completa.py
```


## 📜 Fase 1: Generazione della Storia

- Inserimento descrizione iniziale e vincoli (ramificazione e profondità)
- Generazione della lore tramite LLM + few-shot examples (`examples/*.json`)
- Generazione automatica dei file `domain.pddl` e `problem.pddl`
- Validazione con Fast Downward e VAL
- Ciclo iterativo di correzione con il Reflective Agent
- Possibilità di modifica manuale o approvazione finale
- Output finale:
  - `domain_generato.pddl`
  - `problem_generato.pddl`
  - `piano.txt`
  - `lore_finale.json`

---

## 🕹️ Fase 2: Gioco Interattivo

- La storia diventa esplorabile via web, con scelte narrative dinamiche
- Ogni nodo contiene:
  - descrizione immersiva
  - una scelta coerente con il piano
  - diramazioni fallimentari o alternative
- Stato salvato tramite sessione Streamlit
- Possibilità di:
  - scaricare file `.zip` con output (`.json`, `.md`, `.txt`)
  - riascoltare la lore tramite riproduzione vocale
  - riavviare o modificare la storia

---

## 📁 Output

Alla fine dell’esperienza è possibile scaricare:

- La lore narrativa in `.json`, `.md` e `.txt`
- Il piano PDDL validato
- Il grafo narrativo interattivo in formato JSON

---

## 💡 Caratteristiche principali

- ✅ Human-in-the-loop: modifiche approvate dall’utente
- 🔁 Ciclo iterativo di validazione automatica
- 🔐 Defensive prompting contro prompt malevoli
- 🧠 Reflective Agent per gestire errori semantici e suggerire modifiche
- 🔊 Narrazione vocale della storia
- 📚 RAG (Retrieval-Augmented Generation) per lore coerente
- 🎮 Modalità GUI o CLI per maggiore flessibilità

---

## 👥 Autori

- Anastasia Martucci
- Giuseppe Zappia

---

## 📎 Esempio

Nella cartella `examples/` è incluso un esempio completo di una quest:

- `input_lore.json`
- `domain_generato.pddl`
- `problem_generato.pddl`
- `story_output.json`

---

## 📌 Note finali

Il progetto è stato sviluppato nell’ambito del corso di Intelligenza Artificiale (A.A. 2024/2025), all’interno del corso di laurea magistrale in Ingegneria Informatica presso l’Università della Calabria.