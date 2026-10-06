"""Active recognition sessions endpoint."""

import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db_session
from app.models.session import RecognitionSession
from app.schemas.session import SessionCreate, SessionResponse

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: SessionCreate,
    db: AsyncSession = Depends(get_db_session),
) -> SessionResponse:
    """Initialize a new gesture streaming session."""
    session = RecognitionSession(
        client_id=payload.client_id,
        status="active",
        total_frames_processed=0,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return SessionResponse.model_validate(session)


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db_session),
) -> SessionResponse:
    """Retrieve recognition session state."""
    session = await db.get(RecognitionSession, session_id)
    if not session:
        return SessionResponse(
            id=session_id,
            client_id="anonymous",
            status="inactive",
            total_frames_processed=0,
            created_at=None,
        )
    return SessionResponse.model_validate(session)
