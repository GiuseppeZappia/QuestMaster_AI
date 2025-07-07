(define (domain ombra-tradimento)
  (:requirements :strips :typing)
  (:types ryu masaru rotolo luogo guardia)
  (:predicates
    (at ?x - ryu ?l - luogo)
    (at ?x - masaru ?l - luogo)
    (at ?r - rotolo ?l - luogo)
    (vivo ?x - ryu)
    (vivo ?x - masaru)
    (sconfitto ?x - masaru)
    (possiede ?x - ryu ?r - rotolo)
    (onore-ristabilito)
    (guardie-presenti ?l - luogo)
    (trappole-attive ?l - luogo)
    (at ?g - guardia ?l - luogo)
    (adiacente ?l1 - luogo ?l2 - luogo)
  )

  (:action muovi
    :parameters (?x - ryu ?from - luogo ?to - luogo)
    :precondition (and (at ?x ?from) (adiacente ?from ?to) (vivo ?x))
    :effect (and (at ?x ?to) (not (at ?x ?from)))
  )

  (:action combatti-masaru
    :parameters (?x - ryu ?m - masaru ?l - luogo)
    :precondition (and (at ?x ?l) (at ?m ?l) (vivo ?x) (vivo ?m))
    :effect (and (sconfitto ?m) (not (vivo ?m)))
  )

  (:action prendi-rotolo
    :parameters (?x - ryu ?r - rotolo ?l - luogo)
    :precondition (and (at ?x ?l) (at ?r ?l) (vivo ?x))
    :effect (possiede ?x ?r)
  )

  (:action ripristina-onore
    :parameters (?x - ryu ?m - masaru ?r - rotolo)
    :precondition (and (sconfitto ?m) (possiede ?x ?r))
    :effect (onore-ristabilito)
  )

  (:action combatti-guardia
    :parameters (?x - ryu ?g - guardia ?l - luogo)
    :precondition (and (at ?x ?l) (at ?g ?l) (vivo ?x))
    :effect (not (at ?g ?l))
  )

  (:action disattiva-trappole
    :parameters (?x - ryu ?l - luogo)
    :precondition (and (at ?x ?l) (trappole-attive ?l) (vivo ?x))
    :effect (not (trappole-attive ?l))
  )
)