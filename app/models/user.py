from sqlalchemy.orm import Mapped
from app.db.database import Base, str_uniq, int_pk


class User(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str_uniq]
    password: Mapped[str]