import os
from flask import Blueprint, Response, abort, request
import base64

def create_logs_blueprint(log_file: str, download_name: str = "logs.txt", username: str | None = None, password: str | None = None):
    bp = Blueprint("central_logs", __name__)
    USER = username or os.getenv("LOGS_USER")
    PASS = password or os.getenv("LOGS_PASS")

    def check_auth():
        if not USER or not PASS:
            return True

        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Basic "):
            return False

        try:
            decoded = base64.b64decode(auth.split(" ", 1)[1]).decode()
            u, p = decoded.split(":", 1)
        except Exception:
            return False

        return u == USER and p == PASS
    
    @bp.before_request
    def protect():
        if not check_auth():
            return Response(
                "Unauthorized",
                401,
                {"WWW-Authenticate": 'Basic realm="Logs"'},
            )

    @bp.route("/logs")
    def view_logs():

        if not os.path.exists(log_file):
            return Response("(no logs yet)", mimetype="text/plain")

        # ?limit=200 (default 200)
        try:
            limit = int(request.args.get("limit", 200))
        except ValueError:
            limit = 200

        if limit <= 0:
            limit = 200
        
        level = request.args.get("level")
        if level:
            level = level.upper().strip()

        search = request.args.get("search")
        if search:
            search = search.strip().lower()
        
        download_flag = request.args.get("download", "0").lower() in ("1", "true", "yes", "y")

        try:
            with open(log_file, "r", encoding="utf-8") as f:
                data = f.read()
        except Exception as e:
            abort(500, description=str(e))

        lines = data.strip().split("\n")
        if level:
            level_pattern = f"- {level} -"
            lines = [line for line in lines if level_pattern in line]
        
        if search:
            lines = [line for line in lines if search in line.lower()]
        
        if limit and len(lines) > limit:
            lines = lines[-limit:]

        final_text = "\n".join(lines) if lines else "(no matching logs)"

        headers = {}
        if download_flag:
            headers["Content-Disposition"] = f'attachment; filename="{download_name}"'

        return Response(final_text, mimetype="text/plain", headers=headers)

    return bp
