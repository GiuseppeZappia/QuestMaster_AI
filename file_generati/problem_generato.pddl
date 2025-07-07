;; problem.pddl
(define (problem vendetta-ryu)
  (:domain ombra-tradimento)

  (:objects
    ryu1 - ryu
    masaru1 - masaru
    rotolo-segreto - rotolo
    foresta tempio fiume interno-tempio - luogo
    guardia1 guardia2 - guardia
  )

  (:init
    (at ryu1 foresta)                 ;; Ryu inizia nella foresta
    (at masaru1 interno-tempio)       ;; Masaru si nasconde nel tempio
    (at rotolo-segreto interno-tempio)  ;; Il rotolo è nel tempio
    (vivo ryu1)                       ;; Ryu è vivo
    (vivo masaru1)                    ;; Masaru è vivo
    (guardie-presenti interno-tempio) ;; Ci sono guardie nel tempio
    (trappole-attive tempio)          ;; Ci sono trappole nel tempio
    (at guardia1 interno-tempio)
    (at guardia2 interno-tempio)
    (adiacente foresta tempio)
    (adiacente tempio foresta)
    (adiacente tempio fiume)
    (adiacente fiume tempio)
    (adiacente fiume interno-tempio)
    (adiacente interno-tempio fiume)
    (adiacente tempio interno-tempio)
    (adiacente interno-tempio tempio)
  )

  (:goal (and
    (sconfitto masaru1)             ;; Masaru deve essere sconfitto
    (possiede ryu1 rotolo-segreto)   ;; Ryu deve possedere il rotolo
    (onore-ristabilito)             ;; L'onore del clan deve essere ripristinato
  ))
)