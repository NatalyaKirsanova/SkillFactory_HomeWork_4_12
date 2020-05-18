import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


class Athelete(Base):
    __tablename__ = 'athelete'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)


def connect_db():
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def find_user(id, session):
    query = session.query(User).filter(User.id == id)
    instance = query.first()
    if instance is None:
        print("Пользователя с таким id не существует!")
        exit()
    else:
        return(instance)

def find_Athelete(birthdate_athelete, height_athelete, session):

    query_height = session.query(Athelete).filter(Athelete.height >= height_athelete).order_by(Athelete.height.asc())
    query_h = query_height.first()
    if query_h is None:
        query_height = session.query(Athelete).filter(Athelete.height <= height_athelete).order_by(Athelete.height.desc())
        query_h = query_height.first()


    query_birthdate = session.query(Athelete).filter(Athelete.birthdate <= birthdate_athelete).order_by(Athelete.birthdate.desc())
    query_b = query_birthdate.first()
    if query_b is None:
        query_birthdate = session.query(Athelete).filter(Athelete.birthdate >= birthdate_athelete).order_by(Athelete.birthdate.asc())
        query_b = query_birthdate.first()

    return(query_h,query_b)

def main():
    session = connect_db()
    user_id=input("Введите id пользователя:")
    user = find_user(user_id,session)
    print("Введен пользователь: /id: {} /name: {} /bithdate: {} /height: {}/".format(user.id, user.first_name+" "+user.last_name, user.birthdate, user.height))
    athelete_h, athelete_b =find_Athelete(user.birthdate,user.height,session)
    print("Атлет, ближайший по дате рождения: /id: {} /name: {} /bithdate: {}/".format(athelete_b.id,athelete_b.name,athelete_b.birthdate))
    print("Атлет, ближайший росту: /id: {} /name: {} /height: {}/".format(athelete_h.id,athelete_h.name,athelete_h.height))

if __name__ == "__main__":
    main()