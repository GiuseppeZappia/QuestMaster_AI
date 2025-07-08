<<<<<<< HEAD
(define (problem piumadoro-salvata)
  (:domain re-corvo)

  (:objects
    eroe1 - eroe
    re-corvo1 - re-corvo
    tomo-oblio - oggetto
    piumadoro bosco-maledetto pietra-runica fiume-anime biblioteca-proibita - luogo
=======
;; problem.pddl
(define (problem incubo-accademico-risolto)
  (:domain incubo-accademico)
  (:objects
    studente1 - studente
    scribacchini - professore
    eldritch - rettore
    astrakhan - universita
    dipartimento-storia - dipartimento
    esame1 - esame
    lezione1 - lezione
    ufficio-scribacchini aula-lezioni biblioteca - luogo
>>>>>>> 39ccaaad0cddb0535f353c7ca77c8f34c21c34b6
  )
  (:init
<<<<<<< HEAD
    (at eroe1 bosco-maledetto)
    (at re-corvo1 bosco-maledetto)
    (at-obj tomo-oblio biblioteca-proibita)
=======
    (at studente1 biblioteca) ; Lo studente parte dalla biblioteca
    (at scribacchini ufficio-scribacchini) ; Il professore è nel suo ufficio
    (at eldritch astrakhan) ; Il rettore è nell'università
    (at astrakhan astrakhan) ; L'università è se stessa
    (at dipartimento-storia astrakhan) ; Il dipartimento è nell'università
    (at esame1 aula-lezioni) ; L'esame è nell'aula lezioni
    (at lezione1 aula-lezioni) ; La lezione è nell'aula lezioni
    (esame-scorretto esame1) ; L'esame è stato corretto male
    (lezione-insensata lezione1) ; La lezione è insensata
    (ha-paura studente1) ; Lo studente ha paura
    (conosce-rettore scribacchini eldritch) ; Scribacchini conosce il rettore
>>>>>>> 39ccaaad0cddb0535f353c7ca77c8f34c21c34b6
  )
  (:goal (and
<<<<<<< HEAD
    (sigillato re-corvo1)
=======
    (voti-revisionati) ; I voti devono essere revisionati
>>>>>>> 39ccaaad0cddb0535f353c7ca77c8f34c21c34b6
  ))
)