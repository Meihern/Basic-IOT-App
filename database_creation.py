import sqlite3


def main():
    db_name = "Iot_DataBase.db"
    table_schema = """
        drop table if exists temperature_data;
        create table temperature_data(
            id integer primary key autoincrement,
            sensor_id text,
            date_time text,
            temperature decimal(6,2),
            temperature_level text 
        );
        drop table if exists humidity_data;
        create table humidity_data(
            id integer primary key autoincrement,
            sensor_id text,
            date_time text,
            humidity decimal(6,2),
            humidity_level text 
        );
        drop table if exists acceleration_data;
        create table acceleration_data(
            id integer primary key autoincrement,
            sensor_id text,
            date_time text,
            accX decimal(6,2),
            accY decimal(6,2),
            accZ decimal(6,2) 
        );
"""
    conn = sqlite3.connect(db_name)
    curs = conn.cursor()

    sqlite3.complete_statement(table_schema)
    curs.executescript(table_schema)
    conn.commit()
    curs.close()
    conn.close()


if __name__ == '__main__':
    main()

