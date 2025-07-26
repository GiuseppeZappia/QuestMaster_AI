;; problem.pddl
(define (problem spezzare-maledizione-glaurung)
  (:domain lamento-drago-ghiaccio)

  (:objects
    eroe1 - eroe
    glaurung - drago
    fiamma-eterna - artefatto
    villaggio crepacci-ghiacciati picco-gelido - luogo
  )

  (:init
    ;; Posizioni iniziali degli agenti e degli artefatti
    (at eroe1 villaggio)
    (at glaurung picco-gelido)
    (at-artefatto fiamma-eterna villaggio)

    ;; Stato iniziale del drago
    (corrotto glaurung)

    ;; Connessioni tra i luoghi (la mappa del mondo)
    (connesso villaggio crepacci-ghiacciati)
    (connesso crepacci-ghiacciati villaggio)
    (connesso crepacci-ghiacciati picco-gelido)
    (connesso picco-gelido crepacci-ghiacciati)

    ;; Ostacoli presenti nel mondo
    (guardato-da-guardiani crepacci-ghiacciati)
  )

  (:goal (and
    (purificato glaurung)
  ))
)