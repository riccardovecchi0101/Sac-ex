{
    /* ======================================================
       SCENARIO_SCHEMA
       ------------------------------------------------------
       Definisce quali parametri identificano uno scenario
       di simulazione.
       Ogni combinazione di questi parametri = 1 scenario.
       ====================================================== */
    "scenario_schema": {

        /* rho = tasso di utilizzo del server (lambda / mu)
           - pattern: nome del parametro nei file OMNeT++
           - type: tipo del parametro (qui numero reale)
        */
        "rho": {
            "pattern": "**.rho",
            "type": "real"
        },

        /* cv = coefficiente di variazione del tempo di servizio
           - anche questo è un parametro di scenario
        */
        "cv": {
            "pattern": "**.cv",
            "type": "real"
        }
    },

    /* ======================================================
       METRICS
       ------------------------------------------------------
       Dichiarazione delle metriche DISPONIBILI.
       Qui NON si calcola nulla: si dice solo
       dove leggere i dati dai risultati OMNeT++.
       ====================================================== */
    "metrics": {

        /* ResponseTime = tempo di risposta medio
           - letto dal modulo sink
           - lifeTime:mean è lo scalare OMNeT++
        */
        "ResponseTime": {
            "module": "**.sink",
            "scalar_name": "lifeTime:mean",
            "aggr": ["none"]
        },

        /* WaitingTime = tempo medio di attesa in coda
           - sempre prodotto dal sink
           - totalQueueingTime:mean è lo scalare OMNeT++
        */
        "WaitingTime": {
            "module": "**.sink",
            "scalar_name": "totalQueueingTime:mean",
            "aggr": ["none"]
        }
    },

    /* ======================================================
       HISTOGRAMS
       ------------------------------------------------------
       Dichiarazione degli istogrammi DISPONIBILI.
       Anche qui: nessuna analisi, solo definizione.
       ====================================================== */
    "histograms": {

        /* Istogramma del tempo di risposta
           - prodotto dal sink
           - deve essere abilitato nell’ini
             con result-recording-modes = +histogram
        */
        "ResponseTimeHistogram": {
            "module": "**.sink",
            "histogram_name": "lifeTime:histogram"
        }
    },

    /* ======================================================
       ANALYSES
       ------------------------------------------------------
       Qui si decide COSA viene davvero analizzato.
       Ogni voce produce un file di output.
       ====================================================== */
    "analyses": {

        /* --------------------------------------------------
           Hist_RT
           --------------------------------------------------
           Analisi basata su ISTOGRAMMI.
           Seleziona scenari specifici e salva l’istogramma.
        */
        "Hist_RT": {

            /* File di output dell’istogramma */
            "outfile": "analisi/histogram.data",

            /* Scenario:
               - seleziona solo le simulazioni con
                 rho = 0.7 o 0.9
                 cv = 0.5, 1.0 o 1.5
            */
            "scenario": {
                "rho": [0.7, 0.9],
                "cv":  [0.5, 1.0, 1.5]
            },

            /* Istogramma da usare
               (definito nella sezione histograms)
            */
            "histogram": "ResponseTimeHistogram"
        },

        /* --------------------------------------------------
           RT_rho_cv
           --------------------------------------------------
           Analisi numerica su griglia (rho, cv).
           Calcola le metriche richieste per
           TUTTI gli scenari simulati.
        */
        "RT_rho_cv": {

            /* File di output dei risultati numerici */
            "outfile": "analisi/22-04-2022.data",

            /* Definizione degli scenari:
               - fixed: parametri fissati (qui nessuno)
               - range: parametri che variano
            */
            "scenarios": {

                /* Nessun parametro fissato */
                "fixed": {},

                /* Varia sia rho che cv
                   → sweep bidimensionale
                */
                "range": ["rho", "cv"]
            },

            /* Metriche effettivamente calcolate.
               SOLO queste appariranno nell’output.
            */
            "metrics": [

                /* Tempo di risposta medio */
                {
                    "metric": "ResponseTime",
                    "aggr": "none"
                },

                /* Tempo medio di attesa in coda */
                {
                    "metric": "WaitingTime",
                    "aggr": "none"
                }
            ]
        }
    }
}
