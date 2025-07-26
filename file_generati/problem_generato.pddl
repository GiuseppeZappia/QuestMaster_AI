;; problem.pddl
;; Questo file definisce l'istanza specifica del problema per la lore "Il Risveglio della Rosa".
(define (problem risveglio-lira)
  (:domain risveglio-della-rosa) ; Specifica il dominio di riferimento per questo problema

  ;; Oggetti: Definisce le entita' specifiche presenti in questa istanza del mondo
  (:objects
    valerius - principe ; Il principe protagonista della storia, Valerius
    lira - principessa ; La principessa caduta nel sonno incantato, Lira
    spada-di-famiglia - spada ; La lama che il principe deve incantare
    cancello-castello - luogo ; Il punto di partenza, fuori dal castello dove si trovano i rovi e la fontana
    stanza-principessa - luogo ; Il luogo dove la principessa e' imprigionata nel sonno
  )

  ;; Stato Iniziale: Descrive la configurazione del mondo all'inizio della quest
  (:init
    (at valerius cancello-castello) ; Il principe Valerius si trova al cancello del castello
    (is-in lira stanza-principessa) ; La principessa Lira si trova nella sua stanza
    (asleep lira) ; La principessa Lira e' addormentata a causa della maledizione
    (has-weapon valerius spada-di-famiglia) ; Il principe Valerius possiede la sua spada di famiglia
    (fountain-is-at cancello-castello) ; La Fontana della Luna si trova al cancello del castello, accessibile al principe
    (thorns-are-blocking cancello-castello stanza-principessa) ; I rovi incantati bloccano il passaggio dal cancello alla stanza
  )

  ;; Obiettivo: Definisce la condizione che il piano deve raggiungere per essere considerato un successo
  (:goal (and ; L'obiettivo e' una congiunzione di condizioni da soddisfare
    (not (asleep lira)) ; La condizione finale e' che la principessa Lira non sia piu' addormentata
  ))
)