import aiosqlite


class DataBase:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    async def connect(self):  # connect to database
        self.conn = await aiosqlite.connect(self.db_name)

    async def disconnect(self):  # disconnect from database
        if self.conn:
            await self.conn.close()

    async def execute_query(self, query, *args):  # Запрос базы данных
        if self.conn is None:
            await self.connect()
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, *args)
            result = await cursor.fetchall()
        await self.conn.commit()

        return result

    # ==========================================================
    # Функция проверки записей о мотивации в базе данных
    async def has_records_in_table(self, motivation):
        if self.conn is None:
            await self.connect()
        try:
            # Выполняем запрос на проверку наличия записей в таблице Motivation
            query = "SELECT * FROM Motivation WHERE motivation = ?"
            result = await self.execute_query(query, (motivation,))

            if result:
                return True  # Если есть записи, возвращаем True
            else:
                return False  # Если нет записей, возвращаем False
        except Exception:
            # Обработка ошибок, если что-то пошло не так
            return False  # Возвращаем False, чтобы не было ошибок в программе

    # ==========================================================
    # Функция заполнения базы данных
    async def add_motiv(self, motiv_text):
        if self.conn is None:
            await self.connect()

        try:
            # Проверяем, есть ли уже запись с таким текстом мотивации
            if not await self.has_records_in_table(motiv_text):
                # Если записи нет, добавляем новую запись
                await self.execute_query('''
                INSERT INTO Motivation (motivation) VALUES (?)
                ''', (motiv_text,))  # Передаем параметры как кортеж
                return f'Текст мотивации "{motiv_text}" уже существует в базе данных.'
            else:
                return f'Текст мотивации "{motiv_text}" уже существует в базе данных.'
        except Exception as e:
            return f'Ошибка при добавлении текста мотивации в базу данных: {str(e)}'

    # ==========================================================
    # Функция получения случайного текста мотивации из базы данных
    async def get_random_motivation(self):
        if self.conn is None:
            await self.connect()

        query = "SELECT motivation FROM Motivation ORDER BY RANDOM() LIMIT 1;"
        result = await self.execute_query(query)
        if result:
            motiv = result[0][0]  # Получаем текст мотивации из результата запроса
            return motiv
        else:
            return None  # Возвращаем None, если нет записей в таблице

    # =========================================================
    # Функция создания таблицы БД
    async def create_tables(self) -> None:  # Создание таблицы
        if self.conn is None:
            await self.connect()

        # Создание таблиц для SQLite

        await self.execute_query('''
            CREATE TABLE IF NOT EXISTS Motivation (
            id INTEGER PRIMARY KEY,
            motivation TEXT NULL UNIQUE
        )
        ''')


db = DataBase('sqlite.db')  # подключение БД
