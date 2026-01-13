HTTP_STATUS_DETAILS = {
    # 4xx - Erreurs Client
    400: {"title": "Requête Incorrecte", "message": "La syntaxe de la requête est erronée.", "advice": "Vérifiez le format de vos données."},
    401: {"title": "Authentification Requise", "message": "Vous devez être connecté pour accéder à la ressource.", "advice": "Veuillez vous authentifier."},
    403: {"title": "Accès Refusé", "message": "Le serveur refuse d'exécuter la requête.", "advice": "Vos droits sont insuffisants."},
    404: {"title": "Page Introuvable", "message": "La ressource demandée n'existe pas.", "advice": "Vérifiez l'URL ou revenez à l'accueil."},
    405: {"title": "Méthode Non Autorisée", "message": "La méthode HTTP utilisée n'est pas permise.", "advice": "Vérifiez si vous devez utiliser GET ou POST."},
    429: {"title": "Trop de Requêtes", "message": "Vous avez dépassé votre quota de requêtes.", "advice": "Veuillez ralentir et attendre un moment."},

    # 5xx - Erreurs Serveur
    500: {"title": "Erreur Interne du Serveur", "message": "Une erreur imprévue est survenue de notre côté.", "advice": "Le développeur a été notifié automatiquement."},
    502: {"title": "Mauvaise Passerelle", "message": "Réponse invalide reçue d'un serveur distant.", "advice": "Le problème vient d'une liaison entre services."},
    503: {"title": "Service Indisponible", "message": "Le serveur est en maintenance ou surchargé.", "advice": "Réessayez dans quelques minutes."},
    504: {"title": "Délai Passerelle Dépassé", "message": "Le serveur distant a mis trop de temps à répondre.", "advice": "La base de données est peut-être saturée."}
}

def get_http_info(code):
    try:
        code = int(code)
    except:
        code = 500
    if code < 400 or code >= 600:
        code = 500
    return HTTP_STATUS_DETAILS.get(code, {
        "title": f"Erreur {code}",
        "message": "Une erreur spécifique est survenue.",
        "advice": "Consultez les logs avec le Trace ID."
    })
