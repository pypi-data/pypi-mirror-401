HTTP_STATUS_DETAILS = {
    # --- 1xx : RÉPONSES INFORMATIVES ---
    100: {"title": "Continue", "message": "Le serveur a reçu les en-têtes de la requête et attend le corps.", "advice": "Tout est OK, vous pouvez continuer l'envoi."},
    101: {"title": "Switching Protocols", "message": "Le serveur accepte de changer de protocole (ex: passage à WebSocket).", "advice": "Le basculement est en cours."},
    102: {"title": "Processing", "message": "WebDAV : Le serveur traite la requête mais n'a pas encore de réponse.", "advice": "Patientez, le serveur travaille encore."},
    103: {"title": "Early Hints", "message": "Permet au navigateur de précharger des ressources avant la réponse finale.", "advice": "Optimisation en cours par le serveur."},

    # --- 2xx : RÉPONSES DE SUCCÈS ---
    200: {"title": "OK", "message": "La requête a réussi.", "advice": "Tout fonctionne normalement."},
    201: {"title": "Created", "message": "La requête a réussi et une nouvelle ressource a été créée.", "advice": "La création a été confirmée."},
    202: {"title": "Accepted", "message": "La requête a été acceptée pour traitement, mais n'est pas encore terminée.", "advice": "Le traitement est asynchrone, vérifiez plus tard."},
    203: {"title": "Non-Authoritative Information", "message": "Les informations renvoyées proviennent d'une copie tierce.", "advice": "Donnée potentiellement transformée par un proxy."},
    204: {"title": "No Content", "message": "La requête a réussi mais il n'y a pas de contenu à renvoyer.", "advice": "L'action a bien été effectuée sans retour de donnée."},
    205: {"title": "Reset Content", "message": "Indique au client de réinitialiser la vue du document.", "advice": "Videz les champs de votre formulaire."},
    206: {"title": "Partial Content", "message": "Le serveur renvoie une partie de la ressource (Range).", "advice": "Utile pour le streaming ou la reprise de téléchargement."},
    207: {"title": "Multi-Status", "message": "WebDAV : Plusieurs codes de statut sont renvoyés en même temps.", "advice": "Consultez le corps XML pour le détail par ressource."},
    208: {"title": "Already Reported", "message": "WebDAV : Le membre a déjà été énuméré précédemment.", "advice": "Évite les boucles de répétition."},
    226: {"title": "IM Used", "message": "Le serveur a renvoyé une instance après manipulation (Delta encoding).", "advice": "Optimisation du transfert de données réussie."},

    # --- 3xx : MESSAGES DE REDIRECTION ---
    300: {"title": "Multiple Choices", "message": "La requête a plusieurs réponses possibles.", "advice": "L'utilisateur ou le client doit choisir une option."},
    301: {"title": "Moved Permanently", "message": "La ressource a été déplacée définitivement vers une nouvelle URL.", "advice": "Mettez à jour vos liens, le navigateur suit la nouvelle adresse."},
    302: {"title": "Found", "message": "La ressource est temporairement située à une autre URL.", "advice": "Le lien est toujours valide, mais cette fois utilisez l'autre URL."},
    303: {"title": "See Other", "message": "La réponse se trouve à une autre URI et doit être récupérée avec GET.", "advice": "Redirection suite à une soumission de formulaire (POST)."},
    304: {"title": "Not Modified", "message": "La ressource n'a pas changé depuis la dernière visite.", "advice": "Le navigateur utilise sa version en cache."},
    307: {"title": "Temporary Redirect", "message": "Redirection temporaire conservant la méthode HTTP d'origine.", "advice": "Le client doit réitérer la requête à la nouvelle adresse."},
    308: {"title": "Permanent Redirect", "message": "Redirection permanente conservant la méthode HTTP d'origine.", "advice": "Ne changez pas POST en GET lors du suivi."},

    # --- 4xx : ERREURS DU CLIENT ---
    400: {"title": "Bad Request", "message": "La syntaxe de la requête est invalide ou malformée.", "advice": "Vérifiez les données que vous envoyez au serveur."},
    401: {"title": "Unauthorized", "message": "Authentification nécessaire pour accéder à la ressource.", "advice": "Veuillez vous connecter pour continuer."},
    402: {"title": "Payment Required", "message": "Code réservé pour des systèmes de paiement futur.", "advice": "Accès restreint aux abonnés ou clients payants."},
    403: {"title": "Forbidden", "message": "Le serveur refuse de traiter la requête (droits insuffisants).", "advice": "Vous n'avez pas l'autorisation d'accéder à cette page."},
    404: {"title": "Not Found", "message": "Le serveur n'a pas trouvé la ressource demandée.", "advice": "Vérifiez l'URL ou le lien cliqué."},
    405: {"title": "Method Not Allowed", "message": "La méthode HTTP utilisée n'est pas autorisée pour cette cible.", "advice": "Vérifiez si l'API accepte GET, POST, PUT ou DELETE."},
    406: {"title": "Not Acceptable", "message": "Le serveur ne trouve rien satisfaisant les critères 'Accept' envoyés.", "advice": "Vérifiez les formats de fichiers acceptés par votre client."},
    407: {"title": "Proxy Authentication Required", "message": "L'authentification doit être faite via un proxy.", "advice": "Connectez-vous à votre serveur proxy."},
    408: {"title": "Request Timeout", "message": "Le serveur a mis fin à la connexion car la requête a été trop longue.", "advice": "Réessayez avec une connexion internet plus rapide."},
    409: {"title": "Conflict", "message": "Conflit avec l'état actuel de la ressource sur le serveur.", "advice": "Souvent dû à une modification simultanée par un autre utilisateur."},
    410: {"title": "Gone", "message": "La ressource est définitivement supprimée sans adresse de redirection.", "advice": "Supprimez ce lien de vos favoris."},
    411: {"title": "Length Required", "message": "Le serveur exige que l'en-tête 'Content-Length' soit défini.", "advice": "Spécifiez la taille du corps de votre requête."},
    412: {"title": "Precondition Failed", "message": "Les préconditions des en-têtes n'ont pas été remplies.", "advice": "Vérifiez les en-têtes If-Match ou If-None-Match."},
    413: {"title": "Content Too Large", "message": "La requête est trop volumineuse pour le serveur.", "advice": "Réduisez la taille des fichiers envoyés."},
    414: {"title": "URI Too Long", "message": "L'adresse URL demandée est trop longue.", "advice": "Réduisez le nombre de paramètres dans l'URL."},
    415: {"title": "Unsupported Media Type", "message": "Le format de données envoyé n'est pas supporté par le serveur.", "advice": "Utilisez un format standard (ex: JSON)."},
    416: {"title": "Range Not Satisfiable", "message": "La plage demandée dépasse la taille de la ressource.", "advice": "Vérifiez les octets demandés."},
    417: {"title": "Expectation Failed", "message": "Le serveur ne peut pas satisfaire les attentes de l'en-tête 'Expect'.", "advice": "Modifiez les paramètres de votre client."},
    418: {"title": "I'm a teapot", "message": "Le serveur refuse de brasser du café avec une théière (RFC 2324).", "advice": "Ceci est une plaisanterie du protocole, versez du thé !"},
    421: {"title": "Misdirected Request", "message": "La requête a été envoyée à un serveur incapable de répondre.", "advice": "Vérifiez la configuration DNS ou du certificat SSL."},
    422: {"title": "Unprocessable Content", "message": "La requête est correcte mais contient des erreurs sémantiques.", "advice": "Vérifiez la validité de vos données métier."},
    423: {"title": "Locked", "message": "WebDAV : La ressource est verrouillée.", "advice": "Attendez la fin du verrouillage."},
    424: {"title": "Failed Dependency", "message": "WebDAV : Échec car une requête parente a échoué.", "advice": "Vérifiez les étapes précédentes de votre action."},
    425: {"title": "Too Early", "message": "Le serveur refuse de traiter une requête qui pourrait être rejouée.", "advice": "Utilisez un canal sécurisé ou réessayez."},
    426: {"title": "Upgrade Required", "message": "Le serveur impose l'utilisation d'un autre protocole (ex: TLS).", "advice": "Mettez à jour votre protocole de connexion."},
    428: {"title": "Precondition Required", "message": "Le serveur exige une requête conditionnelle.", "advice": "Ajoutez des en-têtes de validation d'état (ETag)."},
    429: {"title": "Too Many Requests", "message": "Quota de requêtes dépassé (limitation de débit).", "advice": "Ralentissez la fréquence de vos appels."},
    431: {"title": "Request Header Fields Too Large", "message": "Les en-têtes de la requête sont trop volumineux.", "advice": "Réduisez la taille des cookies ou des en-têtes."},
    451: {"title": "Unavailable For Legal Reasons", "message": "L'accès à cette ressource est interdit pour des raisons juridiques.", "advice": "Contenu censuré ou restreint par la loi."},

    # --- 5xx : ERREURS DU SERVEUR ---
    500: {"title": "Internal Server Error", "message": "Le serveur a rencontré une erreur interne imprévue.", "advice": "Un bug est survenu. L'administrateur système a été alerté."},
    501: {"title": "Not Implemented", "message": "Le serveur ne gère pas la fonctionnalité demandée.", "advice": "Cette méthode sera peut-être implémentée plus tard."},
    502: {"title": "Bad Gateway", "message": "Le serveur a reçu une réponse invalide du serveur distant (Proxy).", "advice": "Un service tiers ou intermédiaire est en panne."},
    503: {"title": "Service Unavailable", "message": "Le serveur est temporairement en maintenance ou surchargé.", "advice": "Réessayez dans quelques minutes."},
    504: {"title": "Gateway Timeout", "message": "Le serveur distant n'a pas répondu à temps à la passerelle.", "advice": "La base de données ou un service distant est trop lent."},
    505: {"title": "HTTP Version Not Supported", "message": "La version HTTP n'est pas supportée par le serveur.", "advice": "Mettez à jour votre navigateur ou votre client HTTP."},
    506: {"title": "Variant Also Negotiates", "message": "Erreur de configuration : négociation circulaire détectée.", "advice": "Contactez l'administrateur du site."},
    507: {"title": "Insufficient Storage", "message": "Le serveur manque d'espace disque pour stocker la requête.", "advice": "Videz de l'espace sur le serveur ou contactez l'hébergeur."},
    508: {"title": "Loop Detected", "message": "Le serveur a détecté une boucle infinie de redirection.", "advice": "Vérifiez vos redirections WebDAV."},
    510: {"title": "Not Extended", "message": "Des extensions supplémentaires sont requises pour traiter la requête.", "advice": "Mettez à jour vos plugins serveur."},
    511: {"title": "Network Authentication Required", "message": "Authentification réseau requise (ex: Portail Wi-Fi).", "advice": "Connectez-vous au réseau local avant de continuer."}
}

def get_http_info(code):
    try:
        code = int(code)
    except (ValueError, TypeError):
        code = 500

    if code in HTTP_STATUS_DETAILS:
        return HTTP_STATUS_DETAILS[code]
    
    if 400 <= code < 500:
        return {"title": f"Erreur Client {code}", "message": "Une erreur client inconnue est survenue.", "advice": "Vérifiez votre configuration client."}
    elif 500 <= code < 600:
        return {"title": f"Erreur Serveur {code}", "message": "Le serveur a rencontré un problème spécifique inconnu.", "advice": "Contactez le support technique."}

    return {
        "title": f"Code {code}",
        "message": "Statut HTTP non répertorié ou inhabituel.",
        "advice": "Veuillez vous référer au Trace ID."
    }