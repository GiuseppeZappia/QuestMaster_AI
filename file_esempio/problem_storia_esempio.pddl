(define (problem salvataggio-sofia)
  (:domain principessa-orco)

  (:objects
    eroe1 - eroe
    sofia - principessa
    grognak - orco
    motocicletta1 - motocicletta
    golem1 - golem
    glimmering-glades paludi-putride fortezza-ferro - luogo
  )

  (:init
    (at eroe1 glimmering-glades)           ;; L'eroe parte da Glimmering Glades
    (at sofia fortezza-ferro)              ;; La principessa e' prigioniera nella Fortezza di Ferro
    (at grognak fortezza-ferro)           ;; Grognak e' nella Fortezza di Ferro
    (at motocicletta1 paludi-putride)     ;; La motocicletta e' nelle Paludi Putride
    (at golem1 fortezza-ferro)             ;; Il golem e' nella Fortezza di Ferro
    (alive grognak)                       ;; Grognak e' vivo
    (princess-has-medallion sofia)         ;; La principessa ha il medaglione
    (werewolves-present paludi-putride)
    (bridge-up fortezza-ferro)
    (traps-active fortezza-ferro)
    (golem-active fortezza-ferro)
    (not (werewolves-defeated))           ;; I lupi mannari non sono stati sconfitti
    (not (drawbridge-lowered))            ;; Il ponte levatoio non e' abbassato
    (not (traps-disarmed))                ;; Le trappole non sono disarmate
    (not (golem-defeated))                ;; Il golem non e' stato sconfitto
    (not (bridge-approached paludi-putride))
    (not (fortress-approached fortezza-ferro))
    (not (returned eroe1 glimmering-glades))
  )

  (:goal (and
    (rescued sofia)                        ;; La principessa deve essere salvata
    (returned eroe1 glimmering-glades)
  ))
)