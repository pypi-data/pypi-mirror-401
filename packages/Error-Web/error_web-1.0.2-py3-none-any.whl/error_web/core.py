import uuid
from flask import jsonify, render_template, request, current_app
from .codes_http import get_http_info

def init_app(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        code = getattr(e, 'code', 500)
        trace_id = str(uuid.uuid4())[:8].upper()
        info = get_http_info(code)
        
        error_type = e.__class__.__name__
        if isinstance(e, ZeroDivisionError):
            info["title"] = "Calcul Impossible"
            info["message"] = "Une tentative de division par zéro a été détectée."
            info["advice"] = "Vérifiez les calculs ou les entrées utilisateur."
        elif isinstance(e, KeyError):
            info["title"] = "Donnée Introuvable"
            info["message"] = "Le système a tenté d'accéder à une clé inexistante."

        context = {
            "code": code,
            "trace_id": trace_id,
            "title": info["title"],
            "message": info["message"],
            "advice": info["advice"],
            "type": error_type
        }

        current_app.logger.error(f"[{trace_id}] {error_type} : {str(e)}")

        if request.is_json or request.path.startswith('/api/'):
            return jsonify({"status": "error", "error": context}), code

        try:
            return render_template("errors/error.html", **context), code
        except:
            return f"<h1>{context['title']} ({code})</h1><p>{context['message']}</p><small>ID: {trace_id}</small>", code
