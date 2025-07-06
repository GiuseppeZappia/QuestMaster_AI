;; problem.pddl: Problema per "L'Ombra Contro le Bestie"

(define (problem ombra-contro-bestie-kage)
  (:domain ombra-contro-bestie)

  (:objects
    kenzo - ninja
    kappa1 kappa2 - kappa
    tengu1 tengu2 - tengu
    oni1 oni2 - oni
    capo_yokai1 - capo_yokai
    sigillo_luna - sigillo
    villaggio kage_sentiero foresta tempio_luna - location
  )

  (:init
    (at kenzo villaggio)              ;; Kenzo inizia nel villaggio
    (at kappa1 kage_sentiero)         ;; Kappa pattugliano il sentiero
    (at kappa2 foresta)              ;; Altri Kappa nella foresta
    (at tengu1 foresta)              ;; Tengu nella foresta
    (at tengu2 kage_sentiero)         ;; Altri Tengu nel sentiero
    (at oni1 foresta)                ;; Oni nella foresta
    (at oni2 kage_sentiero)           ;; Altri Oni nel sentiero
    (at capo_yokai1 tempio_luna)     ;; Il capo Yokai è nel tempio
    (at sigillo_luna tempio_luna)     ;; Il sigillo è nel tempio
    (active kappa1)                   ;; Kappa sono attivi
    (active kappa2)                   ;; Kappa sono attivi
    (active tengu1)                   ;; Tengu sono attivi
    (active tengu2)                   ;; Tengu sono attivi
    (active oni1)                     ;; Oni sono attivi
    (active oni2)                     ;; Oni sono attivi
    (active capo_yokai1)              ;; Il capo Yokai è attivo
    (protected tempio_luna)          ;; Il tempio è protetto da trappole
  )

  (:goal (and
    (purified sigillo_luna)          ;; Il sigillo deve essere purificato
    (defeated capo_yokai1)           ;; Il capo Yokai deve essere sconfitto
  ))
)