from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.db.database import Base


class Dependency(Base):
    __tablename__ = "dependencies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    repo_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    source_file: Mapped[str] = mapped_column(String(1024), nullable=False)
    target_file: Mapped[str] = mapped_column(String(1024), nullable=False)
    dependency_type: Mapped[str] = mapped_column(String(64), nullable=True, default="import")

    repository: Mapped["Repository"] = relationship(
        "Repository",
        back_populates="dependencies",
    )

    def __repr__(self) -> str:
        return (
            f"<Dependency id={self.id!r} "
            f"source={self.source_file!r} "
            f"target={self.target_file!r}>"
        )