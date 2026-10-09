# M3U → JSON per Zappr

Converte una playlist M3U in una lista JSON compatibile con lo schema di [Zappr](https://zappr.stream).

## Uso

1. Crea un repository su GitHub e carica questi file (mantieni la cartella `.github/workflows/`).
2. *(Facoltativo)* Aggiungi il tuo `schema.json` nella radice: il workflow validerà l'output.
3. Vai su **Actions → Converti M3U in JSON Zappr → Run workflow**, compila i campi e avvia.
4. Il JSON viene salvato in `output/<nome file>` nel repository e come artifact scaricabile.

L'URL da usare in Zappr è quello raw:

```
https://raw.githubusercontent.com/<utente>/<repo>/main/output/channels.json
```

`raw.githubusercontent.com` invia gli header CORS, quindi Zappr può caricarlo.

## Uso da riga di comando

```bash
python convert.py https://esempio.it/lista.m3u -o channels.json \
  --name "La mia lista" --publisher "Io" --publisher-link "https://esempio.it"
```

## Regole di conversione

| M3U | JSON |
|---|---|
| `tvg-chno` | `lcn` (se manca viene assegnato un numero progressivo) |
| nome dopo la virgola | `name`; se finisce con ` HD` viene tolto e si imposta `hd: true` |
| `tvg-logo` | `logo`; se finisce con `.png`/`.webp` si aggiunge `?raw=1` per rispettare il pattern dello schema |
| URL | `url` + `type` (`hls`, `dash`, `youtube`, `twitch`, `audio`, `direct`) |
| URL `http://` | `http: true` |
| `x-tvg-url` | **ignorato**: `epg` è `false` salvo `--epg` (l'EPG deve avere CORS abilitato) |

Ignorati perché senza campo nello schema: `#EXTVLCOPT`, `#EXTSIZE`, `tvg-id`, `group-title`.
I problemi (LCN o logo mancanti, tipo stream assunto) compaiono come warning nel log dell'Action.
