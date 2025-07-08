(define (domain re-corvo)
  (:requirements :strips :typing)
  (:types eroe re-corvo luogo oggetto)
  (:predicates
    (at ?e - eroe ?l - luogo)
    (sigillato ?r - re-corvo)
    (tomo-ottenuto)
    (at-obj ?o - oggetto ?l - luogo)
  )

  (:action sigilla-re-corvo
    :parameters (?e - eroe ?r - re-corvo ?l - luogo)
    :precondition (and (at ?e ?l) (tomo-ottenuto) (at ?r ?l))
    :effect (sigillato ?r)
  )

  (:action prendi-tomo
    :parameters (?e - eroe ?t - oggetto ?l - luogo)
    :precondition (and (at ?e ?l) (at-obj ?t ?l) (not (tomo-ottenuto)))
    :effect (and (tomo-ottenuto) (not (at-obj ?t ?l)))
  )

  (:action vai
    :parameters (?e - eroe ?da - luogo ?a - luogo)
    :precondition (and (at ?e ?da) (not (= ?da ?a)))
    :effect (and (at ?e ?a) (not (at ?e ?da)))
  )
)