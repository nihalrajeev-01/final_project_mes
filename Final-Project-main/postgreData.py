import psycopg2


# Insert the rows into the table
def insert_user(username, name, password):
    # Connection details
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        user="postgres",
        password="abc123",
        database="test"
    )
    # Create a cursor to execute SQL queries
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO authUsers (username, name, password)
        VALUES (%s, %s, %s);
        """,
        (username, name, password)
        )

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()




def fetch_all_users():
    # Connection details
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        user="postgres",
        password="abc123",
        database="test"
    )

    # Fetch all data from the table
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM authUsers")
    rows = cursor.fetchall()

    # Convert the rows to a list of dictionaries with updated keys
    data = []
    for row in rows:
        data.append({
            'username': row[0],
            'name': row[1],
            'password': row[2]
        })
    

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return data



def userSMS():
    conn = psycopg2.connect(
            host="localhost",
            port="5433",
            user="postgres",
            password="abc123",
            database="test"
        )

    cursor = conn.cursor()
    # Execute the SELECT query to fetch column values
    select_query = "SELECT Phone FROM People"
    cursor.execute(select_query)

    # Fetch all the values from the column
    column_values = [row[0] for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return column_values


# # Create table called 'People'
# conn = psycopg2.connect(
#         host="localhost",
#         port="5433",
#         user="postgres",
#         password="abc123",
#         database="test"
#     )
#     # Create a cursor to execute SQL queries
# cursor = conn.cursor()
# # Create the table
# cursor.execute("""
#     CREATE TABLE People (
#         Name VARCHAR,
#         Phone VARCHAR,
#         FloorNo VARCHAR
#     );
# """)
# # Commit the transaction
# conn.commit()

# # Close the cursor and connection
# cursor.close()
# conn.close()



# # Insert data into People table
# conn = psycopg2.connect(
#         host="localhost",
#         port="5433",
#         user="postgres",
#         password="abc123",
#         database="test"
#     )
# # Create a cursor to execute SQL queries
# cursor = conn.cursor()
# cursor.execute("""
#     INSERT INTO People (Name, Phone, FloorNo)
#     VALUES (%s, %s, %s);
#     """,
#     ("John", "+91342343423", "1")
#     )

# # Commit the transaction
# conn.commit()

# # Close the cursor and connection
# cursor.close()
# conn.close()