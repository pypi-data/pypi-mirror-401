from . import constants
import requests
from typing import Dict, Any
from dotenv import load_dotenv
import os

class SDKClient:

    def __init__(self, api_key: str) -> None:
        load_dotenv()
        self._api_key: str = api_key
        self._endpoint: str = "https://api.tryflowstate.dev"
        self._endpoint_timeout: int = constants.SDK_ENDPOINT_TIMEOUT
        self._user_id: str | None = None
        if not self.__auth():
            raise AuthenticationError(constants.INVALID_AUTH_MESSAGE)
    
    # emit now takes dicts and dataclasses, and task_step_id is optional
    def emit(self, provider_metrics: Dict[Any, Any], task_step_id: str = None) -> None:
        payload: Dict = dict(provider_metrics) if isinstance(provider_metrics, dict) else {**vars(provider_metrics)}
        if task_step_id:
            payload[constants.TASK_STEP_ID] = task_step_id
        try:
            import json
            print("SDKClient.emit =>", json.dumps(payload, default=str))
        except Exception:
            print("SDKClient.emit => (failed to serialize payload)")

        safe_payload = {}
        import json
        for k, v in payload.items():
            if isinstance(v, set):
                safe_payload[k] = list(v)
                continue
            try:
                json.dumps(v)
                safe_payload[k] = v
            except Exception:
                try:
                    safe_payload[k] = str(v)
                except Exception:
                    safe_payload[k] = None
        try:
            response = requests.post(
                "https://api.tryflowstate.dev/sdk/metrics",
                json=safe_payload,
                timeout=constants.SDK_ENDPOINT_TIMEOUT
            )
            try:
                print("SDKClient.emit response:", response.status_code, response.text)
            except Exception:
                pass
            if response.status_code != 200:
                if os.environ.get("SKIP_SDK_METRICS"):
                    return
                raise MetricsDumpError(constants.METRICS_DUMP_ERROR)
        except Exception:
            if os.environ.get("SKIP_SDK_METRICS"):
                return
            raise
    
    def __auth(self) -> bool:
        auth_header: Dict[str, str] = {constants.AUTH_HEADER_NAME: self._api_key}
        try:
            resp: requests.Response = requests.post(
                "https://api.tryflowstate.dev/sdk/auth",
                headers=auth_header,
                timeout=constants.SDK_ENDPOINT_TIMEOUT
            )
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    self._user_id = data.get("user_id")
                except Exception:
                    self._user_id = None
            return resp.status_code == 200
        except:
            return False

    @property
    def user_id(self) -> str | None:
        return self._user_id

    def resolve_workflow_id(self, workflow_name: str) -> str | None:
        resolve_endpoint = "https://api.tryflowstate.dev/sdk/workflows/resolve"
        auth_header: Dict[str, str] = {constants.AUTH_HEADER_NAME: self._api_key}
        payload = {"workflow_name": workflow_name}
        try:
            resp: requests.Response = requests.post(
                resolve_endpoint,
                headers=auth_header,
                json=payload,
                timeout=constants.SDK_ENDPOINT_TIMEOUT
            )
            if resp.status_code != 200:
                return None
            data = resp.json()
            return data.get("workflow_id")
        except Exception:
            return None

class AuthenticationError(Exception):
    pass

class MetricsDumpError(Exception):
    pass
