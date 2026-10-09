Ecco il README aggiornato e ottimizzato per riflettere la nuova struttura "Smart" con supporto al cron e alle variabili.

***

# 📺 M3U → JSON per Zappr (Smart Converter)

Convertitore automatico di playlist **M3U/M3U8** in formato **JSON** compatibile con [Zappr](https://zappr.stream).  
Supporta l'aggiornamento programmato (Cron), la pulizia intelligente dei dati e la gestione sicura degli URL.

## ⚡ Funzionalità Principali
*   **Conversione Intelligente:** Rileva automaticamente tipi di stream (HLS, DASH, YouTube, Twitch) e converte HTTP in HTTPS.
*   **Aggiornamento Automatico:** Può sincronizzare la lista ogni giorno senza intervento manuale.
*   **Memoria URL:** Ricorda il tuo link M3U preferito grazie alle Variabili di GitHub.
*   **Sicuro:** Nessun dato sensibile esposto; i permessi di scrittura sono limitati agli owner del repo.

---

## 🚀 Guida all'Uso

### 1. Configurazione Iniziale (Una volta sola)
Per abilitare l'aggiornamento automatico o evitare di incollare l'URL ogni volta:

1. Vai su **Settings** > **Secrets and variables** > **Actions**.
2. Nella scheda **Variables**, clicca su **New repository variable**.
3. Compila così:
   *   **Name:** `DEFAULT_M3U_URL`
   *   **Value:** L'URL della tua playlist (es. `https://raw.githubusercontent.com/.../lista.m3u`)

### 2. Avvio del Workflow
Vai su **Actions** > **Converti M3U in JSON (Smart & Auto)** > **Run workflow**.

Hai due modalità:
*   **Manuale:** Inserisci un URL diverso nel campo apposito se vuoi convertire una lista specifica al volo.
*   **Automatico (Cron):** Lascia il campo URL vuoto. Il sistema userà quello salvato nelle variabili. Se hai attivato la schedulazione, si aggiornerà da solo ogni notte alle 03:00 UTC.

### 3. Risultato
Il file JSON viene salvato nella cartella `output/` del tuo repository.  
Il link da usare in Zappr sarà sempre lo stesso:
```text
https://raw.githubusercontent.com/<tuo-utente>/<tuo-repo>/main/output/channels.json
```

---

## 💻 Uso Locale (Python)
Se preferisci eseguirlo sul tuo PC:

```bash
python convert.py https://esempio.it/lista.m3u -o channels.json \
  --name "La mia lista" --publisher "Il Mio Nome"
```

---

## ⚙️ Regole di Conversione

| Campo M3U | Azione nel JSON |
| :--- | :--- |
| `tvg-chno` | Diventa `lcn`. Se manca, assegnazione progressiva automatica. |
| Nome Canale | Pulizia caratteri speciali. Rimozione suffisso " HD" (imposta flag `hd: true`). |
| `tvg-logo` | Aggiunta automatica di `?raw=1` ai loghi `.png`/`.webp` per compatibilità schema. |
| URL Stream | Rilevamento tipo (`hls`, `dash`, `youtube`, ecc.) e conversione forzata HTTPS. |
| URL `http://` | Convertito in HTTPS con flag `http: true` per avvisare Zappr. |

---

## 🔒 Note sulla Sicurezza
*   **Artifact vs Commit:** Questo workflow salva il file direttamente nel repo (Commit). Assicurati di non committare dati sensibili.
*   **Permessi:** Solo il proprietario del repo può eseguire il workflow che scrive sui file. Gli utenti esterni possono solo visualizzare il risultato finale se il repo è pubblico.
*   **CORS:** L'URL raw di GitHub (`raw.githubusercontent.com`) è già configurato per accettare le richieste CORS necessarie a Zappr.
