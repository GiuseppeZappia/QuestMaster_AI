;; problem.pddl per la quest "L'Eco della Savana"
(define (problem salvataggio-principessa-cleope) ; definisce il nome del problema specifico
  (:domain eco-savana) ; fa riferimento al dominio eco-savana precedentemente definito

  (:objects ; definisce gli oggetti specifici di questa istanza del problema
    franciscus - principe ; il protagonista, Principe Franciscus
    cleope - principessa ; la principessa da salvare, Cleope
    kael - sciamano ; l'antagonista, lo sciamano Kael
    coccodrillo-guardiano - guardiano ; il guardiano primordiale dell'oasi
    terre-selvagge pianure-iene canyon-ombre luogo-baobab - luogo ; i luoghi generici della savana
    oasi-perduta - oasi ; il luogo finale, che e' un tipo speciale di luogo
  )

  (:init ; definisce lo stato iniziale del mondo basato sulla lore
    ;; Posizioni iniziali dei personaggi
    (at franciscus terre-selvagge) ; il Principe Franciscus inizia la sua missione nelle terre selvagge
    (at kael oasi-perduta) ; lo sciamano Kael si trova nell'Oasi Perduta
    (principessa-imprigionata cleope oasi-perduta) ; la Principessa Cleope e' tenuta prigioniera nell'oasi

    ;; Stato iniziale dei nemici
    (vivo kael) ; lo sciamano Kael e' vivo all'inizio della quest
    (guardiano-vivo coccodrillo-guardiano) ; il guardiano coccodrillo e' vivo
    (guardiano-protegge-oasi coccodrillo-guardiano oasi-perduta) ; il guardiano sta proteggendo l'accesso all'oasi

    ;; Stato iniziale degli ostacoli ambientali
    (iene-pattugliano pianure-iene) ; gli uomini-iena pattugliano le pianure, bloccando il passaggio
    (canyon-indecifrabile) ; l'enigma del Canyon delle Ombre Mute non e' ancora stato risolto
    (sentiero-nascosto) ; il sentiero che conduce all'Oasi Perduta e' nascosto

    ;; Definizione della mappa del mondo (connessioni tra luoghi)
    (connesso terre-selvagge pianure-iene) ; e' possibile viaggiare dalle terre selvagge alle pianure
    (connesso pianure-iene terre-selvagge) ; il percorso e' bidirezionale
    (connesso pianure-iene canyon-ombre) ; e' possibile viaggiare dalle pianure al canyon
    (connesso canyon-ombre pianure-iene) ; il percorso e' bidirezionale
    (connesso canyon-ombre luogo-baobab) ; e' possibile viaggiare dal canyon al luogo dei baobab
    (connesso luogo-baobab canyon-ombre) ; il percorso e' bidirezionale
    (connesso luogo-baobab oasi-perduta) ; e' possibile viaggiare dal luogo dei baobab all'oasi
    (connesso oasi-perduta luogo-baobab) ; il percorso e' bidirezionale
  )

  (:goal (and ; definisce l'obiettivo finale che il piano deve raggiungere
    (not (vivo kael)) ; l'obiettivo e' sconfiggere lo sciamano Kael
    (not (principessa-imprigionata cleope oasi-perduta)) ; e liberare la Principessa Cleope dalla sua prigionia
  ))
)