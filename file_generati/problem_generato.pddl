;; problem.pddl - Istanza della quest "Il Silenzio del Loto Nero"
(define (problem silenzio-loto-nero-quest)
  (:domain silenzio-loto-nero) ; ; Specifica il dominio di riferimento per questo problema

  ;; Definizione degli oggetti specifici per questa istanza della lore
  (:objects
    kaito - eroe ; ; Il protagonista, ultimo della Guardia Shinobi
    shogun-takeda - shogun ; ; Lo Shogun avvelenato
    generale-onimaru - nemico ; ; Il generale nemico nel cortile
    leader-loto-nero - nemico ; ; Il capo del Clan del Loto Nero
    vicoli-capitale - luogo ; ; Il punto di partenza di Kaito
    cortile-interno - luogo ; ; Luogo presidiato dal Generale Onimaru
    biblioteca-proibita - luogo ; ; Luogo dove si trova la formula
    giardino-avvelenato - luogo ; ; Luogo dove si trova un ingrediente raro
    sala-del-trono - luogo ; ; Luogo finale dove si trovano lo Shogun e il leader nemico
    fiore-di-luna - ingrediente ; ; Primo ingrediente per l'antidoto
    radice-ombra - ingrediente ; ; Secondo ingrediente per l'antidoto
    formula-antidoto - formula ; ; La formula per creare l'antidoto
  )

  ;; Definizione dello stato iniziale del mondo basato sulla lore
  (:init
    (at kaito vicoli-capitale) ; ; Kaito inizia la sua missione nascosto nei vicoli della capitale
    (at shogun-takeda sala-del-trono) ; ; Lo Shogun e' prigioniero nella sala del trono
    (at generale-onimaru cortile-interno) ; ; Il Generale Onimaru si trova nel cortile interno
    (at leader-loto-nero sala-del-trono) ; ; Il leader del clan e' nella sala del trono
    (at-item formula-antidoto biblioteca-proibita) ; ; La formula dell'antidoto e' nella biblioteca
    (at-item fiore-di-luna giardino-avvelenato) ; ; Il Fiore di Luna si trova nel giardino avvelenato
    (at-item radice-ombra biblioteca-proibita) ; ; La Radice Ombra si trova anch'essa nella biblioteca
    (shogun-avvelenato shogun-takeda) ; ; Lo Shogun e' stato avvelenato
    (nemico-vivo generale-onimaru) ; ; Il Generale Onimaru e' vivo e rappresenta una minaccia
    (nemico-vivo leader-loto-nero) ; ; Il leader del Loto Nero e' vivo
    (pattugliato cortile-interno) ; ; Il cortile interno e' pattugliato da samurai corrotti
    (trappola-attiva cortile-interno) ; ; Ci sono trappole nel cortile per impedire l'accesso
    (spirito-guardiano-attivo sala-del-trono) ; ; Uno spirito protegge la sala del trono
  )

  ;; Definizione dell'obiettivo finale della quest
  (:goal (and
    (shogun-salvato shogun-takeda) ; ; L'obiettivo primario e' salvare la vita dello Shogun
    (castello-liberato) ; ; L'obiettivo secondario e' liberare il castello sconfiggendo il leader
  ))
)