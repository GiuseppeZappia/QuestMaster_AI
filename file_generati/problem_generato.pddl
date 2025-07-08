(define (problem piumadoro-salvata)
  (:domain re-corvo)

  (:objects
    eroe1 - eroe
    re-corvo1 - re-corvo
    tomo-oblio - oggetto
    piumadoro bosco-maledetto pietra-runica fiume-anime biblioteca-proibita - luogo
  )

  (:init
    (at eroe1 bosco-maledetto)
    (at re-corvo1 bosco-maledetto)
    (at-obj tomo-oblio biblioteca-proibita)
  )

  (:goal (and
    (sigillato re-corvo1)
  ))
)