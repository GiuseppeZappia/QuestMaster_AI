;; domain.pddl
;; Nome del dominio: Il Silenzio del Loto Nero
;; Descrizione: File di dominio per la quest di Kael, il ninja del Loto Silente.
;;              Definisce i tipi, i predicati e le azioni possibili nel mondo di gioco.

(define (domain silenzio-loto-nero)
  (:requirements :strips :typing)

  (:types
    ;; Definizione dei tipi di oggetti nel mondo
    ninja shogun generale leader - character ;; Supertipo per tutti i personaggi
    luogo                                ;; Luoghi esplorabili
    ingrediente                          ;; Ingredienti per l'antidoto
  )

  (:predicates
    ;; Predicati per descrivere lo stato del mondo

    ;; Posizioni e connessioni
    (at ?c - character ?l - luogo)             ;; Un personaggio ?c si trova nel luogo ?l
    (at-ingrediente ?i - ingrediente ?l - luogo) ;; Un ingrediente ?i si trova nel luogo ?l
    (connesso ?from - luogo ?to - luogo)       ;; Esiste un percorso diretto dal luogo ?from a ?to

    ;; Stato della quest e degli ostacoli
    (shogun-avvelenato ?s - shogun)            ;; Lo shogun ?s è avvelenato
    (pattugliato ?l - luogo)                   ;; Il luogo ?l è pattugliato dai nemici
    (trappola-attiva ?l - luogo)               ;; Il luogo ?l ha una trappola attiva

    ;; Inventario e progressi del giocatore
    (ha-ingrediente ?n - ninja ?i - ingrediente) ;; Il ninja ?n possiede l'ingrediente ?i
    (ha-antidoto ?n - ninja)                   ;; Il ninja ?n ha creato l'antidoto

    ;; Predicati di obiettivo
    (shogun-salvato ?s - shogun)               ;; Lo shogun ?s è stato salvato
    (takeda-traditore-svelato)                 ;; Il tradimento di Takeda è stato svelato
    (leader-tigre-sconfitto)                   ;; Il leader del clan nemico è stato sconfitto
  )

  ;; --- AZIONI POSSIBILI ---

  (:action muovi
    :parameters (?n - ninja ?from - luogo ?to - luogo)
    :precondition (and
      (at ?n ?from)
      (connesso ?from ?to)
    )
    :effect (and
      (not (at ?n ?from))
      (at ?n ?to)
    )
  )

  (:action disarma-trappola
    :parameters (?n - ninja ?l - luogo)
    :precondition (and
      (at ?n ?l)
      (trappola-attiva ?l)
    )
    :effect (and
      (not (trappola-attiva ?l))
    )
  )

  (:action raccogli-ingrediente
    :parameters (?n - ninja ?i - ingrediente ?l - luogo)
    :precondition (and
      (at ?n ?l)
      (at-ingrediente ?i ?l)
      (not (trappola-attiva ?l)) ;; Non si può raccogliere se ci sono trappole attive
    )
    :effect (and
      (not (at-ingrediente ?i ?l))
      (ha-ingrediente ?n ?i)
    )
  )

  (:action crea-antidoto
    :parameters (?n - ninja ?i1 - ingrediente ?i2 - ingrediente)
    :precondition (and
      (ha-ingrediente ?n ?i1)
      (ha-ingrediente ?n ?i2)
    )
    :effect (and
      (not (ha-ingrediente ?n ?i1))
      (not (ha-ingrediente ?n ?i2))
      (ha-antidoto ?n)
    )
  )

  (:action cura-shogun
    :parameters (?n - ninja ?s - shogun ?l - luogo)
    :precondition (and
      (at ?n ?l)
      (at ?s ?l)
      (ha-antidoto ?n)
      (shogun-avvelenato ?s)
    )
    :effect (and
      (not (shogun-avvelenato ?s))
      (shogun-salvato ?s)
    )
  )

  (:action smaschera-takeda
    :parameters (?n - ninja ?s - shogun ?g - generale ?l - luogo)
    :precondition (and
      (at ?n ?l)
      (at ?s ?l)
      (at ?g ?l)
      (shogun-salvato ?s) ;; Si può smascherare il traditore solo dopo aver salvato lo Shogun
    )
    :effect (and
      (takeda-traditore-svelato)
    )
  )

  (:action sconfiggi-leader-tigre
    :parameters (?n - ninja ?le - leader ?l - luogo)
    :precondition (and
      (at ?n ?l)
      (at ?le ?l)
      (takeda-traditore-svelato) ;; Si può affrontare il leader solo dopo aver creato scompiglio smascherando il traditore
    )
    :effect (and
      (leader-tigre-sconfitto)
    )
  )
)