;; domain.pddl
(define (domain tesoro-maledetto)
  (:requirements :strips :typing :negative-preconditions)
  (:types
    entity location
    pirata ciurma tesoro tribù - entity
    barbanera dentedisqualo - pirata
  )

  (:predicates
    (at ?x - entity ?l - location)  ;; Posizione di pirati, tesoro, tribù
    (alive ?p - pirata)             ;; Pirata è vivo
    (has-treasure ?c - ciurma)      ;; La ciurma ha il tesoro
    (curse-broken)                   ;; La maledizione è spezzata
    (tribù-hostile ?l - location)    ;; Tribù ostile presente
    (pirati-rivali ?l - location)   ;; Pirati rivali presenti
    (traps-present ?l - location)    ;; Trappole presenti nella location
    (nave-ricostruita)              ;; La nave è stata ricostruita
  )

  ;; Movimento tra locazioni
  (:action move
    :parameters (?p - pirata ?from ?to - location)
    :precondition (and (at ?p ?from) (alive ?p))
    :effect (and (not (at ?p ?from)) (at ?p ?to))
  )

  ;; Evitare le trappole
  (:action avoid-traps
    :parameters (?p - pirata ?l - location)
    :precondition (and (at ?p ?l) (traps-present ?l) (alive ?p))
    :effect (not (traps-present ?l))
  )

  ;; Combattere la tribù
  (:action fight-tribe
    :parameters (?p - pirata ?l - location)
    :precondition (and (at ?p ?l) (tribù-hostile ?l) (alive ?p))
    :effect (not (tribù-hostile ?l))
  )

  ;; Combattere i pirati rivali
  (:action fight-rivals
    :parameters (?p - pirata ?l - location)
    :precondition (and (at ?p ?l) (pirati-rivali ?l) (alive ?p))
    :effect (and (not (pirati-rivali ?l)))
  )

  ;; Trovare il tesoro
  (:action find-treasure
    :parameters (?c - ciurma ?t - tesoro ?l - location)
    :precondition (and (at ?c ?l) (at ?t ?l))
    :effect (and (has-treasure ?c) (not (at ?t ?l)))
  )

  ;; Spezzare la maledizione
  (:action break-curse
    :parameters (?c - ciurma)
    :precondition (has-treasure ?c)
    :effect (curse-broken)
  )

  ;; Ricostruire la nave
  (:action rebuild-ship
    :parameters (?c - ciurma)
    :precondition (curse-broken)
    :effect (nave-ricostruita)
  )
)