import psycopg2


def clear_db(cur, conn):
    """Delete tables in database"""

    cur.execute("DROP TABLE phone, client;")
    conn.commit()


def create_tables(cur, conn):
    """Create tables in database"""

    cur.execute("""
        CREATE TABLE client(
        client_id serial PRIMARY KEY,
        name varchar(50) NOT NULL,
        surname varchar(50) NOT NULL,
        email varchar(100) NOT NULL
        );
        """)
    cur.execute("""
        CREATE TABLE phone(
        phone_number int PRIMARY KEY,
        client_id int REFERENCES client(client_id)
        );
        """)
    conn.commit()


def add_client(cur, conn, name, surname, email):
    """Add new client in table"""

    cur.execute("""
        INSERT INTO client(name, surname, email)
        VALUES (%s, %s, %s);
        """, (name, surname, email))
    conn.commit()


def add_phone_by_id(cur, conn, id, phone):
    """Add phone number for existing client"""

    cur.execute("""
        INSERT INTO phone(client_id, phone_number)
        VALUES (%s, %s);
        """, (id, phone))
    conn.commit()


def change_client_data_by_id(cur, conn, id, new_name, new_surname, new_email):
    """Change client info in database"""

    cur.execute("""
    	UPDATE client 
    	SET name = %s, surname = n%s, email = %s
    	WHERE client_id = %s;
    	""", (new_name, new_surname, new_email, id))
    conn.commit()


def del_phone(cur, conn, phone):
    """Delete phone number from existing client"""

    cur.execute("""
    	DELETE FROM phone
    	WHERE phone_number = %s;
    	""", (phone,))
    conn.commit()


def del_client_by_id(cur, conn, id):
    """Delete client from table"""

    cur.execute("""
    	DELETE FROM phone
    	WHERE client_id = %s;
    	""", (id,))
    conn.commit()

    cur.execute("""
    	DELETE FROM client
    	WHERE client_id = %s;
    	""", (id,))
    conn.commit()


def finde_client(cur, conn, data):
    """Finde client in database"""

    cur.execute("""
    	SELECT * FROM client
    	JOIN phone USING(client_id);
    	""", (id,))

    count = 0
    for person in cur.fetchall():
        if data in person:
            print(f'Имя:     {person[1]}\n'
                  f'Фамилия: {person[2]}\n'
                  f'email:   {person[3]}\n'
                  f'телефон: {person[4]}\n')
            count += 1
    if count == 0:
        print(f'Клиент по запросу: "{data}" не найден')
    else:
        print(f'Найдено {count} совпадений')


def main(db_access):
    """Main function"""

    with psycopg2.connect(database=db_access['database'],
                          user=db_access['user'],
                          password=db_access['password']) as conn:
        with conn.cursor() as cur:
            clear_db(cur, conn)
            create_tables(cur, conn)
            add_client(cur, conn, 'John', 'Doe', 'john.doe@mail.com')
            add_client(cur, conn, 'Вася', 'Пупкин', 'вася.пупкин@почта.рф')
            add_client(cur, conn, 'Ваня', 'Иванов', 'ваня.иванов@почта.рф')
            add_phone_by_id(cur, conn, 1, 1234567)
            add_phone_by_id(cur, conn, 2, 7654321)
            add_phone_by_id(cur, conn, 2, 1111111)
            change_client_data_by_id(cur, conn,
                                     2, 'Василий', 'Пупкин-Иванов',
                                     'вася.пупкин2@mail.ru')
            del_phone(cur, conn, 1111111)
            del_client_by_id(cur, conn, 2)
            finde_client(cur, conn, 'John')
            finde_client(cur, conn, 'Василий')

if __name__ == '__main__':

    db_access = {
        'database': 'homework5',
        'user': 'postgres',
        'password': 'Qwerty11'
    }

    main(db_access)
