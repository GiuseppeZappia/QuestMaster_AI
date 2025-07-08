;; problem.pddl: L'Incubo Accademico

(define (problem incubo-accademico-risolto)
  (:domain incubo-accademico)

  (:objects
    studente1 - studente
    scribacchini - professore
    eldritch - rettore
    astrakhan - universita
    dipartimento-storia - dipartimento
    esame1 - esame
    lezione1 - lezione
  )

  (:init
    (at studente1 astrakhan)  ; Lo studente si trova all'università
    (at scribacchini dipartimento-storia) ; Il professore si trova nel dipartimento
    (at eldritch astrakhan) ; Il rettore si trova all'università
    (incompetente scribacchini) ; Il professore è incompetente
    (influenza scribacchini dipartimento-storia) ; Il professore ha influenza nel dipartimento
    (bocciato studente1) ; Lo studente è stato bocciato
    (paura studente1) ; Lo studente ha paura
    (esame-scorretto esame1) ; L'esame è stato corretto male
    (lezione-senza-senso lezione1) ; La lezione non ha senso
  )

  (:goal (and
    (revisione-ottenuta) ; La revisione dei voti è stata ottenuta
  ))
)