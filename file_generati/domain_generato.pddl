;; domain: risveglio-della-rosa
;; Questo file definisce il dominio di pianificazione per la lore "Il Risveglio della Rosa".
(define (domain risveglio-della-rosa)
  (:requirements :strips :typing) ; Abilita STRIPS e la tipizzazione

  ;; Tipi: definisce le categorie di oggetti nel mondo
  (:types
    personaggio ; Tipo generico per le persone
    principe principessa - personaggio ; Sottotipi specifici di personaggio
    luogo ; Tipo per le location
    oggetto ; Tipo generico per gli item
    spada - oggetto ; Un tipo specifico di oggetto
  )

  ;; Predicati: descrivono lo stato del mondo
  (:predicates
    (at ?p - principe ?l - luogo) ; Indica la posizione attuale del principe
    (is-in ?p - principessa ?l - luogo) ; Indica la posizione fissa della principessa
    (asleep ?p - principessa) ; Indica se la principessa e' addormentata a causa della maledizione
    (has-weapon ?p - principe ?s - spada) ; Indica se il principe possiede la spada
    (sword-is-enchanted ?s - spada) ; Indica se la spada e' stata incantata
    (thorns-are-blocking ?from - luogo ?to - luogo) ; Indica se i rovi bloccano un passaggio
    (fountain-is-at ?l - luogo) ; Indica la presenza della Fontana della Luna in un luogo
  )

  ;; Azione: Incanta la spada e si fa strada tra i rovi per entrare nel castello
  ;; Questa azione combina l'incantamento della spada e il superamento dei rovi per rispettare i vincoli di profondita'
  (:action prepare-sword-and-breach-thorns
    :parameters (?p - principe ?s - spada ?from - luogo ?to - luogo) ; Parametri: il principe, la sua spada, la partenza e l'arrivo
    :precondition (and ; Tutte queste condizioni devono essere vere per eseguire l'azione
      (at ?p ?from) ; Il principe deve essere nel luogo di partenza (le porte)
      (fountain-is-at ?from) ; La fontana magica deve essere in quel luogo
      (has-weapon ?p ?s) ; Il principe deve avere con se' la spada
      (not (sword-is-enchanted ?s)) ; La spada non deve essere gia' incantata
      (thorns-are-blocking ?from ?to) ; I rovi devono bloccare il passaggio verso la destinazione
    )
    :effect (and ; Effetti dell'azione, ovvero come cambia il mondo
      (not (at ?p ?from)) ; Il principe non e' piu' nel luogo di partenza
      (at ?p ?to) ; Il principe ora si trova nella destinazione (dentro il castello)
      (sword-is-enchanted ?s) ; La spada ora e' incantata
      (not (thorns-are-blocking ?from ?to)) ; I rovi non bloccano piu' il passaggio
    )
  )

  ;; Azione: Risvegliare la principessa con il bacio del vero amore
  ;; Questa e' l'azione finale per raggiungere l'obiettivo
  (:action wake-up-princess
    :parameters (?p - principe ?k - principessa ?l - luogo) ; Parametri: il principe, la principessa e il luogo dove si trovano
    :precondition (and ; Tutte queste condizioni devono essere vere
      (at ?p ?l) ; Il principe deve essere nella stessa stanza della principessa
      (is-in ?k ?l) ; La principessa deve trovarsi in quella stanza
      (asleep ?k) ; La principessa deve essere sotto l'incantesimo del sonno
    )
    :effect (and ; Effetti dell'azione
      (not (asleep ?k)) ; La principessa non e' piu' addormentata, la maledizione e' spezzata
    )
  )
)