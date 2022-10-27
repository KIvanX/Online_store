import psycopg2


class Database:
    def __init__(self):
        self.con = psycopg2.connect(
            dbname="Online_store",
            user="postgres",
            password="pass",
            host="localhost",
            port=5432
        )
        self.cur = self.con.cursor()

    def select(self, country=None, min_rating=0, film_id=None):
        if film_id is not None:
            self.cur.execute(f"SELECT * FROM films WHERE id = {film_id};")
        elif country is not None:
            self.cur.execute(f"SELECT * FROM films "
                             f"WHERE rating >= {min_rating} and country = '{country}';")
        else:
            self.cur.execute(f"SELECT * FROM films WHERE rating >= {min_rating};")

        data = self.prepare_data(self.cur.fetchall())

        return data

    def insert(self, new_film):
        self.cur.execute(f"INSERT INTO films VALUES(default, %s, %s, %s)",
                         (new_film['name'], new_film['rating'], new_film['country']))
        self.con.commit()

    def prepare_data(self, data):
        films = []
        if len(data):
            column_names = [desc[0] for desc in self.cur.description]
            for row in data:
                films += [{c_name: row[key] for key, c_name in enumerate(column_names)}]

        return films
