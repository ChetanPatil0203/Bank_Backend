import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Chetan@0203',
    'database': 'payzen_bank',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def verify_data():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute("SELECT count(*) as count FROM account_requests")
            requests_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT count(*) as count FROM bank_accounts")
            accounts_count = cursor.fetchone()['count']
            
            print(f"Total Requests in DB: {requests_count}")
            print(f"Total Accounts in DB: {accounts_count}")
            
            if requests_count > 0:
                cursor.execute("SELECT id, bank_holder_name, status FROM account_requests LIMIT 5")
                print("Latest Requests:", cursor.fetchall())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    verify_data()
