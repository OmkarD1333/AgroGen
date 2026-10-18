from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.dependencies.db import get_db, get_current_user
from app.database.models import User, ChatMessage
from app.schemas.agriculture import ChatMessageRequest, ChatMessageResponse
from app.services.chat_service import answer_farmer_query

chatbot_router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@chatbot_router.post("/chat", response_model=ChatMessageResponse)
async def chat(
    chat_req: ChatMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Store user query
    user_msg = ChatMessage(
        user_id=current_user.id,
        role="user",
        content=chat_req.message,
        language=chat_req.language or "mr",
    )
    db.add(user_msg)
    db.commit()

    # Generate answer
    bot_reply = answer_farmer_query(chat_req.message, language=chat_req.language or "mr")

    # Store bot answer
    bot_msg = ChatMessage(
        user_id=current_user.id,
        role="assistant",
        content=bot_reply,
        language=chat_req.language or "mr",
    )
    db.add(bot_msg)
    db.commit()

    return ChatMessageResponse(
        response=bot_reply,
        language=chat_req.language or "mr",
        timestamp=datetime.now(timezone.utc),
    )


@chatbot_router.get("/history")
async def chat_history(
    limit: int = Query(default=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == current_user.id)
        .order_by(ChatMessage.created_at.asc())
        .limit(limit)
        .all()
    )
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "language": m.language,
            "created_at": m.created_at,
        }
        for m in messages
    ]
