# Flask Error Manager

Un gestionnaire d’erreurs universel pour Flask, simple à intégrer.

## Installation

```bash
pip install flask_error_manager
```

## Utilisation

```python
from flask import Flask
from flask_error_manager import init_error_manager

app = Flask(__name__)
init_error_manager(app)

@app.route("/boom")
def boom():
    1 / 0

app.run(port=5000)
```

## Fonctionnalités

- Gère **toutes** les erreurs (400–599 + exceptions Python)
- Affiche une **page HTML** stylée si c’est un navigateur
- Renvoie une **réponse JSON** si c’est une API
- Génère un **Trace ID** unique pour chaque erreur
- Permet de surcharger les pages (ex: `templates/errors/404.html`)

Licence MIT.
