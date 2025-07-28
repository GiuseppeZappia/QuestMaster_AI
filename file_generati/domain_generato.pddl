;; domain.pddl
;; Dominio PDDL per la quest "Il Sorriso Perduto di Pipo"
(define (domain sorriso-perduto-di-pipo)
  (:requirements :strips :typing :negative-preconditions) ;; Requisiti base per Fast Downward

  ;; Definizione dei tipi per gli elementi del mondo
  (:types
    personaggio ;; Tipo generico per i personaggi
    luogo ;; Tipo per le location del mondo
    oggetto_magico ;; Tipo per gli oggetti magici
    pipo - personaggio ;; Pipo e un tipo speciale di personaggio
    fiore - oggetto_magico ;; Il Fiore che Ride e un tipo speciale di oggetto
  )

  ;; Predicati che descrivono lo stato del mondo
  (:predicates
    (at ?p - pipo ?l - luogo) ;; Indica la posizione attuale di Pipo
    (flower-at ?f - fiore ?l - luogo) ;; Indica la posizione del Fiore che Ride
    (pipo-has-lost-touch) ;; Stato iniziale: Pipo ha perso il suo tocco comico
    (circus-is-saved) ;; Stato finale: il circo e salvo
    (guardian-blocks-bridge) ;; Il Guardiano Brontolone blocca il ponte
    (labyrinth-is-confusing) ;; Il labirinto confonde il percorso
    (mime-is-sabotaging) ;; Il Mimo Silente sta attivamente sabotando
    (melody-is-sad) ;; La melodia malinconica e attiva
    (pipo-has-flower ?f - fiore) ;; Pipo ha raccolto il Fiore che Ride
    (pipo-is-focused) ;; Pipo ha superato i suoi dubbi e puo resistere alla tristezza
    (path-is-clear ?from - luogo ?to - luogo) ;; Indica che un percorso tra due luoghi e libero
  )

  ;; --- AZIONI POSSIBILI ---

  ;; Azione per muoversi tra due luoghi collegati e sicuri
  (:action move
    :parameters (?p - pipo ?from - luogo ?to - luogo) ;; Pipo si muove da un luogo all'altro
    :precondition (and
      (at ?p ?from) ;; Pipo deve essere nel luogo di partenza
      (path-is-clear ?from ?to) ;; Il percorso tra i due luoghi deve essere libero
    )
    :effect (and
      (not (at ?p ?from)) ;; Pipo non e piu nel luogo di partenza
      (at ?p ?to) ;; Pipo e ora nel luogo di destinazione
    )
  )

  ;; Azione per superare il Guardiano Brontolone
  (:action make-guardian-laugh
    :parameters (?p - pipo ?l - luogo) ;; Pipo affronta il guardiano in un certo luogo
    :precondition (and
      (at ?p ?l) ;; Pipo deve essere nella stessa location del guardiano
      (guardian-blocks-bridge) ;; Il guardiano deve bloccare il ponte
    )
    :effect (and
      (not (guardian-blocks-bridge)) ;; Il guardiano non blocca piu il ponte
    )
  )

  ;; Azione per superare il Labirinto degli Specchi
  (:action navigate-labyrinth
    :parameters (?p - pipo ?l - luogo) ;; Pipo affronta il labirinto
    :precondition (and
      (at ?p ?l) ;; Pipo deve essere nel labirinto
      (labyrinth-is-confusing) ;; Il labirinto deve essere un ostacolo
    )
    :effect (and
      (not (labyrinth-is-confusing)) ;; Il labirinto non e piu un ostacolo
      (pipo-is-focused) ;; Superare il labirinto rende Pipo piu concentrato
    )
  )

  ;; Azione per resistere alla Melodia Malinconica
  (:action resist-sad-melody
    :parameters (?p - pipo ?l - luogo) ;; Pipo resiste alla melodia in un certo luogo
    :precondition (and
      (at ?p ?l) ;; Pipo deve essere nel luogo affetto dalla melodia
      (melody-is-sad) ;; La melodia deve essere attiva
      (pipo-is-focused) ;; Pipo deve essere concentrato per resistere (dopo il labirinto)
    )
    :effect (and
      (not (melody-is-sad)) ;; La melodia non e piu attiva
    )
  )

  ;; Azione per sventare il sabotaggio del Mimo Silente
  (:action outsmart-mime
    :parameters (?p - pipo ?l - luogo) ;; Pipo sventa il piano del mimo
    :precondition (and
      (at ?p ?l) ;; Pipo deve essere dove il mimo sta agendo
      (mime-is-sabotaging) ;; Il mimo deve essere in modalita sabotaggio
    )
    :effect (and
      (not (mime-is-sabotaging)) ;; Il mimo non sta piu sabotando
    )
  )

  ;; Azione per raccogliere il Fiore che Ride
  (:action get-laughing-flower
    :parameters (?p - pipo ?f - fiore ?l - luogo) ;; Pipo raccoglie il fiore
    :precondition (and
      (at ?p ?l) ;; Pipo deve essere nella stessa location del fiore
      (flower-at ?f ?l) ;; Il fiore deve essere in quella location
      (not (pipo-has-flower ?f)) ;; Pipo non deve gia avere il fiore
    )
    :effect (and
      (pipo-has-flower ?f) ;; Pipo ora possiede il fiore
      (not (flower-at ?f ?l)) ;; Il fiore non e piu in quella location
    )
  )

  ;; Azione finale per usare il fiore e salvare il circo
  (:action restore-circus-joy
    :parameters (?p - pipo ?f - fiore ?l-circus - luogo) ;; Pipo usa il fiore al circo
    :precondition (and
      (at ?p ?l-circus) ;; Pipo deve essere tornato al circo
      (pipo-has-flower ?f) ;; Pipo deve avere il fiore
      (pipo-has-lost-touch) ;; Il problema iniziale deve essere ancora presente
    )
    :effect (and
      (not (pipo-has-lost-touch)) ;; Pipo ritrova il suo tocco comico
      (circus-is-saved) ;; Il circo e salvo, raggiungendo l'obiettivo finale
    )
  )
)