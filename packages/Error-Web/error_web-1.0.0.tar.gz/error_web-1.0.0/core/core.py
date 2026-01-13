import uuid
import logging
import os
from flask import render_template, jsonify, request
from werkzeug.exceptions import HTTPException

logger = logging.getLogger("flask_error_manager")
logging.basicConfig(level=logging.INFO)

def init_error_manager(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        trace_id = str(uuid.uuid4())
        if isinstance(e, HTTPException):
            code = e.code
            message = e.description
        else:
            code = 500
            message = "Une erreur interne est survenue"
            logger.exception(f"[{trace_id}] Erreur non gérée: {e}")

        if wants_json():
            return jsonify({
                "status": "error",
                "code": code,
                "message": message,
                "trace_id": trace_id
            }), code

        template_folder = os.path.join(os.path.dirname(__file__), "templates")
        app.template_folder = template_folder

        return render_template(
            "base.html",
            code=code,
            message=message,
            trace_id=trace_id
        ), code

def wants_json():
    accept = request.headers.get("Accept", "")
    return "application/json" in accept or "application/vnd.api+json" in accept