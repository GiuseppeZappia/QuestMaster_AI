;; problem.pddl: Problema per la simulazione della Ricerca della Prosperità

(define (problem ricerca-prosperita-problema)
  (:domain ricerca-prosperita)

  (:objects
    me - individuo  ;; L'individuo che cerca la prosperità
    borsa - mercato ;; Il mercato azionario
    ristorante - attivita ;; Un'attività commerciale (ristorante)
    bar - attivita ;; Un'altra attività commerciale (bar)
  )

  (:init
    (ha-denaro me 1000) ;; L'individuo parte con 1000 dollari
    (at me ristorante) ;; Inizialmente l'individuo si trova al ristorante (potrebbe essere ovunque)
    (mercato-favorevole borsa) ;; Il mercato azionario è in una fase favorevole all'inizio
  )

  (:goal (and
    (milionario me) ;; L'obiettivo è diventare milionario
  ))
)