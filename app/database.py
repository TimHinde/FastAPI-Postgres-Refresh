import asyncpg


class Database:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    async def create_table(self):
        """
        Create a table
        """
        query = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                age INTEGER NOT NULL,
                email VARCHAR(254) NOT NULL UNIQUE
            )
        """
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    await conn.execute(query)
            except asyncpg.PostgresError as e:
                print(f"Error executing query: {e}")
            finally:
                await self.disconnect(conn)

    async def check_table(self):
        """
        Check if a table exists
        """
        query = "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'users')"
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    await conn.fetch(query)
            except asyncpg.PostgresError as e:
                print(f"Error executing query: {e}")
            finally:
                await self.disconnect(conn)
    
    async def connect(self):
        """
        Connect to PostgreSQL database
        """
        try:
            conn = await asyncpg.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            return conn
        except asyncpg.PostgresError as e:
            print(f"Error connecting to PostgreSQL: {e}")

    async def disconnect(self, conn):
        """
        Disconnect from PostgreSQL database
        """
        if conn is not None:
            await conn.close()

    async def execute_query(self, query):
        """
        Execute a query - A general function to execute queries
        :param query: Query to be executed
        """
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    await conn.execute(query)
            except asyncpg.PostgresError as e:
                print(f"Error executing query: {e}")
            finally:
                await self.disconnect(conn)

    async def insert_user(self, name, age, email):
        """
        Insert a user into the database
        :param name: Name of the user
        :param age: Age of the user
        :param email: Email of the user
        """
        user_name = name
        user_age = age
        user_email = email
        query = f" INSERT INTO users (name, age, email) VALUES ('{user_name}', {user_age}, '{user_email}') "
        
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    await conn.execute(query)
            except asyncpg.PostgresError as e:
                print(f"Insterting User: Error executing query: {e}")
            finally:
                await self.disconnect(conn)

    async def get_all_users(self): # add pagination when needed.
        """
        Get all users
        """
        query = "SELECT * FROM users"
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    data = await conn.fetch(query)
                    return data
            except asyncpg.PostgresError as e:
                print(f"Error executing query: {e}")
            finally:
                await self.disconnect(conn)

    async def get_user_with_id(self, id):
        """
        Get a user with a specific id
        :param id: Id of the user
        """
        query = f" SELECT * FROM users WHERE id = {id} "
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    data = await conn.fetch(query)
                    if data:
                        return data
            except asyncpg.PostgresError as e:
                print(f"Getting user with id: Error executing query: {e}")
            finally:
                await self.disconnect(conn)

    async def get_user_with_email(self, email):
        """
        Get a user with a specific email
        :param email: Email of the user
        """
        query = f" SELECT * FROM users WHERE email = '{email}' "
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    data = await conn.fetch(query)
                    if data:
                        return data
            except asyncpg.PostgresError as e:
                print(f"Getting user with email: Error executing query: {e}")
            finally:
                await self.disconnect(conn)

    async def update_user(self, id, name, age, email):
        """
        Update a user
        :param name: Name of the user
        :param age: Age of the user
        :param email: Email of the user
        """
        query = f" UPDATE users SET name = '{name}', age = '{age}', email = '{email}' WHERE id = {id} "
        conn = await self.connect()
        if conn is not None:
            try:
                async with conn.transaction():
                    await conn.execute(query)
            except asyncpg.PostgresError as e:
                print(f"Error executing query: {e}")
            finally:
                await self.disconnect(conn)
