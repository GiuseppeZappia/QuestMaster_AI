(define (domain eco-silenzioso-titano)
  (:requirements :strips :typing :equality) ; Aggiunto :equality per il controllo in assembla-codice

  (:types
    personaggio ia luogo livello-accesso frammento-codice
  )

  (:predicates
    ;; Posizione del personaggio e connettività dei luoghi
    (at ?p - personaggio ?l - luogo)
    (connessi ?from - luogo ?to - luogo)

    ;; Stato degli ostacoli e dei sistemi
    (porta-sigillata ?from - luogo ?to - luogo)
    (richiede-accesso ?from - luogo ?to - luogo ?la - livello-accesso)
    (perdita-refrigerante ?l - luogo)
    (drone-minaccia ?l - luogo)
    (helios-offline ?i - ia)
    (nucleo-controllo ?l - luogo)
    (supporto-vitale-ripristinato)

    ;; Posizione degli oggetti nel mondo
    (scheda-in ?la - livello-accesso ?l - luogo)
    (frammento-in ?fc - frammento-codice ?l - luogo)

    ;; Inventario del personaggio
    (ha-scheda ?p - personaggio ?la - livello-accesso)
    (ha-frammento ?p - personaggio ?fc - frammento-codice)
    (codice-assemblato ?p - personaggio)
  )

  ;; AZIONI POSSIBILI

  (:action muovi
    :parameters (?p - personaggio ?from - luogo ?to - luogo)
    :precondition (and
        (at ?p ?from)
        (connessi ?from ?to)
        (not (porta-sigillata ?from ?to))
        (not (perdita-refrigerante ?to))
        (not (drone-minaccia ?to))
    )
    :effect (and
        (not (at ?p ?from))
        (at ?p ?to)
    )
  )

  (:action prendi-scheda
    :parameters (?p - personaggio ?la - livello-accesso ?l - luogo)
    :precondition (and
        (at ?p ?l)
        (scheda-in ?la ?l)
    )
    :effect (and
        (not (scheda-in ?la ?l))
        (ha-scheda ?p ?la)
    )
  )

  (:action prendi-frammento
    :parameters (?p - personaggio ?fc - frammento-codice ?l - luogo)
    :precondition (and
        (at ?p ?l)
        (frammento-in ?fc ?l)
    )
    :effect (and
        (not (frammento-in ?fc ?l))
        (ha-frammento ?p ?fc)
    )
  )

  (:action sblocca-porta
    :parameters (?p - personaggio ?la - livello-accesso ?from - luogo ?to - luogo)
    :precondition (and
        (at ?p ?from)
        (porta-sigillata ?from ?to)
        (richiede-accesso ?from ?to ?la)
        (ha-scheda ?p ?la)
    )
    :effect (not (porta-sigillata ?from ?to))
  )
  
  ;; NUOVA AZIONE: Ripara la perdita di refrigerante da un luogo adiacente.
  (:action ripara-perdita-refrigerante
    :parameters (?p - personaggio ?l_da_cui_ripara - luogo ?l_con_perdita - luogo)
    :precondition (and
        (at ?p ?l_da_cui_ripara)
        (connessi ?l_da_cui_ripara ?l_con_perdita)
        (perdita-refrigerante ?l_con_perdita)
    )
    :effect (not (perdita-refrigerante ?l_con_perdita))
  )

  ;; NUOVA AZIONE: Disattiva il drone da un luogo adiacente.
  (:action disattiva-drone
    :parameters (?p - personaggio ?l_da_cui_agisce - luogo ?l_con_drone - luogo)
    :precondition (and
        (at ?p ?l_da_cui_agisce)
        (connessi ?l_da_cui_agisce ?l_con_drone)
        (drone-minaccia ?l_con_drone)
    )
    :effect (not (drone-minaccia ?l_con_drone))
  )

  ;; AZIONE CORRETTA: Assicura che i frammenti siano diversi e li consuma.
  (:action assembla-codice
    :parameters (?p - personaggio ?f1 - frammento-codice ?f2 - frammento-codice)
    :precondition (and
        (ha-frammento ?p ?f1)
        (ha-frammento ?p ?f2)
        (not (= ?f1 ?f2)) ; Assicura che i frammenti siano diversi
    )
    :effect (and
        (codice-assemblato ?p)
        (not (ha-frammento ?p ?f1)) ; Consuma i frammenti
        (not (ha-frammento ?p ?f2))
    )
  )

  (:action riavvia-helios-e-supporto-vitale
    :parameters (?p - personaggio ?i - ia ?l - luogo)
    :precondition (and
        (at ?p ?l)
        (nucleo-controllo ?l)
        (helios-offline ?i)
        (codice-assemblato ?p)
    )
    :effect (and
        (not (helios-offline ?i))
        (supporto-vitale-ripristinato)
    )
  )
)