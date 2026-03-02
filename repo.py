import psycopg
from psycopg.rows import dict_row

class RepoError(Exception):
    pass

class NotFoundError(RepoError):
    pass

class UniqueViolationError(RepoError):
    pass

class UserRepository:
    FIELDS = "id, name, phone, city, created_at"

    def __init__(self, dsn):
        self.dsn = dsn

    def _get_connection(self):
        return psycopg.connect(self.dsn, row_factory=dict_row)

    def _require_row(self, row, user_id: int):
        if row is None:
            raise NotFoundError(f"user with id={user_id} not found")
        return row

    def list_users(self):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT {self.FIELDS} FROM users ORDER BY id;")
                    return  cur.fetchall()
        except psycopg.Error as e:
            raise RepoError("db error in list_users") from e

    def add_user(self, name, phone, city):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"INSERT INTO users (name, phone, city) VALUES (%s, %s, %s) RETURNING {self.FIELDS};",
                        (name, phone, city)
                    )
                    return cur.fetchone()
        except psycopg.errors.UniqueViolation as e:
            raise UniqueViolationError("phone already exists") from e
        except psycopg.Error as e:
            raise RepoError("db error in add_user") from e


    def get_user(self, user_id):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT {self.FIELDS} FROM users WHERE id = %s;",
                        (user_id,)
                    )
                    row = cur.fetchone()
                    return self._require_row(row, user_id)
        except psycopg.Error as e:
            raise RepoError("db error in get_user") from e


    def delete_user(self, user_id):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"DELETE FROM users WHERE id = %s RETURNING {self.FIELDS};",
                        (user_id,)
                    )
                    row = cur.fetchone()
                    return self._require_row(row, user_id)
        except psycopg.Error as e:
            raise RepoError("db error in delete_user") from e

    def update_user(self, user_id, name, phone, city):
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"UPDATE users SET name = %s, phone = %s, city = %s WHERE id = %s RETURNING {self.FIELDS};",
                        (name, phone, city, user_id)
                    )
                    row = cur.fetchone()
                    return self._require_row(row, user_id)
        except psycopg.errors.UniqueViolation as e:
            raise UniqueViolationError("phone already exists") from e
        except psycopg.Error as e:
            raise RepoError("db error in update_user") from e

    def search_users(self, text):
        pattern = f"%{text}%"
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(f"SELECT {self.FIELDS} FROM users WHERE name ILIKE %s OR phone ILIKE %s OR city ILIKE %s ORDER BY id;",
                        (pattern, pattern, pattern)
                    )
                    return cur.fetchall()
        except psycopg.Error as e:
            raise RepoError("db error in search_users") from e
