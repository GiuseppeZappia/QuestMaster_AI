;; problem.pddl
(define (problem tesoro-perdido)
  (:domain tesoro-maledetto)

  (:objects
    barbanera - barbanera
    ciurma-serpente - ciurma
    dentedisqualo - dentedisqualo
    tesoro-maledetto - tesoro
    zattera giungla spiaggia tempio - location
  )

  (:init
    (at barbanera zattera)          ;; Barbanera è sulla zattera
    (at ciurma-serpente zattera)    ;; La ciurma è sulla zattera
    (at tesoro-maledetto tempio)    ;; Il tesoro è nel tempio
    (alive barbanera)               ;; Barbanera è vivo
    (tribù-hostile tempio)          ;; La tribù è ostile nel tempio
    (pirati-rivali spiaggia)        ;; Pirati rivali sono sulla spiaggia
    (traps-present giungla)         ;; Ci sono trappole nella giungla
    (at dentedisqualo spiaggia)    ;; Capitan Dentedisqualo è sulla spiaggia
  )

  (:goal (and
    (has-treasure ciurma-serpente)  ;; La ciurma deve avere il tesoro
    (curse-broken)                  ;; La maledizione deve essere spezzata
    (nave-ricostruita)             ;; La nave deve essere ricostruita
  ))
)