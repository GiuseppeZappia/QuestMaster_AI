(define (problem recupero-calice)
  (:domain calice-francesco)

  (:objects
    isabella - guerriera
    francesco-calice - calice
    priore1 - priore
    setta1 - setta
    ingresso tempio stanze-interne cripte committente - luogo
  )

  (:init
    (at isabella ingresso)
    (at francesco-calice tempio)
    (at priore1 tempio)
    (guarded tempio setta1)
    (trapped stanze-interne)
    (priore-corrupted priore1)
    (spirits-present cripte)
    (visited ingresso)
  )

  (:goal (and
    (delivered francesco-calice committente)
    (at isabella committente)
  ))
)