;; domain.pddl
(define (domain fuga-dalla-roccia) ; definisce il nome del dominio di pianificazione
  (:requirements :strips :typing :negative-preconditions) ; specifica le estensioni PDDL usate

  (:types ; definisce i tipi di oggetti nel mondo
    prigioniero ; il personaggio controllato dal giocatore
    luogo ; le diverse aree della prigione e dell'isola
    oggetto ; oggetti che possono essere raccolti o usati
  )

  (:predicates ; definisce le proprieta e le relazioni che possono essere vere o false
    (at ?p - prigioniero ?l - luogo) ; indica la posizione attuale del prigioniero
    (porta-chiusa ?from - luogo ?to - luogo) ; indica se una porta tra due luoghi e' chiusa
    (guardia-presente ?l - luogo) ; indica la presenza di una guardia in un luogo
    (allarme-attivo) ; indica se l'allarme generale della prigione e' scattato
    (ha-oggetto ?p - prigioniero ?o - oggetto) ; indica se il prigioniero possiede un oggetto
    (materiali-raccolti ?p - prigioniero) ; indica se il prigioniero ha raccolto i materiali per la zattera
    (zattera-costruita ?p - prigioniero) ; indica se il prigioniero ha costruito la zattera
    (in-fuga) ; predicato per il goal finale, raggiunto sulla terraferma
    (connesso ?from - luogo ?to - luogo) ; definisce i collegamenti tra i luoghi
    (is-officina ?l - luogo) ; identifica il luogo come officina
    (is-riva ?l - luogo) ; identifica il luogo come riva
  )

  ;; Azione per scassinare la serratura della cella con il cucchiaio
  (:action scassina-serratura-cella
    :parameters (?p - prigioniero ?cucchiaio - oggetto ?cella - luogo ?corridoio - luogo) ; definisce i parametri dell'azione
    :precondition (and ; inizio della lista delle precondizioni
      (at ?p ?cella) ; il prigioniero deve essere nella cella
      (ha-oggetto ?p ?cucchiaio) ; il prigioniero deve avere il cucchiaio
      (porta-chiusa ?cella ?corridoio) ; la porta della cella deve essere chiusa
    ) ; fine della lista delle precondizioni
    :effect (and ; inizio della lista degli effetti
      (not (porta-chiusa ?cella ?corridoio)) ; la porta della cella non e' piu' chiusa
    ) ; fine della lista degli effetti
  )

  ;; Azione per muoversi tra due luoghi, eludendo le guardie
  (:action muoviti
    :parameters (?p - prigioniero ?from - luogo ?to - luogo) ; definisce i parametri dell'azione
    :precondition (and ; inizio della lista delle precondizioni
      (at ?p ?from) ; il prigioniero deve essere nel luogo di partenza
      (connesso ?from ?to) ; i due luoghi devono essere connessi
      (not (porta-chiusa ?from ?to)) ; la porta tra i due luoghi non deve essere chiusa
      (not (guardia-presente ?to)) ; non ci devono essere guardie nel luogo di arrivo
      (not (allarme-attivo)) ; l'allarme non deve essere attivo
    ) ; fine della lista delle precondizioni
    :effect (and ; inizio della lista degli effetti
      (not (at ?p ?from)) ; il prigioniero non e' piu' nel luogo di partenza
      (at ?p ?to) ; il prigioniero e' ora nel luogo di arrivo
    ) ; fine della lista degli effetti
  )

  ;; Azione per raccogliere i materiali necessari per la zattera
  (:action raccogli-materiali-zattera
    :parameters (?p - prigioniero ?officina - luogo) ; definisce i parametri dell'azione
    :precondition (and ; inizio della lista delle precondizioni
      (at ?p ?officina) ; il prigioniero deve essere nell'officina
      (is-officina ?officina) ; il luogo deve essere un'officina
      (not (materiali-raccolti ?p)) ; il prigioniero non deve avere gia' i materiali
    ) ; fine della lista delle precondizioni
    :effect (and ; inizio della lista degli effetti
      (materiali-raccolti ?p) ; il prigioniero ora ha i materiali
    ) ; fine della lista degli effetti
  )

  ;; Azione per costruire la zattera sulla riva dell'isola
  (:action costruisci-zattera
    :parameters (?p - prigioniero ?riva - luogo) ; definisce i parametri dell'azione
    :precondition (and ; inizio della lista delle precondizioni
      (at ?p ?riva) ; il prigioniero deve essere sulla riva
      (is-riva ?riva) ; il luogo deve essere una riva
      (materiali-raccolti ?p) ; il prigioniero deve avere i materiali
      (not (zattera-costruita ?p)) ; la zattera non deve essere gia' stata costruita
    ) ; fine della lista delle precondizioni
    :effect (and ; inizio della lista degli effetti
      (zattera-costruita ?p) ; la zattera e' ora costruita
    ) ; fine della lista degli effetti
  )

  ;; Azione per fuggire dall'isola con la zattera costruita
  (:action fuggi-con-zattera
    :parameters (?p - prigioniero ?riva - luogo ?terraferma - luogo) ; definisce i parametri dell'azione
    :precondition (and ; inizio della lista delle precondizioni
      (at ?p ?riva) ; il prigioniero deve essere sulla riva
      (is-riva ?riva) ; il luogo deve essere una riva
      (zattera-costruita ?p) ; la zattera deve essere stata costruita
      (not (allarme-attivo)) ; l'allarme non deve essere scattato
    ) ; fine della lista delle precondizioni
    :effect (and ; inizio della lista degli effetti
      (not (at ?p ?riva)) ; il prigioniero lascia la riva
      (at ?p ?terraferma) ; il prigioniero raggiunge la terraferma
      (in-fuga) ; il predicato di goal e' soddisfatto
    ) ; fine della lista degli effetti
  )
)