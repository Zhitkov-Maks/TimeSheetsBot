from sqlalchemy import Integer, String, Float, BIGINT, SMALLINT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_conf import Base


class Settings(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_chat_id: Mapped[int] = mapped_column(BIGINT)
    price: Mapped[int] = mapped_column(Integer, default=300)
    overtime: Mapped[int] = mapped_column(Integer, default=100)


class Salary(Base):
    __tablename__ = "salary"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_chat_id: Mapped[int] = mapped_column(BIGINT)
    base_hours: Mapped[float] = mapped_column(Float)
    overtime: Mapped[float] = mapped_column(Float)
    earned: Mapped[float] = mapped_column(Float)
    date: Mapped[str] = mapped_column(String)
    period: Mapped[int] = mapped_column(Integer, default=1)


class Remind(Base):
    __tablename__ = "reminds"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[int] = mapped_column(SMALLINT)
    user_chat_id: Mapped[int] = mapped_column(BIGINT, unique=True)
