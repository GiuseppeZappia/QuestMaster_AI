;; domain.pddl - L'Equazione Fatata
(define (domain equazione-fatata)
  (:requirements :strips :typing :negative-preconditions) ;; Definisce i requisiti del linguaggio, inclusa la tipizzazione e le precondizioni negative

  (:types ;; Definisce i tipi di oggetti nel mondo
    personaggio ;; Un tipo generico per le persone
    fantagenitore ;; Il giocatore/agente
    fisico ;; Lo scienziato da aiutare, Leo
    rivale ;; L'antagonista, Dr. Thorne
    entita_magica ;; Il Gremlin della Logica
    ricerca ;; Il lavoro scientifico di Leo
    premio ;; Il Premio Nobel
  )

  (:predicates ;; Definisce gli stati possibili del mondo
    (bloccato ?f - fisico) ;; Lo stato in cui il fisico e' bloccato creativamente
    (ha_sindrome_impostore ?f - fisico) ;; Lo stato in cui il fisico dubita di se'
    (rivale_attivo ?rv - rivale) ;; Lo stato in cui il rivale sta sabotando la ricerca
    (gremlin_presente ?g - entita_magica) ;; Lo stato in cui il gremlin sta causando problemi
    (dati_corrotti ?r - ricerca) ;; Lo stato in cui i dati della ricerca sono corrotti dal gremlin
    (teoria_formulata ?r - ricerca) ;; Lo stato in cui la teoria e' stata formulata con successo
    (ricerca_pubblicata ?r - ricerca) ;; Lo stato in cui la ricerca e' stata pubblicata
    (premio_vinto ?p - premio) ;; Lo stato finale in cui il premio e' stato vinto
  )

  ;; Azione per fornire ispirazione magica e sbloccare il fisico
  (:action incantesimo-ispirazione
    :parameters (?fg - fantagenitore ?f - fisico) ;; Parametri: il fantagenitore che agisce e il fisico che riceve
    :precondition (and (bloccato ?f)) ;; Precondizione: il fisico deve essere bloccato
    :effect (and (not (bloccato ?f))) ;; Effetto: il fisico non e' piu' bloccato
  )

  ;; Azione per aumentare la fiducia del fisico e rimuovere la sindrome dell'impostore
  (:action potenziamento-concentrazione
    :parameters (?fg - fantagenitore ?f - fisico) ;; Parametri: il fantagenitore e il fisico
    :precondition (and (ha_sindrome_impostore ?f)) ;; Precondizione: il fisico deve avere la sindrome dell'impostore
    :effect (and (not (ha_sindrome_impostore ?f))) ;; Effetto: la sindrome dell'impostore viene rimossa
  )

  ;; Azione per contrastare i tentativi di sabotaggio del rivale
  (:action neutralizza-sabotaggio-rivale
    :parameters (?fg - fantagenitore ?rv - rivale) ;; Parametri: il fantagenitore e il rivale da contrastare
    :precondition (and (rivale_attivo ?rv)) ;; Precondizione: il rivale deve essere attivamente impegnato nel sabotaggio
    :effect (and (not (rivale_attivo ?rv))) ;; Effetto: i tentativi del rivale sono sventati
  )

  ;; Azione per scacciare il Gremlin della Logica e riparare i dati
  (:action scaccia-gremlin-logica
    :parameters (?fg - fantagenitore ?g - entita_magica ?r - ricerca) ;; Parametri: fantagenitore, gremlin e la ricerca interessata
    :precondition (and (gremlin_presente ?g) (dati_corrotti ?r)) ;; Precondizione: il gremlin deve essere presente e i dati corrotti
    :effect (and (not (gremlin_presente ?g)) (not (dati_corrotti ?r))) ;; Effetto: il gremlin viene scacciato e i dati vengono ripristinati
  )

  ;; Azione per permettere al fisico di formulare la sua teoria rivoluzionaria
  (:action formulazione-teoria
    :parameters (?f - fisico ?r - ricerca ?rv - rivale ?g - entita_magica) ;; Parametri: il fisico, la sua ricerca, il rivale e il gremlin
    :precondition (and ;; Precondizioni: tutti gli ostacoli devono essere stati rimossi
        (not (bloccato ?f)) ;; Il fisico non deve essere bloccato
        (not (ha_sindrome_impostore ?f)) ;; Il fisico deve avere fiducia in se'
        (not (rivale_attivo ?rv)) ;; Il rivale non deve sabotare
        (not (gremlin_presente ?g)) ;; Il gremlin non deve interferire
        (not (dati_corrotti ?r)) ;; I dati devono essere puliti
      )
    :effect (and (teoria_formulata ?r)) ;; Effetto: la teoria viene formulata con successo
  )

  ;; Azione per pubblicare la ricerca una volta che la teoria e' completa
  (:action pubblicazione-ricerca
    :parameters (?f - fisico ?r - ricerca) ;; Parametri: il fisico e la ricerca da pubblicare
    :precondition (and (teoria_formulata ?r)) ;; Precondizione: la teoria deve essere stata formulata
    :effect (and (ricerca_pubblicata ?r)) ;; Effetto: la ricerca viene pubblicata
  )

  ;; Azione finale per vincere il Premio Nobel come risultato della pubblicazione
  (:action vittoria-premio-nobel
    :parameters (?f - fisico ?r - ricerca ?p - premio) ;; Parametri: il fisico, la ricerca e il premio
    :precondition (and (ricerca_pubblicata ?r)) ;; Precondizione: la ricerca deve essere stata pubblicata
    :effect (and (premio_vinto ?p)) ;; Effetto: il premio viene vinto, raggiungendo l'obiettivo finale
  )
)