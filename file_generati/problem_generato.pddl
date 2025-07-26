;; problem.pddl
;; Nome del problema: riavvio-stazione-astra
;; Descrizione: Leo deve riavviare l'IA HELIOS e il supporto vitale sulla stazione Astra,
;; superando porte sigillate, un drone ostile e una perdita di refrigerante.

(define (problem riavvio-stazione-astra) ; definisce il nome specifico di questa istanza del problema
  (:domain eco-silenzioso-titano) ; fa riferimento al file di dominio 'eco-silenzioso-titano'

  (:objects ; definisce tutti gli oggetti specifici presenti in questo scenario
    leo - personaggio ; il protagonista della storia
    helios - ia ; l'intelligenza artificiale centrale da riavviare
    quartierino-leo corridoio-centrale sala-ingegneria laboratorio nucleo-controllo - luogo ; le aree della stazione spaziale
    accesso-ingegneria accesso-nucleo - livello-accesso ; i due livelli di schede di accesso necessarie
    frammento-a frammento-b - frammento-codice ; i due frammenti del codice di riavvio manuale
  )

  (:init ; definisce lo stato iniziale del mondo
    ;; Posizione iniziale del personaggio
    (at leo quartierino-leo) ; Leo inizia nei suoi alloggi

    ;; Stato dei sistemi principali
    (helios-offline helios) ; l'IA HELIOS e' offline all'inizio
    (nucleo-controllo nucleo-controllo) ; identifica la stanza 'nucleo-controllo' come quella principale

    ;; Connessioni tra le aree della stazione
    (connessi quartierino-leo corridoio-centrale) ; i quartieri sono connessi al corridoio
    (connessi corridoio-centrale quartierino-leo) ; la connessione e' bidirezionale
    (connessi corridoio-centrale sala-ingegneria) ; il corridoio e' connesso alla sala ingegneria
    (connessi sala-ingegneria corridoio-centrale) ; la connessione e' bidirezionale
    (connessi corridoio-centrale laboratorio) ; il corridoio e' connesso al laboratorio
    (connessi laboratorio corridoio-centrale) ; la connessione e' bidirezionale
    (connessi laboratorio nucleo-controllo) ; il laboratorio e' connesso al nucleo di controllo
    (connessi nucleo-controllo laboratorio) ; la connessione e' bidirezionale

    ;; Ostacoli e pericoli nella stazione
    (perdita-refrigerante sala-ingegneria) ; c'e' una perdita di refrigerante nella sala ingegneria
    (drone-minaccia laboratorio) ; un drone ostile pattuglia il laboratorio

    ;; Stato delle porte di sicurezza
    (porta-sigillata corridoio-centrale sala-ingegneria) ; la porta per la sala ingegneria e' bloccata
    (richiede-accesso corridoio-centrale sala-ingegneria accesso-ingegneria) ; richiede la scheda di accesso per l'ingegneria
    (porta-sigillata laboratorio nucleo-controllo) ; la porta per il nucleo di controllo e' bloccata
    (richiede-accesso laboratorio nucleo-controllo accesso-nucleo) ; richiede la scheda di accesso per il nucleo

    ;; Posizione degli oggetti chiave
    (scheda-in accesso-ingegneria quartierino-leo) ; la scheda per l'ingegneria si trova nei quartieri di Leo
    (scheda-in accesso-nucleo sala-ingegneria) ; la scheda per il nucleo si trova nella sala ingegneria
    (frammento-in frammento-a sala-ingegneria) ; il primo frammento di codice e' nella sala ingegneria
    (frammento-in frammento-b laboratorio) ; il secondo frammento di codice e' nel laboratorio
  )

  (:goal (and ; definisce l'obiettivo finale che il piano deve raggiungere
    (supporto-vitale-ripristinato) ; l'obiettivo primario e' ripristinare il supporto vitale della stazione
  ))
)