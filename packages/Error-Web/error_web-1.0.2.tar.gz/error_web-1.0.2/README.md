# 🌐 Error_Web

**Error_Web** est un gestionnaire d’erreurs universel, pédagogique et élégant pour les applications **Flask**.  
Il remplace les pages d’erreurs génériques par des interfaces modernes et explicatives, basées sur les standards **RFC**, **MDN Web Docs** et **Wikipédia**.

Objectif : arrêter les pages d’erreur cryptiques et expliquer clairement *ce qui s’est passé* et *quoi faire*.

---

## ✨ Fonctionnalités

- 📚 Couverture complète des codes HTTP **100 à 599**
- 🧠 Descriptions pédagogiques pour chaque erreur
- 🧭 Conseils pratiques pour utilisateurs et développeurs
- 🐍 Interception des exceptions Python courantes  
  (`ZeroDivisionError`, `KeyError`, `TypeError`)
- 🆔 Trace ID unique pour chaque crash
- 🔀 Réponses HTML ou JSON selon le type de requête
- 🎨 Thèmes visuels automatiques  
  - 4xx → orange  
  - 5xx → rouge  

---

## 🚀 Installation

```bash
pip install error_web


---

🛠 Utilisation

from flask import Flask
import error_web

app = Flask(__name__)
error_web.init_app(app)

@app.route('/test-erreur')
def test():
    return 1 / 0  # Déclenche une erreur pédagogique

if __name__ == "__main__":
    app.run(debug=False)


---

📂 Structure du projet

error_web/
├── codes_http.py
├── core.py
├── __init__.py
└── templates/
    └── errors/
        ├── base.html
        └── default.html


---

📊 Codes HTTP supportés

🔵 1xx — Information

100, 101, 102, 103

🟢 2xx — Succès

200, 201, 202, 203, 204, 205, 206, 207, 208, 226

🟠 3xx — Redirection

300, 301, 302, 303, 304, 305, 306, 307, 308

🟠 4xx — Erreurs Client

400 à 418, 421 à 426, 428, 429, 431, 451

🔴 5xx — Erreurs Serveur

500 à 511

Chaque code dispose :

d’un titre clair

d’une description pédagogique

d’un conseil pratique



---

📝 Licence

Ce projet est sous licence MIT.


---

❤️ Auteur

Développé avec ❤️ par GameurDev.

> Une erreur comprise est une erreur à moitié corrigée.
