from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    repo_url: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    default_branch: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="main",
    )
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    jobs: Mapped[list["AnalysisJob"]] = relationship(
        "AnalysisJob",
        back_populates="repository",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    files: Mapped[list["FileRecord"]] = relationship(
        "FileRecord",
        back_populates="repository",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    dependencies: Mapped[list["Dependency"]] = relationship(
        "Dependency",
        back_populates="repository",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    architectures: Mapped[list["Architecture"]] = relationship(
        "Architecture",
        back_populates="repository",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    reviews: Mapped[list["EngineeringReview"]] = relationship(
    "EngineeringReview",
    back_populates="repository",
    cascade="all, delete-orphan",
    lazy="selectin",
)

    def __repr__(self) -> str:
        return f"<Repository id={self.id!r} owner={self.owner!r} name={self.name!r}>"