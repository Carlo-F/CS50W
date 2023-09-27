## LET'S SCOUT! | CS50W CAPSTONE PROJECT

### Introduzione
**Nel mondo dello scoutismo, gli educatori sprecano un sacco di tempo per creare attivita' educative da proporre agli scout piu' giovani.**

E, poiche' non e' semplice creare da zero sempre nuove attivita', che siano adatte agli obiettivi educativi che si vogliono raggiungere, spesso gli educatori devo chiedere ad altri, o cercare su internet, idee per attivita' gia' fatte da altri e che possano replicare. E devono ripetere questo iter ogni volta, per ogni attivita'; e questo, oltre a far perdere molto tempo, puo' essere frustrante.

Se invece esistesse una piattaforma web unificata che raccoglie le schede dettagliate che descrivono in modo standardizzato le attivita' create dagli educatori scout, si potrebbe facilitare questo processo ripetitivo di ideazione/ricerca/creazione, fornendo agli educatori scout accesso alle informazioni di cui hanno bisogno, quando ne hanno bisogno.

Partendo da questa reale esigenza, ho creato questo progetto, che ho chiamato **LET'S SCOUT!**. **LET'S SCOUT!** è quindi una piattaforma web per la creazione, condivisione e ricerca di schede informative dettagliate per la creazione di attività scout.

Le attività scout sono... (Mirella scrive questo paragrafo).

Ogni scheda di attivita' creata su **LET'S SCOUT!**, sara' standardizzata e conterra' tutte le informazioni necessarie all'educatore per riprodurre questa attività con i suoi scout, compresa la fascia d'eta' degli scout adatta, i requisiti materiali, le caratteristiche e gli obiettivi educativi che questa attvita' si prefigge di raggiungere. 

Il progetto **LET'S SCOUT!** è stato ispirato dalla necessità dell'Associazione di Scoutismo Italiano di avere una raccolta unica, uniforme e persistente nel tempo, delle schede di attivita' che al momento non esiste. Gli educatori al momento non hanno un luogo unico dove ricercare ispirazione per le attività scout e devono quindi improvvisare cercando online o parlando tra di loro ogni volta. La piattaforma **LET'S SCOUT!**, una volta terminato il corso CS50W, verrà realmente implementata, in accordo con l'associazione dello scoutismo italiano, per essere utilizzata da tutte le sezioni italiane.

### Distinctiveness and Complexity

#### Come questo progetto si distingue dagli altri del corso: distinctiveness
Questo progetto si distingue dagli altri sviluppati durante il corso in quanto non è un e-commerce, ne un social network, ne nient'altro di simile gia' fatto. E' piuttosto una piattaforma di tipo knoledge-sharing, in cui gli utenti can create, share, organize, access and store le informazioni di cui hanno bisogno, sia loro che altri utenti come loro. **LET'S SCOUT!** e' pertanto una piattaforma web di creazione, condivisione e ricerca di una specifica tipologia di informazione, per rispondere ad una specifica esigenza informativa di conoscenza degli educatori scout.

#### In cosa questo progetto e' piu complesso degli altri del corso: complexity
Per aumentare la complessita' di questo progetto rispetto agli altri progetti portati a termine durante il corso, ho ripreso alcune funzionalita' gia' presenti negli altri progetti, e ho proceduto quindi ad arricchirle, espanderle e a renderle piu' complesse. Ad esempio, c'e' maggiore complessita' nella funzionalita' di **ricerca delle informazioni**. 

Durante il corso le informazioni potevano essere ricercate sostanzialmente in due modi: **consultando delle pagine-elenco** come "latest", "following", "categories" (riferimento a progetti Commerce e Network) oppure con una **ricerca semplificata** con parametro in query string (riferimento a progetto Wiki).

In questo progetto ho voluto implementare queste due funzionalita' ma le ho anche rese piu' complesse: la ricerca testuale e' piu' complessa perche' ho scelto di implementare una nuova funzionalita' che restituisce i risultati in tempo reale durante la digitazione dell'utente tramite interrogazione di API creata ad hoc (tramite la search bar posta in alto in ogni pagina).

La ricerca per pagine-elenco e' anche questa piu' complessa: ho aggiunto una nuova tipologia di ricerca, **la ricerca per tags**. I tag sono essenzialmente delle caratteristiche predefinite (quindi gia' fissate in origine) che l'utente puo' o meno attribuire alle attivita' in fase di creazione. La ricerca per etichette aggiunge al progetto la pagina **Tags** con elenco di tutti i tag, e la pagina del singolo **Tag** dove sono elencate tutte le attivita' che possiedono quella specifica caratteristica.

Due ulteriori esempi della maggior complessita' riguardano la **complessita' di una scheda attivita'** e la funzionalita' di **attivita' suggerite** (similar activities).

In questo progetto, infatti, il modello dell'entita' *Activity* richiede piu' informazioni rispetto alla creazione di un post nel progetto Network e anche piu' informazioni di una scheda prodotto del progetto Commerce. Questo ha implicato piu' campi da gestire sia nel modello, sia nel database, sia nel form nel frontend dell'applicativo aumentando ulteriormente la complessita' generale. Inoltre, nella pagina della singola attivita', in basso, possono comparire delle **attivita' simili**. Sono attivita' che condividono delle caratteristiche con l'attivita' attualmente visualizzata.


### Funzionalità

Elenca le principali funzionalità del tuo progetto. Descrivile in modo chiaro e conciso, evidenziando ciò che lo rende unico o interessante. Puoi anche includere screenshot o GIF animate per mostrare il progetto in azione.

- ricerca di schede attivita secondo differenti parametri:
    - age range
    - titolo (ricerca testuale in tempo reale)
    - tag specifici (caratteristiche)
    - per popolarita'
    - dal piu' recente al meno recente
- creazione e modifica di schede attivita' proprie
- possibilita' di salvare le schede attivita' in una sezione "favoriti"
- attivita' suggerite (similar activities)

### Tecnologie utilizzate

Elenca le principali tecnologie, framework o librerie che hai utilizzato per sviluppare il progetto. Questo aiuta gli altri sviluppatori a capire meglio il contesto tecnologico del tuo lavoro.

### Installazione e utilizzo

Fornisci istruzioni chiare e concise su come installare e configurare il tuo progetto. Indica le dipendenze necessarie e le istruzioni per installarle, se necessario. Includi anche le istruzioni per avviare il progetto localmente.

Descrivi dettagliatamente come utilizzare il tuo progetto. Fornisci esempi specifici di comandi o azioni che l'utente può eseguire per sfruttare le funzionalità del progetto.

### Struttura del codice

Spiega l'organizzazione del codice nel progetto. Se hai una struttura modulare o un'architettura specifica, puoi illustrarla in questa sezione. **Descrivi le directory principali.**

### Contenuto dei file

elenca **TUTTI i file** presenti nel repository e spiega brevemente la funzione di ciascuno.

### Sviluppi futuri

- registrazione libera oppure utenti creati solo da admin
- poter scaricare in PDF la scheda di un'attivita'
- aggiungere ulteriori tag se necessario

### Contatti

Fornisci informazioni su come contattarti. Puoi includere link al tuo profilo GitHub, indirizzo email o altri canali di comunicazione pertinenti.
