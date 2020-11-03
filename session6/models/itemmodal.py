import sqlite3


class ItemModal:
    table_name = 'items'

    def __init__(self, _id, name, price):
        self.id = _id
        self.name = name
        self.price = price

    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.table_name)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(row[0], row[1], row[2])

    @classmethod
    def delete(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM {table} WHERE name=?".format(table=cls.table_name)
        cursor.execute(query, name)
        connection.commit()
        connection.close()

    def create(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (NULL, ?, ?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE {table} SET price=? WHERE name=?".format(table=self.table_name)
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
