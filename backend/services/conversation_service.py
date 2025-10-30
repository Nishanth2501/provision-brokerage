"""
Conversation Service - Handles chat sessions and message history
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import desc
from models.conversation import Conversation


class ConversationService:
    """Service for managing chat conversations and tracking qualification progress."""

    def __init__(self, db: Session):
        self.db = db

    def create_conversation(
        self, session_id: str, channel: str = "web", lead_id: Optional[int] = None
    ) -> Conversation:
        """
        Create a new conversation session.

        Args:
            session_id: Unique session identifier (UUID recommended)
            channel: Communication channel (web, sms, whatsapp, facebook)
            lead_id: Optional lead ID if linked to existing lead

        Returns:
            Conversation: Created conversation object
        """
        conversation = Conversation(
            session_id=session_id,
            channel=channel,
            lead_id=lead_id,
            messages=[],
            qualification_progress=0,
            qualification_answers={},
            context={},
            is_qualified=False,
            appointment_booked=False,
        )

        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_conversation(self, session_id: str) -> Optional[Conversation]:
        """
        Retrieve conversation by session ID.

        Args:
            session_id: Session identifier

        Returns:
            Conversation or None if not found
        """
        return (
            self.db.query(Conversation)
            .filter(Conversation.session_id == session_id)
            .first()
        )

    def get_or_create_conversation(
        self, session_id: str, channel: str = "web"
    ) -> Conversation:
        """
        Get existing conversation or create new one.

        Args:
            session_id: Session identifier
            channel: Communication channel

        Returns:
            Conversation: Existing or new conversation
        """
        conversation = self.get_conversation(session_id)

        if not conversation:
            conversation = self.create_conversation(session_id, channel)

        return conversation

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Conversation:
        """
        Add a message to the conversation.

        Args:
            session_id: Session identifier
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata (e.g., qualification data, intent)

        Returns:
            Conversation: Updated conversation
        """
        conversation = self.get_conversation(session_id)

        if not conversation:
            raise ValueError(f"Conversation {session_id} not found")

        # Create message object
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
        }

        if metadata:
            message["metadata"] = metadata

        # Add to messages array
        if conversation.messages is None:
            conversation.messages = []

        conversation.messages.append(message)
        conversation.updated_at = datetime.utcnow()

        # Mark JSON field as modified for SQLAlchemy to detect changes
        flag_modified(conversation, "messages")

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def update_qualification(
        self,
        session_id: str,
        progress: int,
        answers: Dict[str, Any],
        is_qualified: bool = False,
    ) -> Conversation:
        """
        Update qualification progress and answers.

        Args:
            session_id: Session identifier
            progress: Qualification progress (0-7)
            answers: Dictionary of qualification answers
            is_qualified: Whether lead is qualified for appointment

        Returns:
            Conversation: Updated conversation
        """
        conversation = self.get_conversation(session_id)

        if not conversation:
            raise ValueError(f"Conversation {session_id} not found")

        conversation.qualification_progress = progress
        conversation.qualification_answers = answers
        conversation.is_qualified = is_qualified
        conversation.updated_at = datetime.utcnow()

        # Mark JSON field as modified for SQLAlchemy to detect changes
        flag_modified(conversation, "qualification_answers")

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def mark_appointment_booked(self, session_id: str) -> Conversation:
        """
        Mark conversation as having booked appointment.

        Args:
            session_id: Session identifier

        Returns:
            Conversation: Updated conversation
        """
        conversation = self.get_conversation(session_id)

        if not conversation:
            raise ValueError(f"Conversation {session_id} not found")

        conversation.appointment_booked = True
        conversation.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def update_context(
        self, session_id: str, context_updates: Dict[str, Any]
    ) -> Conversation:
        """
        Update conversation context with additional information.

        Args:
            session_id: Session identifier
            context_updates: Dictionary of context updates

        Returns:
            Conversation: Updated conversation
        """
        conversation = self.get_conversation(session_id)

        if not conversation:
            raise ValueError(f"Conversation {session_id} not found")

        if conversation.context is None:
            conversation.context = {}

        conversation.context.update(context_updates)
        conversation.updated_at = datetime.utcnow()

        # Mark JSON field as modified for SQLAlchemy to detect changes
        flag_modified(conversation, "context")

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_message_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get message history for conversation.

        Args:
            session_id: Session identifier
            limit: Optional limit on number of messages

        Returns:
            List of messages
        """
        conversation = self.get_conversation(session_id)

        if not conversation or not conversation.messages:
            return []

        messages = conversation.messages

        if limit:
            messages = messages[-limit:]

        return messages

    def link_to_lead(self, session_id: str, lead_id: int) -> Conversation:
        """
        Link conversation to a lead.

        Args:
            session_id: Session identifier
            lead_id: Lead ID to link to

        Returns:
            Conversation: Updated conversation
        """
        conversation = self.get_conversation(session_id)

        if not conversation:
            raise ValueError(f"Conversation {session_id} not found")

        conversation.lead_id = lead_id
        conversation.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(conversation)

        return conversation

    def get_recent_conversations(
        self, limit: int = 10, channel: Optional[str] = None
    ) -> List[Conversation]:
        """
        Get recent conversations.

        Args:
            limit: Number of conversations to retrieve
            channel: Optional channel filter

        Returns:
            List of conversations
        """
        query = self.db.query(Conversation)

        if channel:
            query = query.filter(Conversation.channel == channel)

        return query.order_by(desc(Conversation.updated_at)).limit(limit).all()


# Test function
if __name__ == "__main__":
    from core.database import SessionLocal, init_db
    import uuid

    # Initialize database
    init_db()

    # Create test session
    db = SessionLocal()
    service = ConversationService(db)

    # Test: Create conversation
    session_id = str(uuid.uuid4())
    print(f"\n1. Creating conversation with session_id: {session_id}")
    conversation = service.create_conversation(session_id, "web")
    print(f" Created: {conversation.session_id}")

    # Test: Add messages
    print("\n2. Adding messages...")
    service.add_message(session_id, "user", "Hi, I'm interested in retirement planning")
    service.add_message(
        session_id, "assistant", "Great! I'd love to help. How old are you?"
    )
    print(f" Added 2 messages")

    # Test: Get message history
    print("\n3. Retrieving message history...")
    messages = service.get_message_history(session_id)
    print(f" Retrieved {len(messages)} messages")
    for msg in messages:
        print(f"   {msg['role']}: {msg['content'][:50]}...")

    # Test: Update qualification
    print("\n4. Updating qualification...")
    service.update_qualification(
        session_id,
        progress=2,
        answers={"age_range": "50-59", "retirement_timeline": "5-10 years"},
        is_qualified=False,
    )
    print(" Qualification updated")

    # Test: Get conversation
    print("\n5. Retrieving conversation...")
    conv = service.get_conversation(session_id)
    print(f" Progress: {conv.qualification_progress}/7")
    print(f"   Qualified: {conv.is_qualified}")
    print(f"   Messages: {len(conv.messages)}")

    print("\n All conversation service tests passed!")

    db.close()
