class QueryStrategy:
    def execute(self, cursor, value):
        pass

class QueryByDateStrategy(QueryStrategy):
    def execute(self, cursor, value):
        cursor.execute('SELECT * FROM time_records WHERE date = ?', (value,))
        return cursor.fetchall()

class QueryByTagStrategy(QueryStrategy):
    def execute(self, cursor, value):
        cursor.execute('SELECT * FROM time_records WHERE tag LIKE ?', ('%' + value + '%',))
        return cursor.fetchall()

class QueryByTaskStrategy(QueryStrategy):
    def execute(self, cursor, value):
        cursor.execute('SELECT * FROM time_records WHERE task LIKE ?', ('%' + value.strip("'") + '%',))
        return cursor.fetchall()

class QueryByDateRangeStrategy(QueryStrategy):
    def execute(self, cursor, start_date, end_date):
        cursor.execute('SELECT * FROM time_records WHERE date BETWEEN ? AND ?', (start_date, end_date))
        return cursor.fetchall()