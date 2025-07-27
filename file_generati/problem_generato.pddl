;; problem.pddl
;; File di problema per la quest "Il Sorriso Perduto di Pipo".
;; Definisce lo stato iniziale del mondo e l'obiettivo finale della missione.

(define (problem ritrovare-il-sorriso-di-pipo)
  (:domain sorriso-perduto-di-pipo) ;; Specifica il dominio di riferimento per questo problema

  ;; --- OGGETTI ---
  ;; Definizione degli oggetti specifici presenti in questa istanza del mondo.
  (:objects
    pipo1 - pipo ;; Il nostro eroe, il pagliaccio Pipo
    fiore-che-ride - fiore ;; L'oggetto magico da recuperare

    circus-aeturnum - luogo ;; Il punto di partenza e di arrivo della quest
    ponte-caramello - luogo ;; Il luogo dove si trova il Guardiano Brontolone
    labirinto-specchi - luogo ;; Il luogo dove si trova il labirinto e il mimo
    foresta-sussurrante - luogo ;; Il luogo dove si trova il fiore e la melodia
  )

  ;; --- STATO INIZIALE ---
  ;; Descrizione dello stato del mondo all'inizio della quest.
  (:init
    ;; Posizioni iniziali dei personaggi e degli oggetti
    (at pipo1 circus-aeturnum) ;; Pipo parte dal tendone del circo
    (flower-at fiore-che-ride foresta-sussurrante) ;; Il Fiore che Ride si trova nella foresta

    ;; Stato iniziale di Pipo e del circo
    (pipo-has-lost-touch) ;; Pipo ha perso la sua comicita, il problema principale

    ;; Ostacoli attivi nel mondo
    (guardian-blocks-bridge) ;; Il Guardiano Brontolone blocca il passaggio sul ponte
    (labyrinth-is-confusing) ;; Il labirinto degli specchi e un ostacolo attivo
    (mime-is-sabotaging) ;; Il Mimo Silente sta attivamente sabotando la missione
    (melody-is-sad) ;; La Melodia Malinconica e attiva e induce tristezza

    ;; Definizione dei percorsi percorribili tra i luoghi
    (path-is-clear circus-aeturnum ponte-caramello) ;; Si puo viaggiare dal circo al ponte
    (path-is-clear ponte-caramello circus-aeturnum) ;; Si puo tornare dal ponte al circo
    (path-is-clear ponte-caramello labirinto-specchi) ;; Si puo viaggiare dal ponte al labirinto
    (path-is-clear labirinto-specchi ponte-caramello) ;; Si puo tornare dal labirinto al ponte
    (path-is-clear labirinto-specchi foresta-sussurrante) ;; Si puo viaggiare dal labirinto alla foresta
    (path-is-clear foresta-sussurrante labirinto-specchi) ;; Si puo tornare dalla foresta al labirinto
  )

  ;; --- OBIETTIVO ---
  ;; Le condizioni che devono essere vere per considerare il problema risolto.
  (:goal (and
    (circus-is-saved) ;; L'obiettivo finale e salvare il Circus Aeturnum
  ))
)