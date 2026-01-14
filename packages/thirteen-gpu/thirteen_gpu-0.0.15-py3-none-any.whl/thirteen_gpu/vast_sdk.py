import json
import os
from typing import Any, Dict, List, Optional, Tuple


def _get_vast_api_key(api_key: Optional[str] = None) -> str:
    if api_key:
        return api_key
    api_key = os.getenv("VASTAI_API_KEY") or os.getenv("VAST_API_KEY")
    if api_key:
        return api_key
    # 로컬/서버에서 ~/.vast_api_key 파일로 관리하는 경우도 지원
    try:
        key_path = os.path.expanduser("~/.vast_api_key")
        with open(key_path, "r") as f:
            file_key = f.read().strip()
        if file_key:
            return file_key
    except Exception:
        pass
    raise ValueError(
        "Vast API key가 없습니다. `VASTAI_API_KEY`(또는 `VAST_API_KEY`) 환경변수를 설정하거나 "
        "함수 인자로 api_key를 전달하세요."
    )


def _parse_vast_output(raw: Any, last_output: Optional[str]) -> Any:
    if isinstance(raw, (list, dict)):
        return raw
    if raw is None and last_output:
        raw = last_output
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            return raw
    return raw


def get_vast_template_hash_id(
    template_name: str,
    *,
    api_key: Optional[str] = None,
    server_url: str = "https://console.vast.ai",
) -> str:
    """Vast 템플릿 이름으로 hash_id(=template_hash)를 구한다.

    Vast에 동일 이름 템플릿이 여러 개면 created_at이 가장 최신인 것을 사용.
    """
    try:
        from vastai import VastAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)
    raw = client.search_templates(query=f"name={template_name}")
    parsed = _parse_vast_output(raw, getattr(client, "last_output", None))

    if not isinstance(parsed, list):
        raise RuntimeError(f"templates 응답 포맷이 예상과 다릅니다: {parsed!r}")

    candidates: List[Tuple[float, Dict[str, Any]]] = []
    for t in parsed:
        if not isinstance(t, dict):
            continue
        if t.get("name") != template_name:
            continue
        hash_id = t.get("hash_id")
        if not hash_id:
            continue
        created_at = float(t.get("created_at") or 0.0)
        candidates.append((created_at, t))

    if not candidates:
        raise RuntimeError(f"'{template_name}' 템플릿을 찾지 못했습니다.")

    candidates.sort(key=lambda x: x[0], reverse=True)
    return str(candidates[0][1]["hash_id"])


def create_vast_instances_from_offers(
    offer_ids: List[int],
    *,
    disk_gb: int,
    user_tag: str,
    template_name: str = "thirteen",
    api_key: Optional[str] = None,
    server_url: str = "https://console.vast.ai",
) -> Dict[str, Any]:
    """offer id(=contract offer) 리스트로 인스턴스 생성. 템플릿 강제."""
    try:
        from vastai import VastAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)

    template_hash = get_vast_template_hash_id(
        template_name, api_key=api_key, server_url=server_url
    )

    results = []
    errors = []

    for oid in offer_ids:
        try:
            raw = client.create_instance(
                id=int(oid),
                template_hash=template_hash,
                disk=float(disk_gb),
                label=f"{user_tag}",
            )
            parsed = _parse_vast_output(raw, getattr(client, "last_output", None))
            results.append({"offer_id": oid, "response": parsed})
        except Exception as e:
            errors.append({"offer_id": oid, "error": str(e)})

    return {
        "template_name": template_name,
        "template_hash": template_hash,
        "created": results,
        "errors": errors,
    }


def list_vast_instances(
    *,
    api_key: Optional[str] = None,
    server_url: str = "https://console.vast.ai",
) -> List[Dict[str, Any]]:
    """내 계정의 Vast 인스턴스 목록(raw)."""
    try:
        from vastai import VastAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)
    raw = client.show_instances()
    parsed = _parse_vast_output(raw, getattr(client, "last_output", None))
    if not isinstance(parsed, list):
        raise RuntimeError(f"instances 응답 포맷이 예상과 다릅니다: {parsed!r}")
    return parsed


def destroy_vast_instances(
    instance_ids: List[int],
    *,
    api_key: Optional[str] = None,
    server_url: str = "https://console.vast.ai",
) -> Dict[str, Any]:
    """인스턴스 다중 삭제(DESTROY, irreversible)."""
    try:
        from vastai import VastAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)

    destroyed = []
    errors = []
    for iid in instance_ids:
        try:
            raw = client.destroy_instance(id=int(iid))
            parsed = _parse_vast_output(raw, getattr(client, "last_output", None))
            destroyed.append({"id": int(iid), "response": parsed})
        except Exception as e:
            errors.append({"id": int(iid), "error": str(e)})

    return {"destroyed": destroyed, "errors": errors}


