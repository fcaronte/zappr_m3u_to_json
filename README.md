***

# 📺 M3U → JSON per Zappr

Questo tool converte automaticamente una playlist **M3U/M3U8** in un file **JSON** perfettamente compatibile con lo schema di [Zappr](https://zappr.stream).

Gestisce automaticamente la pulizia dei nomi, la conversione degli URL da HTTP a HTTPS, l'assegnazione dei LCN e il rilevamento del tipo di stream (HLS, DASH, YouTube, Twitch, ecc.).

## 🚀 Come si usa

Ci sono due modi principali per utilizzare questo convertitore, a seconda delle tue esigenze:

### Opzione 1: Uso Personale (Tramite Artifact)
*Ideale se vuoi tenere il tuo repository pulito e non vuoi salvare file permanentemente.*

1. Vai sulla scheda **Actions** del repository.
2. Seleziona il workflow **"Converti M3U in JSON (Scarica Artifact)"**.
3. Clicca su **Run workflow** e inserisci:
   - L'URL della tua playlist M3U.
   - Il nome che vuoi dare alla lista.
4. Al termine dell'esecuzione, scorri in fondo alla pagina nella sezione **Artifacts**.
5. Scarica il file ZIP contenente il tuo `channels.json`.
6. **Importante:** Poiché questo file non viene salvato nel repository, per usarlo su Zappr dovrai caricarlo su un servizio di hosting raw come **[Pastebin](https://pastebin.com/)**, **[GitHub Gist](https://gist.github.com/)** o simili, e usare quel link pubblico in Zappr.

### Opzione 2: Uso Permanente / Fork (Tramite Commit)
*Ideale se vuoi che il file rimanga accessibile direttamente dal tuo repository GitHub.*

1. Vai sulla scheda **Actions** e seleziona **"Converti M3U in JSON (Salva su Repo)"**.
2. Compila i campi richiesti e avvia il workflow.
3. Il file JSON verrà salvato automaticamente nella cartella `output/` del tuo repository.
4. Ora puoi usare direttamente il link "Raw" di GitHub in Zappr:
   ```text
   https://raw.githubusercontent.com/<tuo-utente>/<tuo-repo>/main/output/channels.json
   ```
   *(Nota: `raw.githubusercontent.com` supporta nativamente le richieste CORS richieste da Zappr).*

> **Sicurezza:** Solo il proprietario del repository può eseguire il workflow che salva i file (Commit). Gli utenti esterni possono solo scaricare gli Artifact o usare il workflow sui loro fork personali.

## 💻 Uso da riga di comando

Se preferisci eseguirlo localmente sul tuo PC:

```bash
python convert.py https://esempio.it/lista.m3u -o channels.json \
  --name "La mia lista" --publisher "Il Mio Nome"
```

## ⚙️ Regole di Conversione

Il convertitore applica queste regole per rispettare lo schema di Zappr:

| Campo M3U | Azione nel JSON |
| :--- | :--- |
| `tvg-chno` | Diventa `lcn`. Se manca, viene assegnato un numero progressivo automatico. |
| Nome Canale | Diventa `name`. Se finisce con " HD", viene rimosso e impostato `hd: true`. |
| `tvg-logo` | Diventa `logo`. Se finisce in `.png` o `.webp`, aggiunge `?raw=1` per compatibilità. |
| URL Stream | Rileva automaticamente il `type` (`hls`, `dash`, `youtube`, `twitch`, `audio`, `direct`). |
| URL `http://` | Converte l'URL in `https://` e imposta `http: true` per segnalare a Zappr l'uso del protocollo non sicuro. |

## ❓ Risoluzione Problemi

- **Errore JSON:** Se ricevi errori di sintassi, assicurati che l'URL M3U sia raggiungibile pubblicamente. Lo script include protezioni contro caratteri speciali nei nomi dei canali.
- **Warning nei Log:** Controlla i log dell'Action se vedi warning su "LCN mancante" o "Tipo stream non riconosciuto". Il convertitore farà del suo meglio per indovinare, ma è sempre meglio avere una M3U ben formattata.
