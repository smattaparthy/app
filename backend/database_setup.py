import sqlite3
import os

DATABASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(DATABASE_DIR, 'adventureworks.db')

def create_database():
    # Remove existing database file if it exists
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print("Removed existing database.")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create Product table
    cursor.execute('''
    CREATE TABLE Product (
        ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        ProductNumber TEXT NOT NULL UNIQUE,
        Color TEXT,
        StandardCost REAL NOT NULL,
        ListPrice REAL NOT NULL,
        Size TEXT,
        Weight REAL,
        ProductCategoryID INTEGER,
        ProductModelID INTEGER,
        SellStartDate TEXT NOT NULL,
        SellEndDate TEXT,
        DiscontinuedDate TEXT
    )
    ''')
    print("Created Product table.")

    # Create Customer table
    cursor.execute('''
    CREATE TABLE Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        EmailAddress TEXT UNIQUE,
        Phone TEXT
    )
    ''')
    print("Created Customer table.")

    # Create SalesOrderHeader table
    cursor.execute('''
    CREATE TABLE SalesOrderHeader (
        SalesOrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderDate TEXT NOT NULL,
        DueDate TEXT NOT NULL,
        ShipDate TEXT,
        Status INTEGER NOT NULL CHECK (Status IN (1, 2, 3, 4, 5)), -- 1=In process, 2=Approved, 3=Backordered, 4=Rejected, 5=Shipped
        OnlineOrderFlag INTEGER NOT NULL DEFAULT 1,
        SalesOrderNumber TEXT NOT NULL UNIQUE,
        CustomerID INTEGER,
        SubTotal REAL NOT NULL,
        TaxAmt REAL NOT NULL,
        Freight REAL NOT NULL,
        TotalDue REAL NOT NULL,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
    )
    ''')
    print("Created SalesOrderHeader table.")

    # Create SalesOrderDetail table
    cursor.execute('''
    CREATE TABLE SalesOrderDetail (
        SalesOrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
        SalesOrderID INTEGER NOT NULL,
        OrderQty INTEGER NOT NULL,
        ProductID INTEGER NOT NULL,
        UnitPrice REAL NOT NULL,
        UnitPriceDiscount REAL NOT NULL DEFAULT 0,
        LineTotal REAL NOT NULL, -- Calculated as (OrderQty * UnitPrice * (1 - UnitPriceDiscount))
        FOREIGN KEY (SalesOrderID) REFERENCES SalesOrderHeader(SalesOrderID),
        FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
    )
    ''')
    print("Created SalesOrderDetail table.")

    # Populate Product table
    products_data = [
        ('HL Road Frame - Black, 58', 'FR-R92B-58', 'Black', 1059.31, 1431.50, '58', 1016.04, 18, 6, '2001-07-01', None, None),
        ('HL Mountain Frame - Silver, 42', 'FR-M94S-42', 'Silver', 608.09, 1364.50, '42', 1242.84, 25, 10, '2002-07-01', None, None),
        ('Sport-100 Helmet, Red', 'HL-U509-R', 'Red', 13.08, 34.99, None, None, 35, 27, '2001-07-01', None, None),
        ('AWC Logo Cap', 'CA-1098', None, 6.9223, 8.6442, None, None, 17, 31, '2001-07-01', None, None),
        ('Long-Sleeve Logo Jersey, L', 'LJ-0192-L', None, 38.4923, 49.99, 'L', None, 20, 3, '2001-07-01', None, None)
    ]
    cursor.executemany('''
    INSERT INTO Product (Name, ProductNumber, Color, StandardCost, ListPrice, Size, Weight, ProductCategoryID, ProductModelID, SellStartDate, SellEndDate, DiscontinuedDate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', products_data)
    print(f"Inserted {len(products_data)} products.")

    # Populate Customer table
    customers_data = [
        ('Orlando', 'Gee', 'orlando0@adventure-works.com', '245-555-0173'),
        ('Keith', 'Harris', 'keith0@adventure-works.com', '170-555-0127'),
        ('Donna', 'Carreras', 'donna0@adventure-works.com', '279-555-0130'),
        ('Janet', 'Gates', 'janet1@adventure-works.com', '710-555-0173')
    ]
    cursor.executemany('''
    INSERT INTO Customer (FirstName, LastName, EmailAddress, Phone)
    VALUES (?, ?, ?, ?)
    ''', customers_data)
    print(f"Inserted {len(customers_data)} customers.")

    # Populate SalesOrderHeader table
    # For simplicity, let's assume CustomerID 1 and 2 exist from the inserts above
    sales_orders_data = [
        ('2001-07-01 00:00:00', '2001-07-13 00:00:00', '2001-07-08 00:00:00', 5, 1, 'SO43659', 1, 20565.6206, 1971.5149, 616.0984, 23153.2339),
        ('2001-08-01 00:00:00', '2001-08-13 00:00:00', '2001-08-08 00:00:00', 5, 1, 'SO43660', 2, 1294.2529, 124.2483, 38.8276, 1457.3288)
    ]
    cursor.executemany('''
    INSERT INTO SalesOrderHeader (OrderDate, DueDate, ShipDate, Status, OnlineOrderFlag, SalesOrderNumber, CustomerID, SubTotal, TaxAmt, Freight, TotalDue)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', sales_orders_data)
    print(f"Inserted {len(sales_orders_data)} sales orders.")

    # Get SalesOrderIDs for linking SalesOrderDetail
    so_ids = [row[0] for row in cursor.execute("SELECT SalesOrderID FROM SalesOrderHeader").fetchall()]

    # Populate SalesOrderDetail table
    # Assume ProductID 1, 2, 3, 4, 5 exist from inserts above
    # Order 1 (SO43659)
    sales_order_details_data = [
        (so_ids[0], 1, 1, 1431.50, 0, 1431.50), # ProductID 1: HL Road Frame
        (so_ids[0], 2, 3, 34.99, 0, 69.98),   # ProductID 3: Sport-100 Helmet
    ]
    # Order 2 (SO43660)
    sales_order_details_data.extend([
        (so_ids[1], 1, 2, 1364.50, 0, 1364.50), # ProductID 2: HL Mountain Frame
        (so_ids[1], 3, 4, 8.6442, 0, 25.9326), # ProductID 4: AWC Logo Cap
        (so_ids[1], 1, 5, 49.99, 0, 49.99)    # ProductID 5: Long-Sleeve Logo Jersey
    ])

    cursor.executemany('''
    INSERT INTO SalesOrderDetail (SalesOrderID, OrderQty, ProductID, UnitPrice, UnitPriceDiscount, LineTotal)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', sales_order_details_data)
    print(f"Inserted {len(sales_order_details_data)} sales order details.")

    conn.commit()
    conn.close()
    print(f"Database created and populated at {DATABASE_PATH}")

if __name__ == '__main__':
    create_database()