def stop_vast_instances(
    instance_ids: List[int],
    *,
    api_key: Optional[str] = None,
    server_url: str = "https://console.vast.ai",
) -> Dict[str, Any]:
    """인스턴스 다중 stop."""
    try:
        from vastai import VastAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)

    stopped = []
    errors = []
    for iid in instance_ids:
        try:
            raw = client.stop_instance(id=int(iid))
            parsed = _parse_vast_output(raw, getattr(client, "last_output", None))
            stopped.append({"id": int(iid), "response": parsed})
        except Exception as e:
            errors.append({"id": int(iid), "error": str(e)})

    return {"stopped": stopped, "errors": errors}


def start_vast_instances(
    instance_ids: List[int],
    *,
    api_key: Optional[str] = None,
    server_url: str = "https://console.vast.ai",
) -> Dict[str, Any]:
    """인스턴스 다중 start."""
    try:
        from vastai import VastAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)

    started = []
    errors = []
    for iid in instance_ids:
        try:
            raw = client.start_instance(id=int(iid))
            parsed = _parse_vast_output(raw, getattr(client, "last_output", None))
            started.append({"id": int(iid), "response": parsed})
        except Exception as e:
            errors.append({"id": int(iid), "error": str(e)})

    return {"started": started, "errors": errors}


def reboot_vast_instances(
    instance_ids: List[int],
    *,
    api_key: Optional[str] = None,
    server_url: str = "https://console.vast.ai",
) -> Dict[str, Any]:
    """인스턴스 다중 reboot."""
    try:
        from vastai import VastAI
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)

    rebooted = []
    errors = []
    for iid in instance_ids:
        try:
            raw = client.reboot_instance(id=int(iid))
            parsed = _parse_vast_output(raw, getattr(client, "last_output", None))
            rebooted.append({"id": int(iid), "response": parsed})
        except Exception as e:
            errors.append({"id": int(iid), "error": str(e)})

    return {"rebooted": rebooted, "errors": errors}


def search_vast_offers(
    query: str,
    *,
    api_key: Optional[str] = None,
    limit: Optional[int] = 50,
    order: Optional[str] = None,
    offer_type: Optional[str] = None,
    storage: Optional[float] = None,
    disable_bundling: bool = False,
    no_default: bool = False,
    new: bool = False,
    server_url: str = "https://console.vast.ai",
) -> List[Dict[str, Any]]:
    """Vast.ai offers 검색(SDK).

    - query: Vast query string (예: "gpu_name=RTX_4090 rentable=true rented=false dph_total<1.0")
    - 반환: offer dict 리스트 (SDK의 raw JSON을 파싱한 결과)
    """
    try:
        from vastai import VastAI  # vastai-sdk 패키지가 제공
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "vastai-sdk가 설치되어 있지 않습니다. `pip install vastai-sdk` 후 다시 실행하세요."
        ) from e

    api_key = _get_vast_api_key(api_key)
    client = VastAI(api_key=api_key, server_url=server_url, raw=True, quiet=True)

    # 주의: vastai-sdk에서 `storage=None`처럼 None을 "명시적으로" 넘기면
    # 빈 결과가 나오는 케이스가 있어, None 값은 아예 파라미터에서 제거한다.
    kwargs: Dict[str, Any] = {
        "no_default": no_default,
        "new": new,
        "disable_bundling": disable_bundling,
        "query": query,
    }
    if offer_type is not None:
        kwargs["type"] = offer_type
    if limit is not None:
        kwargs["limit"] = limit
    if storage is not None:
        kwargs["storage"] = storage
    if order is not None:
        kwargs["order"] = order

    raw = client.search_offers(**kwargs)

    if isinstance(raw, (list, dict)):
        return raw  # type: ignore[return-value]

    try:
        parsed = json.loads(raw)
    except Exception as e:
        raise RuntimeError(f"offers 응답 JSON 파싱 실패: {raw!r}") from e

    if isinstance(parsed, dict) and "offers" in parsed and isinstance(parsed["offers"], list):
        return parsed["offers"]
    if isinstance(parsed, list):
        return parsed

    raise RuntimeError(f"offers 응답 포맷이 예상과 다릅니다: {parsed!r}")