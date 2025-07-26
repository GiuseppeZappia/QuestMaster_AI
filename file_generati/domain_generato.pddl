;; domain.pddl
(define (domain lamento-drago-ghiaccio)
  (:requirements :strips :typing)

  (:types
    agente luogo artefatto
    eroe drago - agente
  )

  (:predicates
    ;; Predicati di posizione
    (at ?a - agente ?l - luogo)
    (at-artefatto ?art - artefatto ?l - luogo)

    ;; Predicati di stato dell'eroe
    (ha-fiamma ?h - eroe)

    ;; Predicati di stato del drago
    (corrotto ?d - drago)
    (purificato ?d - drago)

    ;; Predicati di stato del mondo e ostacoli
    (connesso ?from - luogo ?to - luogo)
    (sentiero-bloccato ?from - luogo ?to - luogo)
    (guardato-da-guardiani ?l - luogo)
  )

  ;; Azione per muoversi tra due luoghi sicuri
  (:action muovi
    :parameters (?h - eroe ?from - luogo ?to - luogo)
    :precondition (and
      (at ?h ?from)
      (connesso ?from ?to)
      (not (sentiero-bloccato ?from ?to))
      (not (guardato-da-guardiani ?to)) ; Non ci si può muovere verso un luogo guardato
    )
    :effect (and
      (not (at ?h ?from))
      (at ?h ?to)
    )
  )

  ;; Azione per attraversare un luogo sorvegliato, sconfiggendo i guardiani
  (:action supera-guardiani
    :parameters (?h - eroe ?from - luogo ?to - luogo)
    :precondition (and
      (at ?h ?from)
      (connesso ?from ?to)
      (not (sentiero-bloccato ?from ?to))
      (guardato-da-guardiani ?to) ; Il luogo di destinazione deve essere guardato
    )
    :effect (and
      (not (at ?h ?from))
      (at ?h ?to)
      (not (guardato-da-guardiani ?to)) ; I guardiani vengono sconfitti all'arrivo
    )
  )

  ;; Azione per raccogliere la Fiamma Eterna
  (:action raccogli-fiamma-eterna
    :parameters (?h - eroe ?f - artefatto ?l - luogo)
    :precondition (and
      (at ?h ?l)
      (at-artefatto ?f ?l)
    )
    :effect (and
      (ha-fiamma ?h)
      (not (at-artefatto ?f ?l))
    )
  )

  ;; Azione finale per purificare il drago usando la Fiamma Eterna
  (:action purifica-drago
    :parameters (?h - eroe ?d - drago ?l - luogo)
    :precondition (and
      (at ?h ?l)
      (at ?d ?l)
      (ha-fiamma ?h)
      (corrotto ?d)
    )
    :effect (and
      (not (corrotto ?d))
      (purificato ?d)
    )
  )
)