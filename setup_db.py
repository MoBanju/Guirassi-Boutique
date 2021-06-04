import sqlite3
from sqlite3 import Error
from werkzeug.security import generate_password_hash, check_password_hash

database = r"./database.db"

### CONNECTION ###
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

##### CREATE TABLES ######## 
sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER,
                                username VARCHAR(20) NOT NULL,
                                passwordhash VARCHAR(120) NOT NULL,
                                role TEXT,
                                PRIMARY KEY (user_id),
                                UNIQUE (username)
                            );"""

sql_create_products_table = """CREATE TABLE IF NOT EXISTS products (
                                prod_id INTEGER,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                file_name TEXT,
                                description text,
                                PRIMARY KEY (prod_id)
                            );"""

sql_create_orders_table = """CREATE TABLE IF NOT EXISTS orders (
                                order_id INTEGER,
                                user_id INTEGER,
                                prod_id INTEGER,
                                quantity INTEGER,
                                size TEXT,
                                purchased BIT,
                                total REAL,
                                PRIMARY KEY(order_id),
                                FOREIGN KEY (user_id) REFERENCES users (user_id),
                                FOREIGN KEY (prod_id) REFERENCES products (prod_id)
                            );"""

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


### INSERT ###
def add_user(conn, username, hash, role="user"):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO users (username, passwordhash, role) VALUES (?,?,?)")
        cur.execute(sql, (username, hash,role))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, cur.lastrowid))
        return cur.lastrowid # Returns the last row of id
    finally:
        cur.close()

def add_product(conn, name, price, file, description):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO products (name, price, file_name, description) VALUES (?,?,?,?)")
        cur.execute(sql, (name, price, file, description))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Product {} added to the store with id {}.".format(name, cur.lastrowid))
        return cur.lastrowid # Returns the last row of id
    finally:
        cur.close()

def add_order(conn, user_id, prod_id, quantity, size, purchased=0, total=0):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO orders (user_id, prod_id, quantity, size, purchased, total) VALUES (?,?,?,?,?,?)")
        #total = ("SELECT O.quantity*P.price FROM orders AS O, products AS P WHERE O.prod_id = P.prod_id")
        #cur.execute(total)
        cur.execute(sql, (user_id, prod_id, quantity, size, purchased, total))
        conn.commit()
        
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Order {} with Product Id {} by user ID {}.".format(cur.lastrowid, prod_id, user_id))
        return cur.lastrowid # Returns the last row of id
    finally:
        cur.close()

def add_total(conn, order_id):
    cur = conn.cursor()
    try:
        total = ("UPDATE orders set total = O.quantity*P.price FROM orders AS O, products AS P WHERE O.prod = P.prod and O.order_id={}".format(order_id))
        cur.execute(total)
        conn.commit()
        
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Total Order {} is {} by user ID {}.".format(order_id, total))
        return cur.lastrowid # Returns the last row of id
    finally:
        cur.close()

def buy(conn, user_id):
    cur = conn.cursor()
    try:
        sql = ("UPDATE orders SET purchased=1 WHERE purchased=0 AND user_id={}".format(user_id))
        cur.execute(sql)
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Order was purchased successfully!!!")
    finally:
        cur.close()


def remove_product_from_order(conn, order_id):
    cur = conn.cursor()
    try:
        sql = ("DELETE FROM orders WHERE purchased=0 AND order_id={}".format(order_id))
        cur.execute(sql)
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("The product was deleted from order successfully!!!")
    finally:
        cur.close()


### INITIALIZE ###
def init_users(conn):
    init = [("johndoe", "Joe123"),
            ("maryjane", "LoveDogs"),
            ("leander", "WebDesigner456", "admin")]
    for u in init:
        if len(u) > 2 and u[2] == "admin":
            add_user(conn, u[0], generate_password_hash(u[1]), u[2])
        else:
            add_user(conn, u[0], generate_password_hash(u[1]))

def init_products(conn):
    init = [("Classic", 30, "classic.png", "From Africa"),
            ("Cac", 30, "somali.png", "From Somalia"),
            ("Mafuzzy", 30, "angola.png", "From Angola"),
            ("Barakah", 30, "guigui.png", "From Guinea-Bissau")]
    for p in init:
        add_product(conn, p[0], p[1], p[2], p[3])

def init_orders(conn):
    init = [(1, 1, 1, "M"),
            (2, 2, 2, "L"),
            (3, 4, 10, "S"),
            (3, 2, 10, "S")]
    for o in init:
        add_order(conn, o[0], o[1], o[2], o[3])

### SELECT ###

# List of Products #
def select_products(conn):
    cur = conn.cursor()
    cur.execute("SELECT prod_id, name, price, file_name, description FROM products")

    products = []
    for (prod_id, name, price, file_name, description) in cur:
        products.append({ 
            "prod_id": prod_id, 
            "name": name,
            "price": price,
            "file_name": file_name,
            "description": description
            })

    return products

### Orders  ###
def select_orders(conn):
    cur = conn.cursor()
    cur.execute("SELECT O.order_id, U.username, O.prod_id, O.quantity, O.size, O.total, P.name, P.price, O.purchased FROM orders as O, products as P, users AS U WHERE P.prod_id = O.prod_id AND O.user_id = U.user_id")

    orders = []
    for (order_id, username, prod_id, quantity, size, total, name, price, purchased) in cur:
        orders.append({
            "order_id": order_id,
            "username": username,
            "prod_id": prod_id,
            "quantity": quantity,
            "size": size,
            "name": name,
            "price": price,
            "total": total,
            "purchased": purchased
        })
    return orders

# Specific product #
def get_product_by_prod_id(conn, prod_id):
    cur = conn.cursor()
    cur.execute("SELECT prod_id, name, price, file_name, description FROM products WHERE prod_id = {}".format(prod_id))

    for row in cur:
        (prod_id, name, price, file_name, description) = row
        return{ 
            "prod_id": prod_id, 
            "name": name,
            "price": price,
            "file_name": file_name,
            "description": description
            }
    else:
        return{
            "prod_id": prod_id, 
            "name": None,
            "price": None,
            "file_name": None
        }
            
# Specific product price #
def get_price_by_prod_id(conn, prod_id):
    cur = conn.cursor()
    cur.execute("SELECT  price FROM products WHERE prod_id = {}".format(prod_id))

    for row in cur:
        (price) = row
        return{
            price,
            }
        

### Orders by specific user ###
def get_orders_by_userid(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT O.order_id, O.prod_id, O.quantity, O.size, O.total, P.name, P.price FROM orders as O, products as P WHERE O.user_id = {} AND purchased = 0 AND O.prod_id = P.prod_id".format(user_id))

    orders = []
    for row in cur:
        (order_id, prod_id, quantity, size, total, name, price) = row
        orders.append({
            "order_id": order_id,
            "prod_id": prod_id,
            "quantity": quantity,
            "size": size,
            "name": name,
            "price": price,
            "total": total
        })
    print(orders)
    return orders

### Orders by specific user ###
def get_orders_purchased_by_userid(conn, user_id):
    cur = conn.cursor()
    cur.execute("SELECT O.order_id, O.prod_id, O.quantity, O.size, O.total, P.name, P.price FROM orders as O, products as P WHERE user_id = {} AND purchased = 1 AND P.prod_id = O.prod_id".format(user_id))

    orders = []
    for (order_id, prod_id, quantity, size, total, name, price) in cur:
        orders.append({
            "order_id": order_id,
            "user_id": user_id,
            "prod_id": prod_id,
            "quantity": quantity,
            "size": size,
            "name": name,
            "price": price,
            "total": total
        })
    return orders

### Get the username 
def get_user_by_name(conn, username):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT user_id, username, role FROM users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (id,name,role) = row
            return {
                "username": name,
                "userid": id,
                "role": role
            }
        else:
            #user does not exist
            return {
                "username": username,
                "userid": None,
                "role": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


### Get the usernames
def get_usernames(conn):
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")

    usernames = []
    for (usernames) in cur:
        users.append({
            "username": username
        })
    return usernames

### Get the users
def select_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT user_id, username, role FROM users")

    users = []
    for (user_id, username, role) in cur:
        users.append({
            "user_id": user_id,
            "username": username,
            "role": role
        })
    return users

### LOGIN AND STUFF ####

### Get the hash for the login ###
def get_hash_for_login(conn, username):
    """Get user details from id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT passwordhash FROM users WHERE username=?")
        cur.execute(sql, (username,))
        for row in cur:
            (passhash,) = row
            return passhash
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()

### SETUP ###
def setup():
    conn = create_connection(database)
    if conn is not None:
        # Create tables
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_products_table)
        create_table(conn, sql_create_orders_table)

        # Initiate
        init_users(conn)
        init_products(conn)
        init_orders(conn)

        

        # Selects
        print(select_users(conn))
        print(select_products(conn))
        print("Not bought yet")
        print(get_orders_by_userid(conn, 3))
        print("bought")
        print(get_orders_purchased_by_userid(conn, 3))

        buy(conn, 3)
        print("not bought yet")
        print(get_orders_by_userid(conn, 3))
        print("Bought")
        print(get_orders_purchased_by_userid(conn, 3))

        hash = get_hash_for_login(conn, "leander")
        print("Check password: {}".format(check_password_hash(hash,"WebDesigner456")))


        print(select_orders(conn))
        conn.close()

if __name__ == "__main__":
    setup()