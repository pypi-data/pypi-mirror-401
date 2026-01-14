from vesta import Server
from os.path import abspath, dirname
import sys
from psycopg import sql

PATH = dirname(abspath(__file__))


class DBInitializer(Server):
    def initUniauth(self):
        if sys.argv[1].upper() == 'Y':
            self.uniauth.initUniauth()

    def initDB(self):
        self.referenceUniauth()
        self.db.cur.execute(open(self.path + "/db/schema.sql", "r").read())
        self.db.conn.commit()

    def referenceUniauth(self):
        self.db.cur.execute("CREATE EXTENSION if not exists postgres_fdw;")

        ua_host = self.config.get('UNIAUTH', 'DB_HOST')
        ua_port = self.config.get('UNIAUTH', 'DB_PORT')
        ua_dbname = self.config.get('UNIAUTH', 'DB_NAME')
        q_server = sql.SQL("""
            CREATE SERVER IF NOT EXISTS uniauth
            FOREIGN DATA WRAPPER postgres_fdw
            OPTIONS (host {host}, port {port}, dbname {dbname});
        """).format(
            host=sql.Literal(ua_host),
            port=sql.Literal(ua_port),
            dbname=sql.Literal(ua_dbname)
        )
        self.db.cur.execute(q_server)

        q_mapping = sql.SQL("""
        CREATE USER MAPPING IF NOT EXISTS FOR CURRENT_USER SERVER uniauth
        OPTIONS (user {user}, password {password});
    """).format(
            user=sql.Literal(self.config.get('DB', 'DB_USER')),
            password=sql.Literal(self.config.get('DB', 'DB_PASSWORD'))
        )
        self.db.cur.execute(q_mapping)
        self.db.cur.execute(
            """
            CREATE FOREIGN TABLE if not exists account (id bigserial NOT NULL)
            SERVER uniauth
            OPTIONS (schema_name 'public', table_name 'account');
            """)



# initializer = DBInitializer(path=PATH[:-3], configFile="/server.ini", noStart=True)
# initializer.initUniauth()
# initializer.initDB()
# print("DB ready")
