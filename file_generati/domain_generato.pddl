;; domain.pddl: Salvataggio della Principessa Lyra

(define (domain salvataggio-lyra)
  (:requirements :strips :typing :negative-preconditions)
  (:types
    entity - object
    luogo - entity
    personaggio - entity
    principe - personaggio
    principessa - personaggio
    stregone - personaggio
    goblin - personaggio
    golem - personaggio
    regno - luogo
  )

  (:predicates
    (at ?x - entity ?l - luogo)  ;; Posizione di un'entità (principe, principessa, ecc.) in un luogo
    (prigioniero ?p - principessa ?l - luogo) ;; La principessa è prigioniera in un luogo
    (sano ?p - principessa)  ;; La principessa è sana e salva
    (alleato ?r - regno)  ;; Il regno è alleato
    (goblin-presente ?l - luogo) ;; Goblin presenti in un luogo
    (trappola-attiva ?l - luogo) ;; Trappola magica attiva in un luogo
    (fiume-attraversabile) ;; Il fiume è attraversabile
    (golem-attivo) ;; Il golem è attivo
    (sconfitto ?g - golem) ;; Il golem è sconfitto
    (sconfitto ?s - stregone) ;; Lo stregone è sconfitto
    (vivo ?s - stregone) ;; Lo stregone è vivo
  )

  ;; Azione: Muoversi da un luogo all'altro
  (:action muovi
    :parameters (?p - principe ?da - luogo ?a - luogo)
    :precondition (and (at ?p ?da) (not (= ?da ?a)))
    :effect (and (at ?p ?a) (not (at ?p ?da)))
  )

  ;; Azione: Combattere i goblin
  (:action combatti-goblin
    :parameters (?p - principe ?l - luogo)
    :precondition (and (at ?p ?l) (goblin-presente ?l))
    :effect (not (goblin-presente ?l))
  )

  ;; Azione: Disattivare una trappola
  (:action disattiva-trappola
    :parameters (?p - principe ?l - luogo)
    :precondition (and (at ?p ?l) (trappola-attiva ?l))
    :effect (not (trappola-attiva ?l))
  )

  ;; Azione: Attraversare il fiume
  (:action attraversa-fiume
    :parameters (?p - principe ?da - luogo ?a - luogo)
    :precondition (and (at ?p ?da) (fiume-attraversabile) (not (= ?da ?a)))
    :effect (and (at ?p ?a) (not (at ?p ?da)))
  )

  ;; Azione: Combattere il golem
  (:action combatti-golem
    :parameters (?p - principe ?l - luogo ?g - golem)
    :precondition (and (at ?p ?l) (golem-attivo) (at ?g ?l))
    :effect (and (sconfitto ?g) (not (golem-attivo)))
  )

  ;; Azione: Combattere Malkor
  (:action combatti-malkor
    :parameters (?p - principe ?s - stregone ?l - luogo)
    :precondition (and (at ?p ?l) (at ?s ?l) (vivo ?s))
    :effect (and (sconfitto ?s) (not (vivo ?s)))
  )

  ;; Azione: Salvare la principessa
  (:action salva-principessa
    :parameters (?p - principe ?lyra - principessa ?l - luogo)
    :precondition (and (at ?p ?l) (prigioniero ?lyra ?l) (sconfitto ?s - stregone))
    :effect (and (sano ?lyra) (not (prigioniero ?lyra ?l)))
  )

  ;; Azione: Riportare la principessa al regno
  (:action riporta-al-regno
    :parameters (?p - principe ?lyra - principessa ?da - luogo ?a - regno)
    :precondition (and (at ?p ?da) (at ?lyra ?da) (sano ?lyra))
    :effect (and (at ?p ?a) (at ?lyra ?a) (not (at ?p ?da)) (not (at ?lyra ?da)))
  )
)

(define (problem salvataggio-lyra-problem)
  (:domain salvataggio-lyra)

  (:objects
    valerian - principe
    lyra - principessa
    malkor - stregone
    golem - golem
    eldoria - regno
    foresta montagne fiume fortezza - luogo
  )

  (:init
    (at valerian eldoria)        ;; Il principe Valerian inizia nel regno di Eldoria
    (at malkor fortezza)          ;; Malkor si trova nella fortezza
    (vivo malkor)               ;; Malkor è vivo
    (at lyra fortezza)            ;; La principessa Lyra è prigioniera nella fortezza
    (prigioniero lyra fortezza)   ;; Lyra è prigioniera nella fortezza
    (goblin-presente foresta)   ;; Ci sono goblin nella foresta
    (trappola-attiva montagne)    ;; Ci sono trappole nelle montagne
    (fiume-attraversabile)      ;; Il fiume è attraversabile
    (golem-attivo)              ;; Il golem è attivo
    (at golem fortezza)
  )

  (:goal (and
    (at valerian eldoria)       ;; Valerian deve tornare a Eldoria
    (at lyra eldoria)           ;; Lyra deve tornare a Eldoria
    (sano lyra)               ;; Lyra deve essere sana e salva
  ))
)