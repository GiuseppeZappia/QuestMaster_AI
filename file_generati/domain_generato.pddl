;; domain.pddl per la storia "Il Primo Giorno di Scuola di Sofia"
(define (domain primo-giorno-scuola-sofia)
  (:requirements :strips :typing :negative-preconditions)
  (:types
    entity luogo persona compito - object
    sofia bullo insegnante - persona
    scuola casa - luogo
    matematica - compito
  )

  (:predicates
    (at ?x - entity ?l - luogo)  ;; Posizione di Sofia, Marco, etc.
    (is-afraid ?s - sofia)        ;; Sofia ha paura
    (is-alone ?s - sofia)         ;; Sofia si sente sola
    (met-friend ?s - sofia)       ;; Sofia ha fatto amicizia
    (bullied ?s - sofia ?b - bullo) ;; Sofia è stata bullizzata
    (task-completed ?t - compito)  ;; Il compito è stato completato
    (misses-mom ?s - sofia)       ;; Sofia sente la mancanza della mamma
    (is-happy ?s - sofia)          ;; Sofia è felice
    (learned-something ?s - sofia) ;; Sofia ha imparato qualcosa
  )

  ;; Azione: Entrare a scuola
  (:action enter-school
    :parameters (?s - sofia ?l - luogo)
    :precondition (and (at ?s ?l) (eq ?l casa))
    :effect (and (not (at ?s ?l)) (at ?s scuola) (is-afraid ?s) (is-alone ?s))
  )

  ;; Azione: Parlare con un altro bambino
  (:action talk-to-child
    :parameters (?s - sofia ?l - luogo)
    :precondition (and (at ?s ?l) (is-afraid ?s) (is-alone ?s))
    :effect (and (not (is-afraid ?s)) (not (is-alone ?s)) (met-friend ?s))
  )

  ;; Azione: Affrontare il bullo
  (:action confront-bully
    :parameters (?s - sofia ?b - bullo ?l - luogo)
    :precondition (and (at ?s ?l) (at ?b ?l) (is-afraid ?s))
    :effect (and (not (bullied ?s ?b)) (not (is-afraid ?s)))
  )

  ;; Azione: Chiedere aiuto all'insegnante per il compito
  (:action ask-teacher-for-help
    :parameters (?s - sofia ?t - compito ?l - luogo ?i - insegnante)
    :precondition (and (at ?s ?l) (at ?i ?l) (eq ?t matematica))
    :effect (and (task-completed ?t) (learned-something ?s))
  )

  ;; Azione: Pensare alla mamma
  (:action think-of-mom
    :parameters (?s - sofia)
    :precondition (and (misses-mom ?s))
    :effect (and (not (misses-mom ?s)))
  )

  ;; Azione: Tornare a casa
  (:action return-home
    :parameters (?s - sofia ?l - luogo)
    :precondition (and (at ?s ?l) (eq ?l scuola) (met-friend ?s) (task-completed ?t) (not (is-afraid ?s)))
    :effect (and (not (at ?s ?l)) (at ?s casa) (is-happy ?s))
  )

    ;; Azione: Imparare qualcosa
  (:action learn
    :parameters (?s - sofia)
    :precondition (and (not (learned-something ?s)))
    :effect (and (learned-something ?s))
  )
)