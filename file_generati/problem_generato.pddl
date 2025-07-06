;; problem.pddl per la storia "Il Primo Giorno di Scuola di Sofia"
(define (problem primo-giorno-sofia)
  (:domain primo-giorno-scuola-sofia)

  (:objects
    sofia1 - sofia
    marco - bullo
    signora-maestra - insegnante
    scuola-arcobaleno casa-sofia - luogo
    compito-matematica - matematica
  )

  (:init
    (at sofia1 casa-sofia)         ;; Sofia è a casa sua all'inizio
    (at marco scuola-arcobaleno)    ;; Marco è a scuola
    (at signora-maestra scuola-arcobaleno) ;; L'insegnante è a scuola
    (is-afraid sofia1)              ;; Sofia ha paura
    (is-alone sofia1)               ;; Sofia si sente sola
    (misses-mom sofia1)             ;; Sofia sente la mancanza della mamma
  )

  (:goal (and
    (at sofia1 casa-sofia)          ;; Sofia deve tornare a casa
    (is-happy sofia1)               ;; Sofia deve essere felice
    (met-friend sofia1)            ;; Sofia deve fare amicizia
    (task-completed compito-matematica)  ;; Il compito deve essere completato
    (learned-something sofia1)      ;; Sofia deve imparare qualcosa
  ))
)