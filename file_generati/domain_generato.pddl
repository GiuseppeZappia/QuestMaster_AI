;; domain.pddl
(define (domain incubo-accademico)
  (:requirements :strips :typing :negative-preconditions :equality)
  (:types
    entity persona luogo documento - entity
    studente professore rettore - persona
    universita dipartimento - luogo
    esame lezione - documento
  )

  (:predicates
    (at ?x - entity ?l - luogo)            ; x si trova in l
    (incompetente ?p - professore)          ; il professore è incompetente
    (prova-ottenuta ?d - documento)        ; prova è stata ottenuta
    (reclamo-presentato)                  ; il reclamo è stato presentato
    (voti-revisionati)                    ; i voti sono stati revisionati
    (ha-paura ?s - studente)              ; lo studente ha paura
    (influente ?p - professore ?d - dipartimento) ; professore ha influenza nel dipartimento
    (esame-scorretto ?e - esame)           ; l'esame è stato corretto male
    (lezione-insensata ?l - lezione)        ; la lezione è insensata
    (conosce-rettore ?p - professore ?r - rettore) ; il professore conosce il rettore
    (parla-studente ?s - studente ?p - professore) ; lo studente parla con il professore
  )

  ;; Muoversi tra i luoghi
  (:action move
    :parameters (?e - entity ?from - luogo ?to - luogo)
    :precondition (and (at ?e ?from))
    :effect (and (not (at ?e ?from)) (at ?e ?to))
  )

  ;; Ottenere una prova (esame mal corretto)
  (:action ottieni-prova-esame
    :parameters (?s - studente ?e - esame ?l - luogo)
    :precondition (and (at ?s ?l) (at ?e ?l) (esame-scorretto ?e) (not (prova-ottenuta ?e)))
    :effect (and (prova-ottenuta ?e))
  )

  ;; Ottenere una prova (lezione insensata)
  (:action ottieni-prova-lezione
    :parameters (?s - studente ?le - lezione ?l - luogo)
    :precondition (and (at ?s ?l) (at ?le ?l) (lezione-insensata ?le) (not (prova-ottenuta ?le)))
    :effect (and (prova-ottenuta ?le))
  )

  ;; Presentare un reclamo
  (:action presenta-reclamo
    :parameters (?s - studente ?u - universita ?d - dipartimento ?x - documento)
    :precondition (and (at ?s ?u) (at ?d ?u) (prova-ottenuta ?x) (not (reclamo-presentato)))
    :effect (and (reclamo-presentato))
  )

  ;; Parlare con il rettore
  (:action parla-rettore
    :parameters (?s - studente ?r - rettore ?u - universita)
    :precondition (and (at ?s ?u) (at ?r ?u) (reclamo-presentato))
    :effect (and (voti-revisionati))
  )

  ;; Superare la paura
  (:action supera-paura
    :parameters (?s - studente)
    :precondition (ha-paura ?s)
    :effect (and (not (ha-paura ?s)))
  )

  ;; Affrontare il professore
  (:action affronta-professore
    :parameters (?s - studente ?p - professore ?l - luogo ?d - dipartimento)
    :precondition (and (not (ha-paura ?s)) (at ?s ?l) (at ?p ?l) (at ?d ?l))
    :effect (and (incompetente ?p))
  )

  ;; Dimostrare l'incompetenza
  (:action dimostra-incompetenza
    :parameters (?p - professore ?d - dipartimento ?u - universita ?s - studente)
    :precondition (and (reclamo-presentato) (incompetente ?p) (at ?p ?u) (at ?s ?u) (at ?d ?u))
    :effect ()
  )

  ;; Revisione dei voti
  (:action revisiona-voti
    :parameters (?u - universita ?s - studente ?r - rettore)
    :precondition (and (reclamo-presentato) (at ?s ?u) (at ?r ?u))
    :effect (and (voti-revisionati))
  )
)