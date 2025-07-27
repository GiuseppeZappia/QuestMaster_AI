:precondition (and
      (at ?p ?from)
      (connesso ?from ?to)
      (not (iene-pattugliano ?to)) ; <-- PROBLEMA QUI
    )