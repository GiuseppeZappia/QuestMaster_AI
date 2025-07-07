;; problem.pddl: Salvataggio della Principessa Lyra

(define (problem salvataggio-lyra-problem)
  (:domain salvataggio-lyra)

  (:objects
    valerian - principe
    lyra - principessa
    malkor - stregone
    golem - golem
    eldoria - regno
    foresta montagne fiume fortezza - luogo
  )

  (:init
    (at valerian eldoria)
    (at malkor fortezza)
    (vivo malkor)
    (at lyra fortezza)
    (prigioniero lyra fortezza)
    (goblin-presente foresta)
    (trappola-attiva montagne)
    (fiume-attraversabile)
    (golem-attivo)
    (at golem fortezza)
  )

  (:goal (and
    (at valerian eldoria)
    (at lyra eldoria)
    (sano lyra)
  ))
)