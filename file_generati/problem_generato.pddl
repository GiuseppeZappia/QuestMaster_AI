;; problem.pddl - L'Equazione Fatata
(define (problem guida-a-leo)
  (:domain equazione-fatata) ;; Specifica il dominio di riferimento per questo problema

  (:objects
    fantagenitore1 - fantagenitore ;; Tu, l'agente che deve risolvere il problema
    leo - fisico ;; Il figlioccio, un fisico bloccato sulla sua ricerca
    dr-thorne - rivale ;; L'antagonista accademico che sabota Leo
    gremlin-logica - entita_magica ;; L'entita' che corrompe i dati
    teoria-coerenza-quantistica - ricerca ;; La ricerca rivoluzionaria di Leo
    premio-nobel - premio ;; L'obiettivo finale, il prestigioso premio
  )

  (:init
    (bloccato leo) ;; Leo parte in uno stato di blocco creativo
    (ha_sindrome_impostore leo) ;; Leo soffre della sindrome dell'impostore
    (rivale_attivo dr-thorne) ;; Il Dr. Thorne sta attivamente cercando di sabotare la ricerca
    (gremlin_presente gremlin-logica) ;; Il Gremlin della Logica e' presente e causa problemi
    (dati_corrotti teoria-coerenza-quantistica) ;; I dati della ricerca di Leo sono corrotti a causa del gremlin
  )

  (:goal (and
    (premio_vinto premio-nobel) ;; L'obiettivo finale e' far vincere il Premio Nobel a Leo
  ))
)