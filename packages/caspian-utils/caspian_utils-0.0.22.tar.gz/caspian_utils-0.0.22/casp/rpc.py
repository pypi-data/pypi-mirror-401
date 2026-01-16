import traceback
from datetime import timedelta
from .auth import auth
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from functools import wraps
from .caspian_config import get_files_index
from typing import Optional, Any
import inspect
import os
import json
import hmac
import dataclasses
from datetime import datetime, date

RPC_REGISTRY = {}
RPC_META = {}

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(
    ',') if os.getenv('CORS_ALLOWED_ORIGINS') else None
IS_PRODUCTION = os.getenv('APP_ENV') == 'production'

RATE_LIMIT_DEFAULT = os.getenv('RATE_LIMIT_DEFAULT', '200/minute')
RATE_LIMIT_RPC = os.getenv('RATE_LIMIT_RPC', '60/minute')
RATE_LIMIT_AUTH = os.getenv('RATE_LIMIT_AUTH', '10/minute')

limiter = Limiter(key_func=get_remote_address)


def _serialize_result(obj: Any) -> Any:
    """Convert objects to JSON-serializable format."""
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, date):
        return obj.isoformat()
    if isinstance(obj, (list, tuple)):
        return [_serialize_result(item) for item in obj]
    if isinstance(obj, dict):
        return {k: _serialize_result(v) for k, v in obj.items()}

    to_dict = getattr(obj, 'to_dict', None)
    if callable(to_dict):
        return _serialize_result(to_dict())

    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return {k: _serialize_result(v) for k, v in dataclasses.asdict(obj).items()}

    # Pydantic v2
    model_dump = getattr(obj, 'model_dump', None)
    if callable(model_dump):
        return model_dump()
    # Fallback to __dict__
    obj_dict = getattr(obj, '__dict__', None)
    if obj_dict is not None:
        return {k: _serialize_result(v) for k, v in obj_dict.items()}
    return str(obj)


def _filepath_to_route(filepath: str) -> str:
    files_index = get_files_index()
    filepath = filepath.replace('\\', '/')
    for route_entry in files_index.routes:
        if route_entry.fs_dir:
            pattern = f'/src/app/{route_entry.fs_dir}/index.py'
            if filepath.endswith(pattern) or pattern in filepath:
                return route_entry.url_path
        else:
            if filepath.endswith('/src/app/index.py'):
                return '/'
    return '/'


def rpc(require_auth: bool = False, allowed_roles: Optional[list[str]] = None):
    def decorator(func):
        frame = inspect.stack()[1]
        filepath = frame.filename
        route = _filepath_to_route(filepath)

        key = f"{route}:{func.__name__}"
        RPC_REGISTRY[key] = func
        RPC_META[key] = {
            'require_auth': require_auth,
            'allowed_roles': allowed_roles or [],
            'route': route
        }

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator


def _validate_origin(request: Request) -> Optional[JSONResponse]:
    origin = request.headers.get('Origin')
    if not origin:
        return None
    if not IS_PRODUCTION:
        if origin.startswith(('http://localhost:', 'http://127.0.0.1:')):
            return None
    host_url = str(request.base_url).rstrip('/')
    if CORS_ALLOWED_ORIGINS:
        if origin not in CORS_ALLOWED_ORIGINS and origin != host_url:
            return JSONResponse({'error': 'Invalid origin'}, status_code=403)
    elif origin != host_url:
        return JSONResponse({'error': 'Invalid origin'}, status_code=403)
    return None


def _validate_csrf(request: Request, session: dict) -> Optional[JSONResponse]:
    csrf_header = request.headers.get('X-CSRF-Token')
    session_token = session.get('csrf_token')

    if not csrf_header or not session_token:
        return JSONResponse({'error': 'Missing CSRF token'}, status_code=403)

    if not hmac.compare_digest(csrf_header, session_token):
        return JSONResponse({'error': 'Invalid CSRF token'}, status_code=403)
    return None


def _validate_content_type(request: Request) -> Optional[JSONResponse]:
    content_type = request.headers.get('content-type', '')
    if not content_type.startswith(('application/json', 'multipart/form-data')):
        content_length = request.headers.get('content-length')
        if content_length and int(content_length) > 0:
            return JSONResponse({'error': 'Invalid content type'}, status_code=415)
    return None


def _get_registry_key(route: str, func_name: str) -> Optional[str]:
    route = ('/' + route.strip('/')).rstrip('/') or '/'
    key = f"{route}:{func_name}"
    if key in RPC_REGISTRY:
        return key
    if func_name in RPC_REGISTRY:
        return func_name
    return None


async def _handle_rpc_request(request: Request, session: dict) -> Response:
    func_name = request.headers.get('X-PP-Function')
    if not func_name:
        return JSONResponse({'error': 'Missing function name'}, status_code=400)

    route = request.url.path.rstrip('/') or '/'
    registry_key = _get_registry_key(route, func_name)
    if not registry_key:
        return JSONResponse({'error': 'Function not found'}, status_code=404)

    if error := _validate_origin(request):
        return error
    if error := _validate_content_type(request):
        return error
    if error := _validate_csrf(request, session):
        return error

    meta = RPC_META.get(registry_key, {})

    if meta.get('require_auth') and not auth.is_authenticated():
        return JSONResponse({'error': 'Authentication required'}, status_code=401)

    allowed_roles = meta.get('allowed_roles', [])
    if allowed_roles:
        user = auth.get_payload()
        if not auth.check_role(user, allowed_roles):
            return JSONResponse({'error': 'Permission denied'}, status_code=403)

    content_type = request.headers.get('content-type', '')
    if content_type.startswith('multipart/form-data'):
        form = await request.form()
        data: dict[str, Any] = {}
        for key in form:
            value = form[key]
            if isinstance(value, str):
                try:
                    data[key] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    data[key] = value
            else:
                data[key] = value
    else:
        try:
            data = await request.json()
        except:
            data = {}

    try:
        result = RPC_REGISTRY[registry_key](**data)

        if isinstance(result, Response):
            location = result.headers.get("Location")
            status = result.status_code
            if location and 300 <= status < 400:
                resp = JSONResponse({"result": None})
                resp.headers["X-PP-Redirect"] = location
                resp.headers["X-PP-Redirect-Status"] = str(status)
                return resp
            return result

        return JSONResponse({'result': _serialize_result(result)})

    except PermissionError as e:
        return JSONResponse({'error': str(e)}, status_code=403)
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=400)
    except Exception as e:
        print(f"[RPC Error] {registry_key}: {e}")
        traceback.print_exc()  # This prints the full stack trace
        return JSONResponse({'error': 'Internal server error'}, status_code=500)


# Standalone middleware function (exported)
async def rpc_middleware(request: Request, call_next):
    session = dict(request.session) if hasattr(request, 'session') else {}

    if request.headers.get('X-PP-RPC') == 'true' and request.method == 'POST':
        return await _handle_rpc_request(request, session)

    response = await call_next(request)
    return response


def register_rpc_routes(app: FastAPI):
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse({'error': 'Rate limit exceeded. Please slow down.'}, status_code=429)
