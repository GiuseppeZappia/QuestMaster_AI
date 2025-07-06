;; domain.pddl: Dominio per "L'Ombra Contro le Bestie"

(define (domain ombra-contro-bestie)
  (:requirements :strips :typing :negative-preconditions)

  (:types
    entity location yokai item  ;; Tipi di oggetti nel dominio
    ninja - entity              ;; Kenzo, il ninja
    kappa tengu oni - yokai     ;; Tipi di Yokai
    capo_yokai - yokai          ;; Il boss finale
    sigillo - item              ;; Il sigillo da purificare
  )

  (:predicates
    (at ?e - entity ?l - location)  ;; Entità (ninja, yokai) si trova in una location
    (protected ?l - location)       ;; Location protetta da trappole magiche
    (active ?y - yokai)             ;; Yokai è attivo (presente)
    (purified ?s - sigillo)         ;; Il sigillo è stato purificato
    (defeated ?y - yokai)           ;; Yokai è stato sconfitto
    (has_item ?n - ninja ?i - item)  ;; Il ninja possiede un oggetto
    (in_woods ?n - ninja)           ;; Il ninja è nel bosco infestato
    (woods_clear)                   ;; Il bosco è stato reso sicuro
  )

  ;; Azione: Muoversi tra le location
  (:action move
    :parameters (?n - ninja ?from - location ?to - location)
    :precondition (and (at ?n ?from) (not (in_woods ?n)))
    :effect (and (not (at ?n ?from)) (at ?n ?to))
  )

  ;; Azione: Muoversi nel bosco (rischio di perdersi)
  (:action enter_woods
    :parameters (?n - ninja ?l - location)
    :precondition (and (at ?n ?l) (not (woods_clear)))
    :effect (and (in_woods ?n))
  )

  ;; Azione: Uscire dal bosco
  (:action exit_woods
    :parameters (?n - ninja ?l - location)
    :precondition (and (in_woods ?n) (at ?n ?l))
    :effect (and (not (in_woods ?n)))
  )

  ;; Azione: Disattivare le trappole magiche
  (:action disarm_traps
    :parameters (?n - ninja ?l - location)
    :precondition (and (at ?n ?l) (protected ?l))
    :effect (not (protected ?l))
  )

  ;; Azione: Combattere un Kappa
  (:action fight_kappa
    :parameters (?n - ninja ?k - kappa ?l - location)
    :precondition (and (at ?n ?l) (at ?k ?l) (active ?k))
    :effect (and (not (active ?k)) (defeated ?k))
  )

  ;; Azione: Combattere un Tengu
  (:action fight_tengu
    :parameters (?n - ninja ?t - tengu ?l - location)
    :precondition (and (at ?n ?l) (at ?t ?l) (active ?t))
    :effect (and (not (active ?t)) (defeated ?t))
  )

  ;; Azione: Combattere un Oni
  (:action fight_oni
    :parameters (?n - ninja ?o - oni ?l - location)
    :precondition (and (at ?n ?l) (at ?o ?l) (active ?o))
    :effect (and (not (active ?o)) (defeated ?o))
  )

  ;; Azione: Combattere il Capo Yokai
  (:action fight_capo_yokai
    :parameters (?n - ninja ?cy - capo_yokai ?l - location)
    :precondition (and (at ?n ?l) (at ?cy ?l) (active ?cy))
    :effect (and (not (active ?cy)) (defeated ?cy))
  )

  ;; Azione: Purificare il sigillo
  (:action purify_sigillo
    :parameters (?n - ninja ?s - sigillo ?l - location)
    :precondition (and (at ?n ?l) (at ?s ?l) (not (purified ?s)))
    :effect (purified ?s)
  )
)