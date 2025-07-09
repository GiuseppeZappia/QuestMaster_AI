(define (domain calice-francesco)
  (:requirements :strips :typing)
  (:types guerriera calice priore setta luogo)
  (:predicates
    (at ?x - guerriera ?l - luogo)
    (at ?c - calice ?l - luogo)
    (guarded ?l - luogo ?s - setta)
    (trapped ?l - luogo)
    (priore-corrupted ?p - priore)
    (spirits-present ?l - luogo)
    (visited ?l - luogo)
    (has-calice ?x - guerriera ?c - calice)
    (delivered ?c - calice ?l - luogo)
    (protected ?c - calice ?l - luogo)
    (defeated ?s - setta)
    (defeated-priore ?p - priore)
  )

  (:action move
    :parameters (?x - guerriera ?from - luogo ?to - luogo)
    :precondition (and (at ?x ?from) (not (at ?x ?to)) (visited ?from))
    :effect (and (at ?x ?to) (not (at ?x ?from)) (visited ?to))
  )

  (:action retrieve-calice
    :parameters (?x - guerriera ?c - calice ?l - luogo)
    :precondition (and (at ?x ?l) (at ?c ?l) (not (has-calice ?x ?c)))
    :effect (and (has-calice ?x ?c) (not (at ?c ?l)))
  )

  (:action deliver-calice
    :parameters (?x - guerriera ?c - calice ?l - luogo)
    :precondition (and (at ?x ?l) (has-calice ?x ?c))
    :effect (and (delivered ?c ?l) (not (has-calice ?x ?c)))
  )

  (:action defeat-setta
    :parameters (?x - guerriera ?l - luogo ?s - setta)
    :precondition (and (at ?x ?l) (guarded ?l ?s))
    :effect (and (defeated ?s) (not (guarded ?l ?s)))
  )
   (:action explore-crypts
    :parameters (?x - guerriera ?l - luogo)
    :precondition (and (at ?x ?l) (spirits-present ?l))
    :effect (and (visited ?l) (not (spirits-present ?l)))
  )

  (:action disarm-traps
    :parameters (?x - guerriera ?l - luogo)
    :precondition (and (at ?x ?l) (trapped ?l))
    :effect (not (trapped ?l))
  )
)