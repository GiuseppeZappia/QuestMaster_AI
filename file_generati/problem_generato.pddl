;; problem.pddl
;; Nome del problema: Vendetta del Loto Silente
;; Descrizione: File di problema per la quest "Il Silenzio del Loto Nero".
;;              Rappresenta lo stato iniziale del mondo e l'obiettivo finale
;;              del ninja Kael per salvare il regno di Kageyama.

(define (problem vendetta-loto-silente)
  (:domain silenzio-loto-nero) ;; Riferimento al file di dominio corrispondente

  (:objects
    ;; Definizione dei personaggi specifici di questa storia
    kael - ninja ;; Il protagonista, ultimo del suo clan
    shogun-kageyama - shogun ;; Il sovrano avvelenato del regno
    takeda - generale ;; Il generale traditore
    leader-tigre - leader ;; Il capo del clan rivale, la Tigre di Ferro

    ;; Definizione degli ingredienti necessari per l'antidoto
    erba-luna - ingrediente ;; Primo ingrediente per l'antidoto "Sonno di Giada"
    radice-ombra - ingrediente ;; Secondo ingrediente per l'antidoto

    ;; Definizione dei luoghi chiave della missione
    dojo-segreto - luogo ;; Il punto di partenza di Kael, ai margini della citta
    strade-capitale - luogo ;; Le strade della citta, pattugliate dal nemico
    ingresso-palazzo - luogo ;; L'entrata principale del palazzo dello Shogun
    stanze-interne - luogo ;; Le stanze interne del palazzo, protette da trappole
    sala-trono - luogo ;; Il cuore del palazzo, dove si trova lo Shogun
  )

  (:init
    ;; Stato iniziale del mondo basato sulla lore

    ;; Posizione iniziale dei personaggi
    (at kael dojo-segreto) ;; Kael inizia la sua missione dal suo dojo segreto
    (at shogun-kageyama sala-trono) ;; Lo Shogun giace avvelenato nella sala del trono
    (at takeda sala-trono) ;; Il Generale Takeda si trova con lo Shogun, fingendosi leale
    (at leader-tigre sala-trono) ;; Il leader della Tigre di Ferro ha preso controllo del palazzo

    ;; Posizione iniziale degli ingredienti per l'antidoto
    (at-ingrediente erba-luna ingresso-palazzo) ;; L'Erba Luna si trova vicino all'ingresso del palazzo
    (at-ingrediente radice-ombra stanze-interne) ;; La Radice Ombra e' nascosta nelle stanze interne

    ;; Connessioni tra i luoghi (percorsi possibili)
    (connesso dojo-segreto strade-capitale) ;; Dal dojo si puo raggiungere la citta
    (connesso strade-capitale dojo-segreto) ;; E' possibile tornare al dojo dalla citta
    (connesso strade-capitale ingresso-palazzo) ;; Dalle strade si puo arrivare all'ingresso del palazzo
    (connesso ingresso-palazzo strade-capitale) ;; E' possibile tornare in citta dal palazzo
    (connesso ingresso-palazzo stanze-interne) ;; Dall'ingresso si accede alle stanze interne
    (connesso stanze-interne ingresso-palazzo) ;; Si puo tornare all'ingresso dalle stanze interne
    (connesso stanze-interne sala-trono) ;; Dalle stanze interne si raggiunge la sala del trono
    (connesso sala-trono stanze-interne) ;; E' possibile lasciare la sala del trono verso le stanze

    ;; Stato degli ostacoli e della quest
    (shogun-avvelenato shogun-kageyama) ;; Lo Shogun e' attualmente avvelenato
    (pattugliato strade-capitale) ;; Le strade della capitale sono sorvegliate dal Clan della Tigre
    (trappola-attiva stanze-interne) ;; Le stanze interne del palazzo sono protette da trappole magiche
  )

  (:goal (and
    ;; Condizioni che devono essere vere per completare la missione
    (shogun-salvato shogun-kageyama) ;; Obiettivo primario: lo Shogun deve essere curato e salvato
    (takeda-traditore-svelato) ;; Obiettivo secondario: il tradimento di Takeda deve essere smascherato
    (leader-tigre-sconfitto) ;; Obiettivo finale: il leader del clan nemico deve essere sconfitto per ripristinare l'ordine
  ))
)