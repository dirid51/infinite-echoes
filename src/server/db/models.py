import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy import String, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from src.server.db.session import Base

class Entity(Base):
    """
    The Core Atom of the Infinite Echoes world.
    
    Hybrid Architecture:
    1. SQL: Identity and Location (Fast Lookups).
    2. JSONB: Mechanics and State (Flexible D&D 5e Stats).
    3. Vector: Semantic 'Vibe' (AI Retrieval).
    """
    __tablename__ = "entities"

    # --- Identity & Metadata ---
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()") # Native Postgres UUID generation
    )
    name: Mapped[str] = mapped_column(String, index=True)
    kind: Mapped[str] = mapped_column(String, index=True) # e.g., 'player', 'npc', 'monster', 'prop'
    
    # --- Spatial Indexing ---
    # We use a string ID for zones (e.g., "crypt_level_1") to decouple from strict FK constraints 
    # during lazy generation, or we can use a strict FK if Zones are pre-generated.
    # For now, we use a string to allow "Phantom Zones" generated on the fly.
    zone_id: Mapped[str] = mapped_column(String, index=True, nullable=True)

    # --- The "Component" Bag (Hybrid Layer) ---
    # Stores strict mechanics data: 
    # {
    #   "stats": {"str": 18, "dex": 12}, 
    #   "hp": {"current": 20, "max": 20}, 
    #   "ac": 14,
    #   "inventory": ["sword", "shield"]
    # }
    attributes: Mapped[Dict[str, Any]] = mapped_column(JSONB, default={}, server_default=text("'{}'::jsonb"))
    
    # --- Narrative State ---
    # Mutable description changed by the AI (e.g., "Standing proudly" -> "Bleeding heavily")
    description: Mapped[str] = mapped_column(String, default="")
    
    # --- Dream Protocol (AI Layer) ---
    # 1536 dimensions matches OpenAI's text-embedding-3-small
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(1536), nullable=True)
    
    # --- Timestamps ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def get_stat(self, stat_name: str, default: int = 10) -> int:
        """Helper to safely retrieve nested D&D stats."""
        stats = self.attributes.get("stats", {})
        return stats.get(stat_name, default)

    def __repr__(self):
        return f"<Entity(id={self.id}, name='{self.name}', kind='{self.kind}')>"


class Zone(Base):
    """
    Represents a location in the world.
    Stored separately to allow for 'Biomes' and broad semantic searches.
    """
    __tablename__ = "zones"
    
    id: Mapped[str] = mapped_column(String, primary_key=True) # e.g., "whispering_woods"
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    
    # Atmospheric Embedding (e.g., "Scary, Dark, Damp")
    # Used to seed the 'Mood' of the narrator when entering this zone.
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(1536), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )