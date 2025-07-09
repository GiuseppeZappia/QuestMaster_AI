(define (domain principessa-orco)
  (:requirements :strips :typing)
  (:types eroe luogo principessa orco motocicletta golem)
  (:predicates
    (at ?x - eroe ?l - luogo)
    (at ?x - principessa ?l - luogo)
    (at ?x - orco ?l - luogo)
    (at ?x - motocicletta ?l - luogo)
    (at ?x - golem ?l - luogo)
    (alive ?o - orco)
    (princess-has-medallion ?p - principessa)
    (werewolves-present ?l - luogo)
    (werewolves-defeated)
    (bridge-up ?l - luogo)
    (drawbridge-lowered)
    (traps-active ?l - luogo)
    (traps-disarmed)
    (golem-active ?l - luogo)
    (golem-defeated)
    (bridge-approached ?l - luogo)
    (fortress-approached ?l - luogo)
    (rescued ?p - principessa)
    (returned ?e - eroe ?l - luogo)
  )

  (:action defeat-werewolves
    :parameters (?e - eroe ?l - luogo)
    :precondition (and (at ?e ?l) (werewolves-present ?l))
    :effect (and (werewolves-defeated) (not (werewolves-present ?l)))
  )

  (:action move
    :parameters (?e - eroe ?from - luogo ?to - luogo)
    :precondition (and (at ?e ?from) (not (= ?from ?to)))
    :effect (and (at ?e ?to) (not (at ?e ?from)))
  )

  (:action lower-drawbridge
    :parameters (?e - eroe ?l - luogo)
    :precondition (and (at ?e ?l) (bridge-up ?l) (not (drawbridge-lowered)))
    :effect (and (drawbridge-lowered) (not (bridge-up ?l)))
  )

  (:action disarm-traps
    :parameters (?e - eroe ?l - luogo ?p - principessa)
    :precondition (and (at ?e ?l) (at ?p ?l) (traps-active ?l) (princess-has-medallion ?p) (drawbridge-lowered))
    :effect (and (traps-disarmed) (not (traps-active ?l)))
  )

  (:action defeat-golem
    :parameters (?e - eroe ?l - luogo)
    :precondition (and (at ?e ?l) (golem-active ?l) (traps-disarmed) (drawbridge-lowered))
    :effect (and (golem-defeated) (not (golem-active ?l)))
  )
  
  (:action rescue-princess
    :parameters (?e - eroe ?p - principessa ?l - luogo)
    :precondition (and (at ?e ?l) (at ?p ?l) (not (rescued ?p)) (golem-defeated) (drawbridge-lowered) (traps-disarmed))
    :effect (rescued ?p)
  )

  (:action return-princess
    :parameters (?e - eroe ?p - principessa ?from - luogo ?to - luogo)
    :precondition (and (at ?e ?from) (at ?p ?from) (rescued ?p) (not (returned ?e ?to)) (not (= ?from ?to)))
    :effect (and (at ?e ?to) (at ?p ?to) (not (at ?e ?from)) (not (at ?p ?from)) (returned ?e ?to))
  )
)