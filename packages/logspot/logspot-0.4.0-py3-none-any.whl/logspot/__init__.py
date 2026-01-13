from .manager import LogManager
from .blueprint import create_logs_blueprint
from .fastapi_blueprint import create_logs_router
from typing import Optional

def setup_logs(app, service="app", log_dir: str = "logs", telegram_chat_id: str | None = None, telegram_bot_token: Optional[str] = None, logs_user: str | None = None, logs_pass: str | None = None):
    """
    Configure file-based logging and attach a protected `/logs` endpoint to a Flask or FastAPI app.

    This function initializes a `LogManager`, creates the log file, and automatically
    registers a route for viewing and downloading logs. The route is protected using
    HTTP Basic Authentication if `logs_user` and `logs_pass` are provided.

    The logging methods are also attached directly to the app instance as:
    `app.log_info`, `app.log_debug`, `app.log_warn`, `app.log_error`, `app.log_critical`.

    Parameters
    ----------
    app : Flask | FastAPI
        Application instance. Must support `register_blueprint` (Flask)
        or `include_router` (FastAPI).

    service : str, default="app"
        Logical service name used for log file naming and alert messages.

    log_dir : str, default="logs"
        Directory where log files will be stored.

    telegram_chat_id : str | None, optional
        Default Telegram chat ID for error and critical alerts.
        If None, the environment variable `TELEGRAM_CHAT_ID` may be used.

    telegram_bot_token : str | None, optional
        Telegram bot token used to send alerts.
        If None, the environment variable `TELEGRAM_BOT_TOKEN` may be used.

    logs_user : str | None, optional
        Username for HTTP Basic Authentication on the `/logs` endpoint.
        If None, authentication can be disabled or loaded from environment variables.
        
    logs_pass : str | None, optional
        Password for HTTP Basic Authentication on the `/logs` endpoint.

    Returns
    -------
    LogManager
        The initialized LogManager instance for manual logging control if needed.

    Raises
    ------
    RuntimeError
        If the provided application object is not Flask or FastAPI compatible.
    """
    manager = LogManager(service=service, log_dir=log_dir, telegram_chat_id=telegram_chat_id, telegram_bot_token=telegram_bot_token)
    download_name = f"{service}.log"
    
    # Flask
    if hasattr(app, "register_blueprint"):
        bp = create_logs_blueprint(manager.log_file, download_name=download_name, username=logs_user,password=logs_pass)
        app.register_blueprint(bp)

    # FastAPI
    elif hasattr(app, "include_router"):
        router = create_logs_router(manager.log_file, download_name=download_name, username=logs_user,password=logs_pass)
        app.include_router(router)
    
    else:
        raise RuntimeError("Unsupported application type: must be Flask or FastAPI")

    app.log_info = manager.info
    app.log_debug = manager.debug
    app.log_warn = manager.warn
    app.log_error = manager.error
    app.log_critical = manager.critical

    return manager

