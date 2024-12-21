import os
import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

SQL_BASE_PATH = 'SQL/'


class User:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age


def create_table(table_name):
    sql_script_name = f'create_{table_name}.sql'
    script_path = os.path.join(SQL_BASE_PATH, sql_script_name)

    with open(script_path, 'r') as fd:
        sql_script = fd.read()
        cursor.execute(sql_script)
        conn.commit()


def add_user(user: User):
    cursor.execute(f'INSERT INTO users (username, email, age )VALUES (?, ?, ?)', (user.username, user.email, user.age))
    conn.commit()
def get_all_usernames():
    cursor.execute(f'SELECT username FROM users')
    users = cursor.fetchall()
    usernames = set([user[0] for user in users])
    for user in usernames:
        print(user)


def main():
    create_table('users')
    add_user(User(
        'Arina',
        'Arina@gmail.com',
        age=17
    ))

    add_user(User(
        'Vlad',
        'Vlad@gmail.com',
        age=20
    ))
if __name__ == '__main__':
    main()
    get_all_usernames()
    if conn:
        conn.close()
