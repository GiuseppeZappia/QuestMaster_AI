;; problem.pddl
(define (problem fuga-alcatraz-az1441) ; definisce il nome specifico di questo problema
  (:domain fuga-dalla-roccia) ; specifica a quale dominio questo problema appartiene

  (:objects ; definisce gli oggetti specifici per questa istanza del problema
    az1441 - prigioniero ; il nostro prigioniero, #AZ-1441
    cucchiaio - oggetto ; l'oggetto iniziale che il prigioniero possiede
    cella-b - luogo ; la cella di partenza nel Blocco B
    corridoio-b - luogo ; il corridoio fuori dalla cella
    cortile - luogo ; il cortile della prigione
    officina - luogo ; l'officina per trovare i materiali
    riva - luogo ; la riva dell'isola da cui fuggire
    terraferma - luogo ; la destinazione finale, fuori dall'isola
  )

  (:init ; definisce lo stato iniziale del mondo
    (at az1441 cella-b) ; il prigioniero inizia nella sua cella
    (ha-oggetto az1441 cucchiaio) ; il prigioniero possiede il cucchiaio affilato
    (porta-chiusa cella-b corridoio-b) ; la porta tra la cella e il corridoio e' chiusa a chiave
    
    (is-officina officina) ; definisce che 'officina' e' un'officina
    (is-riva riva) ; definisce che 'riva' e' una riva

    (connesso cella-b corridoio-b)
    (connesso corridoio-b cella-b)
    (connesso corridoio-b cortile)
    (connesso cortile corridoio-b)
    (connesso cortile officina)
    (connesso officina cortile)
    (connesso cortile riva)
    (connesso riva cortile)
  )

  (:goal (and ; definisce la condizione che deve essere vera per risolvere il problema
    (in-fuga) ; l'obiettivo finale e' raggiungere lo stato di 'in-fuga'
  ))
)