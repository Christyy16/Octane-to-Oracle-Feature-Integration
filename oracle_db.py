import oracledb

from config import (
    ORACLE_USER,
    ORACLE_PASSWORD,
    ORACLE_HOST,
    ORACLE_PORT,
    ORACLE_SERVICE,
)

def get_connection():
 try:

    connection = oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        host=ORACLE_HOST,
        port=ORACLE_PORT,
        service_name=ORACLE_SERVICE
    )

    print("Oracle Connected Successfully!")

    return connection

 except Exception as e:

    print("Oracle Connection Failed")

    print(e)

    return None

if __name__ == "__main__":

    conn = get_connection()

    if conn:

        cursor = conn.cursor()

        cursor.execute("SELECT SYDATE FROM dual")

        result = cursor.fetchone()

        print("Database Time:", result[0])

        cursor.close()

        conn.close()

        print("Connection Closed")