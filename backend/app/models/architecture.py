from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.database import Base


class Architecture(Base):
    __tablename__ = "architectures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repo_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    architecture_type: Mapped[str] = mapped_column(String(128), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    repository: Mapped["Repository"] = relationship(
        "Repository",
        back_populates="architectures",
    )

    def __repr__(self) -> str:
        return (
            f"<Architecture id={self.id!r} "
            f"repo_id={self.repo_id!r} "
            f"type={self.architecture_type!r} "
            f"confidence={self.confidence_score!r}>"
        )