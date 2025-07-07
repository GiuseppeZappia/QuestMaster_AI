;; domain.pddl: Dominio per la simulazione della Ricerca della Prosperità

(define (domain ricerca-prosperita)
  (:requirements :strips :typing :negative-preconditions :equality :numeric-fluents :action-costs :conditional-effects)
  (:types
    entity
    risorsa - entity
    attivita - entity
    individuo - entity
    mercato - risorsa
  )

  (:predicates
    (at ?i - individuo ?l - attivita) ;; L'individuo si trova in una determinata attività
    (redditizio ?a - attivita) ;; L'attività è redditizia
    (tasse-pagate ?i - individuo) ;; L'individuo ha pagato le tasse
    (mercato-favorevole ?m - mercato) ;; Il mercato è in una fase favorevole
    (milionario ?i - individuo) ;; L'individuo è milionario
  )

  (:functions
    (ha-denaro ?i - individuo) - number
  )

  ;; Azione: Investire in borsa
  (:action investi-borsa
    :parameters (?i - individuo ?m - mercato ?quantita - number)
    :precondition (and (>= (ha-denaro ?i) ?quantita) (mercato-favorevole ?m))
    :effect (and (increase (ha-denaro ?i) (* ?quantita 0.1)) (decrease (ha-denaro ?i) ?quantita)) ;; Aumenta il denaro del 10%
  )

  ;; Azione: Avviare un'attività
  (:action avvia-attivita
    :parameters (?i - individuo ?a - attivita ?costo - number)
    :precondition (and (>= (ha-denaro ?i) ?costo) (not (redditizio ?a)))
    :effect (and (redditizio ?a) (decrease (ha-denaro ?i) ?costo))
  )

  ;; Azione: Lavorare
  (:action lavora
    :parameters (?i - individuo ?guadagno - number)
    :precondition (not (milionario ?i))
    :effect (increase (ha-denaro ?i) ?guadagno)
  )

  ;; Azione: Pagare le tasse
  (:action paga-tasse
    :parameters (?i - individuo ?percentuale - number)
    :precondition (and (>= (ha-denaro ?i) 1) (not (tasse-pagate ?i)))
    :effect (and (tasse-pagate ?i) (decrease (ha-denaro ?i) (* (ha-denaro ?i) ?percentuale)))
  )

  ;; Azione: Gestire imprevisti
  (:action gestisci-imprevisto
    :parameters (?i - individuo ?costo - number)
    :precondition (>= (ha-denaro ?i) ?costo)
    :effect (decrease (ha-denaro ?i) ?costo)
  )

  ;; Azione: Controlla se sei milionario (azione di test, non modifica lo stato)
  (:action controlla-milionario
    :parameters (?i - individuo)
    :precondition (>= (ha-denaro ?i) 1000000)
    :effect (when (>= (ha-denaro ?i) 1000000) (milionario ?i))
  )
)