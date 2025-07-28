;; domain.pddl - Il Silenzio del Loto Nero
(define (domain silenzio-loto-nero)
  (:requirements :strips :typing :negative-preconditions) ; ; Definisce i requisiti del linguaggio PDDL utilizzati

  ;; Tipi di entita' nel mondo di gioco
  (:types
    personaggio luogo oggetto ; ; Tipi base
    eroe shogun nemico - personaggio ; ; Sottotipi di personaggio
    ingrediente formula - oggetto ; ; Sottotipi di oggetto
  )

  ;; Predicati che descrivono lo stato del mondo
  (:predicates
    (at ?p - personaggio ?l - luogo) ; ; Indica la posizione di un personaggio in un luogo
    (at-item ?o - oggetto ?l - luogo) ; ; Indica la posizione di un oggetto in un luogo
    (shogun-avvelenato ?s - shogun) ; ; Lo Shogun e' avvelenato
    (shogun-salvato ?s - shogun) ; ; Lo Shogun e' stato salvato
    (nemico-vivo ?n - nemico) ; ; Un nemico specifico e' vivo
    (pattugliato ?l - luogo) ; ; Un luogo e' pattugliato da nemici generici
    (trappola-attiva ?l - luogo) ; ; C'e' una trappola attiva in un luogo
    (ha-ingrediente ?e - eroe ?i - ingrediente) ; ; L'eroe possiede un ingrediente specifico
    (ha-formula ?e - eroe) ; ; L'eroe possiede la formula per l'antidoto
    (antidoto-creato) ; ; L'antidoto e' stato creato
    (spirito-guardiano-attivo ?l - luogo) ; ; Lo spirito guardiano e' attivo in un luogo
    (castello-liberato) ; ; Il castello e' stato liberato dal leader nemico
  )

  ;; Azione: muoversi furtivamente tra due luoghi
  (:action muoversi-furtivamente
    :parameters (?e - eroe ?from - luogo ?to - luogo) ; ; L'eroe si muove da un luogo a un altro
    :precondition (and
      (at ?e ?from) ; ; L'eroe deve essere nel luogo di partenza
      (not (pattugliato ?to)) ; ; Il luogo di destinazione non deve essere pattugliato
      (not (trappola-attiva ?to)) ; ; Il luogo di destinazione non deve avere trappole attive
    )
    :effect (and
      (not (at ?e ?from)) ; ; L'eroe non e' piu' nel luogo di partenza
      (at ?e ?to) ; ; L'eroe e' ora nel luogo di destinazione
    )
  )

  ;; Azione: eliminare una pattuglia di nemici in un luogo
  (:action eliminare-pattuglia
    :parameters (?e - eroe ?l - luogo) ; ; L'eroe elimina una pattuglia in un luogo
    :precondition (and
      (at ?e ?l) ; ; L'eroe deve essere nel luogo pattugliato
      (pattugliato ?l) ; ; Il luogo deve essere pattugliato
    )
    :effect (and
      (not (pattugliato ?l)) ; ; Il luogo non e' piu' pattugliato
    )
  )

  ;; Azione: disattivare una trappola in un luogo
  (:action disattivare-trappola
    :parameters (?e - eroe ?l - luogo) ; ; L'eroe disattiva una trappola
    :precondition (and
      (at ?e ?l) ; ; L'eroe deve essere nel luogo con la trappola
      (trappola-attiva ?l) ; ; La trappola deve essere attiva
    )
    :effect (and
      (not (trappola-attiva ?l)) ; ; La trappola non e' piu' attiva
    )
  )

  ;; Azione: raccogliere un ingrediente per l'antidoto
  (:action raccogliere-ingrediente
    :parameters (?e - eroe ?i - ingrediente ?l - luogo) ; ; L'eroe raccoglie un ingrediente
    :precondition (and
      (at ?e ?l) ; ; L'eroe deve essere nel luogo dell'ingrediente
      (at-item ?i ?l) ; ; L'ingrediente deve essere in quel luogo
    )
    :effect (and
      (ha-ingrediente ?e ?i) ; ; L'eroe ora possiede l'ingrediente
      (not (at-item ?i ?l)) ; ; L'ingrediente non e' piu' nel luogo
    )
  )

  ;; Azione: trovare la formula per l'antidoto
  (:action trovare-formula
    :parameters (?e - eroe ?f - formula ?l - luogo) ; ; L'eroe trova la formula
    :precondition (and
      (at ?e ?l) ; ; L'eroe deve essere nel luogo della formula
      (at-item ?f ?l) ; ; La formula deve essere in quel luogo
    )
    :effect (and
      (ha-formula ?e) ; ; L'eroe ora possiede la formula
      (not (at-item ?f ?l)) ; ; La formula non e' piu' nel luogo
    )
  )

  ;; Azione: creare l'antidoto (richiede tutti gli ingredienti e la formula)
  (:action creare-antidoto
    :parameters (?e - eroe ?i1 - ingrediente ?i2 - ingrediente) ; ; L'eroe crea l'antidoto
    :precondition (and
      (ha-formula ?e) ; ; L'eroe deve avere la formula
      (ha-ingrediente ?e ?i1) ; ; L'eroe deve avere il primo ingrediente
      (ha-ingrediente ?e ?i2) ; ; L'eroe deve avere il secondo ingrediente
    )
    :effect (and
      (antidoto-creato) ; ; L'antidoto viene creato
    )
  )

  ;; Azione: sconfiggere un nemico importante (es. Generale Onimaru)
  (:action sconfiggere-nemico-importante
    :parameters (?e - eroe ?n - nemico ?l - luogo) ; ; L'eroe combatte un nemico chiave
    :precondition (and
      (at ?e ?l) ; ; L'eroe deve essere nello stesso luogo del nemico
      (at ?n ?l) ; ; Il nemico deve essere nello stesso luogo
      (nemico-vivo ?n) ; ; Il nemico deve essere vivo
    )
    :effect (and
      (not (nemico-vivo ?n)) ; ; Il nemico non e' piu' vivo
    )
  )

  ;; Azione: sconfiggere lo spirito guardiano
  (:action sconfiggere-spirito-guardiano
    :parameters (?e - eroe ?l - luogo) ; ; L'eroe affronta lo spirito
    :precondition (and
      (at ?e ?l) ; ; L'eroe deve essere nella sala del trono
      (spirito-guardiano-attivo ?l) ; ; Lo spirito deve essere attivo
    )
    :effect (and
      (not (spirito-guardiano-attivo ?l)) ; ; Lo spirito non e' piu' attivo
    )
  )

  ;; Azione: curare lo Shogun con l'antidoto
  (:action curare-shogun
    :parameters (?e - eroe ?s - shogun ?l - luogo) ; ; L'eroe somministra l'antidoto
    :precondition (and
      (at ?e ?l) ; ; L'eroe deve essere vicino allo Shogun
      (at ?s ?l) ; ; Lo Shogun deve essere nello stesso luogo
      (antidoto-creato) ; ; L'antidoto deve essere stato creato
      (shogun-avvelenato ?s) ; ; Lo Shogun deve essere avvelenato
    )
    :effect (and
      (shogun-salvato ?s) ; ; Lo Shogun e' salvato
      (not (shogun-avvelenato ?s)) ; ; Lo Shogun non e' piu' avvelenato
    )
  )

  ;; Azione: sconfiggere il leader del Loto Nero e liberare il castello
  (:action liberare-castello
    :parameters (?e - eroe ?leader - nemico ?s - shogun ?l - luogo) ; ; Battaglia finale
    :precondition (and
      (at ?e ?l) ; ; L'eroe e' nella sala del trono
      (at ?leader ?l) ; ; Il leader e' nella sala del trono
      (nemico-vivo ?leader) ; ; Il leader e' vivo
      (not (spirito-guardiano-attivo ?l)) ; ; Lo spirito guardiano e' stato sconfitto
      (shogun-salvato ?s) ; ; Lo Shogun deve essere stato salvato per evitare il rituale
    )
    :effect (and
      (not (nemico-vivo ?leader)) ; ; Il leader e' sconfitto
      (castello-liberato) ; ; Il castello e' liberato
    )
  )
)