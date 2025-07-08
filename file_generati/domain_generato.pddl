;; domain.pddl: L'Incubo Accademico
(define (domain incubo-accademico)
  (:requirements :strips :typing :negative-preconditions :equality)
  (:types
    persona luogo documento - object
    studente professore rettore - persona
    universita dipartimento - luogo
    esame lezione - documento
  )

  (:predicates
    (at ?p - persona ?l - luogo)  ; Persona si trova in un luogo
    (incompetente ?p - professore) ; Professore è incompetente
    (ha-prove ?s - studente)       ; Studente ha prove
    (influenza ?p - professore ?d - dipartimento) ; Professore ha influenza nel dipartimento
    (bocciato ?s - studente)       ; Studente è stato bocciato
    (reclamo-presentato ?s - studente) ; Studente ha presentato un reclamo
    (revisione-ottenuta)          ; Revisione dei voti è stata ottenuta
    (paura ?s - studente)            ; Studente ha paura
    (esame-scorretto ?e - esame)   ; Esame è stato corretto male
    (lezione-senza-senso ?l - lezione) ; Lezione non ha senso
    (rettore-informato)           ; Il rettore è stato informato
  )

  ;; Azione: Muoversi tra i luoghi
  (:action move
    :parameters (?p - persona ?from - luogo ?to - luogo)
    :precondition (at ?p ?from)
    :effect (and (not (at ?p ?from)) (at ?p ?to))
  )

  ;; Azione: Raccogliere prove dell'incompetenza
  (:action raccogli-prove
    :parameters (?s - studente ?l - luogo ?e - esame)
    :precondition (and (at ?s ?l) (esame-scorretto ?e))
    :effect (and (ha-prove ?s))
  )

  ;; Azione: Presentare un reclamo formale
  (:action presenta-reclamo
    :parameters (?s - studente ?d - dipartimento)
    :precondition (and (at ?s ?d) (ha-prove ?s) (not (paura ?s)))
    :effect (reclamo-presentato ?s)
  )

  ;; Azione: Informare il rettore della situazione
  (:action informa-rettore
    :parameters (?s - studente ?r - rettore ?u - universita)
    :precondition (and (at ?s ?u) (at ?r ?u) (reclamo-presentato ?s))
    :effect (rettore-informato)
  )

  ;; Azione: Dimostrare l'incompetenza del professore
  (:action dimostra-incompetenza
    :parameters (?p - professore ?d - dipartimento)
    :precondition (and (rettore-informato) (influenza ?p ?d) (incompetente ?p))
    :effect (and (not (influenza ?p ?d)))
  )

  ;; Azione: Ottenere una revisione dei voti
  (:action ottieni-revisione
    :parameters (?p - professore ?d - dipartimento)
    :precondition (and (rettore-informato) (not (influenza ?p ?d)))
    :effect (revisione-ottenuta)
  )

  ;; Azione: Superare la paura
  (:action supera-paura
    :parameters (?s - studente)
    :precondition (paura ?s)
    :effect (not (paura ?s))
  )

  ;; Azione: Segnala lezione senza senso
  (:action segnala-lezione
    :parameters (?s - studente ?u - universita ?l - lezione ?e - esame)
    :precondition (and (at ?s ?u) (lezione-senza-senso ?l))
    :effect (esame-scorretto ?e)
  )
)