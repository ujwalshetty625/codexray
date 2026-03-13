from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.database import Base


class EngineeringReview(Base):
    __tablename__ = "engineering_reviews"

    id:         Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    repo_id:    Mapped[str] = mapped_column(String(36), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True)
    summary:    Mapped[str] = mapped_column(Text, nullable=False)
    strengths:  Mapped[str] = mapped_column(Text, nullable=False)
    weaknesses: Mapped[str] = mapped_column(Text, nullable=False)
    suggestions:Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    repository: Mapped["Repository"] = relationship("Repository", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<EngineeringReview id={self.id!r} repo_id={self.repo_id!r}>"