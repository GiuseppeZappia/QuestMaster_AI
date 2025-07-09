(define (problem salvare-aurelia)
  (:domain chiave-drago)

  (:objects
    ettore - eroe
    aurelia - principessa
    fumo-nero - drago
    chiave-luce - artefatto
    eldoria cuore-montagna caverna-fumo-nero - luogo
  )

  (:init
    (at ettore eldoria)              ;; L'eroe inizia a Eldoria
    (at aurelia cuore-montagna)    ;; La principessa e prigioniera nel cuore della montagna
    (at chiave-luce cuore-montagna) ;; La chiave e nel cuore della montagna
    (at fumo-nero caverna-fumo-nero) ;; Il drago e nella caverna
    (dragon-awake fumo-nero)         ;; Il drago e sveglio
  )

  (:goal (and
    (princess-rescued aurelia)       ;; La principessa deve essere salvata
    (dragon-sealed fumo-nero)        ;; Il drago deve essere sigillato
  ))
)