import sqlalchemy


def create_database(db_name):
    postgres = "mydatabase"
    localhost = "5432"
    try:
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{postgres}@localhost:{localhost}/postgres")
        connection = engine.connect()
        connection.execute("commit")
        connection.execute(f"create database {db_name}")
        connection.close()
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{postgres}@localhost:{localhost}/{db_name}")
        connection = engine.connect()
        create_table(connection)
        return connection
    except sqlalchemy.exc.ProgrammingError:
        engine = sqlalchemy.create_engine(f"postgresql://postgres:{postgres}@localhost:{localhost}/{db_name}")
        connection = engine.connect()
        return connection
    except sqlalchemy.exc.OperationalError:
        print("Ошибка подключения к базе данных")


def create_table(arg):
    arg.execute("""CREATE TABLE IF NOT EXISTS user_id (
    id SERIAL PRIMARY KEY,
    url_id VARCHAR(50) NOT NULL UNIQUE);""")

    arg.execute("""CREATE TABLE IF NOT EXISTS photo (
    id SERIAL REFERENCES user_id(id),
    photo_url text );""")


def insert_data(arg_1, arg):
    try:
        for i in arg:
            uid, url = i.items()
            insert = f"INSERT INTO user_id(id, url_id) VALUES('{uid[0]}', '{uid[1]}');"
            arg_1.execute(insert)
            for photo in url[1]:
                photo_url = list(photo.items())[0][1]
                insert = f"INSERT INTO photo(id, photo_url) VALUES('{uid[0]}', '{photo_url}');"
                arg_1.execute(insert)
    except AttributeError:
        print("Ошибка подключения к базе данных, запись данных не возможна")


def select_user_id(arg):
    list_id = []
    try:
        for i in arg.execute("""SELECT id FROM user_id""").fetchall():
            list_id.append(i[0])
        return list_id
    except AttributeError:
        print("Ошибка подключения к базе данных, получение данных из БД не возможна")
        return list_id
