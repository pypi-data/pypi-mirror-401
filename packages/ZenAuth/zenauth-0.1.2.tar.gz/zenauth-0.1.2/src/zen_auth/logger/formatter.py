import json
import logging
from datetime import datetime, timedelta, timezone


class AuditFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.fromtimestamp(record.created, timezone(timedelta(hours=9))).isoformat(
            timespec="milliseconds"
        )

        log_data: dict[str, object] = {
            "ts": ts,
            "logger": record.name,
            "msg": record.getMessage(),
        }

        request = getattr(record, "request", None)
        if request:
            log_data.update(
                {
                    "req_id": getattr(request.state, "req_id", "--"),
                    "path": request.url.path,
                    "method": request.method,
                    "ip": request.client.host if request.client else "--",
                    "ua": request.headers.get("user-agent", "--"),
                    "url": str(request.url),
                }
            )

        log_data["user_name"] = getattr(record, "user_name", "--")
        log_data["result"] = getattr(record, "result", "--")
        # required_context: authorization context such as role/scope
        required_context = getattr(record, "required_context", None)
        if required_context is not None:
            log_data["required_context"] = required_context

        return json.dumps({k: v for k, v in log_data.items() if v is not None}, ensure_ascii=False)
