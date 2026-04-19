from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, status

from app.core.exceptions import AppError


DEFAULT_OWNER_ID = UUID("00000000-0000-4000-8000-000000000001")
SCOPE_ERROR_PREFIXES = {
    "imports": "IMPORT",
    "analytics": "ANALYTICS",
    "daily_logs": "DAILY_LOGS",
    "ai_insights": "AI_INSIGHTS",
}


@dataclass(frozen=True)
class CurrentOwner:
    owner_id: UUID
    scopes: frozenset[str]


async def get_current_owner(
    x_request_id: Annotated[str | None, Header(alias="X-Request-Id")] = None,
) -> CurrentOwner:
    _ = x_request_id
    return CurrentOwner(
        owner_id=DEFAULT_OWNER_ID,
        scopes=frozenset(
            {
                "imports:read",
                "imports:write",
                "analytics:read",
                "daily_logs:read",
                "ai_insights:read",
                "ai_insights:write",
            }
        ),
    )


def require_scope(scope: str):
    async def dependency(owner: Annotated[CurrentOwner, Depends(get_current_owner)]) -> CurrentOwner:
        if scope not in owner.scopes:
            scope_domain = scope.split(":", maxsplit=1)[0]
            code_prefix = SCOPE_ERROR_PREFIXES.get(scope_domain, scope_domain.upper())
            raise AppError(
                f"{code_prefix}_PERMISSION_DENIED",
                "Authenticated user lacks the required read scope.",
                status_code=status.HTTP_403_FORBIDDEN,
                details={"required_scope": scope},
            )
        return owner

    return dependency
