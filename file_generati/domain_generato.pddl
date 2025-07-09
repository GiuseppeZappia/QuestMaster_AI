(define (domain chiave-drago)
  (:requirements :strips :typing :negative-preconditions)
  (:types
    entity luogo
    eroe principessa drago artefatto - entity
  )

  (:predicates
    (at ?x - entity ?l - luogo)  ;; Posizione di un'entita in un luogo
    (dragon-awake ?d - drago)   ;; Il drago e sveglio
    (has-key ?e - eroe)         ;; L'eroe possiede la chiave
    (princess-rescued ?p - principessa) ;; La principessa e stata salvata
    (dragon-sealed ?d - drago)  ;; Il drago e stato sigillato
  )

  ;; Azione: Muoversi tra due luoghi
  (:action move
    :parameters (?e - eroe ?from - luogo ?to - luogo)
    :precondition (and (at ?e ?from))
    :effect (and (not (at ?e ?from)) (at ?e ?to))
  )

  ;; Azione: Recuperare la Chiave di Luce
  (:action get-key
    :parameters (?e - eroe ?k - artefatto ?l - luogo)
    :precondition (and (at ?e ?l) (at ?k ?l))
    :effect (and (has-key ?e) (not (at ?k ?l)))
  )

  ;; Azione: Salvare la principessa
  (:action rescue-princess
    :parameters (?e - eroe ?p - principessa ?l - luogo)
    :precondition (and (at ?e ?l) (at ?p ?l) (has-key ?e))
    :effect (princess-rescued ?p)
  )

  ;; Azione: Sigillare il drago con la chiave
  (:action seal-dragon
    :parameters (?e - eroe ?d - drago ?l - luogo)
    :precondition (and (has-key ?e) (dragon-awake ?d) (at ?e ?l) (at ?d ?l))
    :effect (and (dragon-sealed ?d) (not (dragon-awake ?d)))
  )
)