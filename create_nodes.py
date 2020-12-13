from neo4j import GraphDatabase



def execute_tx(tx, transaction):
    tx.run(transaction) 


def import_orders(session):
    for number in range(1,14):
        command = "LOAD CSV WITH HEADERS FROM \"file:///orders" + str(number) +".csv\" AS row \
                    CREATE (o:Order) \
                    SET o = row, \
                    o.orderID=toInteger(row.orderID), \
                    o.customerID=toInteger(row.customerID), \
                    o.storeID=toInteger(row.storeID) "

        session.write_transaction(execute_tx, command)


def import_products(session):
    for number in range(1,6):
        command = "LOAD CSV WITH HEADERS FROM \"file:///products" + str(number) +".csv\" AS row \
                    CREATE (p:Product) \
                    SET p = row, \
                    p.productID=toInteger(row.productID), \
                    p.supplierID=toInteger(row.supplierID), \
                    p.categoryID=toInteger(row.categoryID)"
                    
        session.write_transaction(execute_tx, command)

def import_order_details(session):
    for number in range(50,126):
#126
        print("CP4"+str(number))

        command = "LOAD CSV WITH HEADERS FROM \"file:///order-details" + str(number) +".csv\" AS row \
                   MATCH (p:Product), (o:Order) \
                   WHERE p.productID = toInteger(row.productID) AND o.orderID = toInteger(row.orderID) \
                   CREATE (p)-[details:BELONGS_TO]->(o) \
                   SET details = row, \
                   details.quantity = toInteger(row.quantity)"

        session.write_transaction(execute_tx, command)

def create_index(session):

    print("UPS!!!")
    session.write_transaction(execute_tx, "CREATE INDEX ON :Product(productID)")
    session.write_transaction(execute_tx, "CREATE INDEX ON :Category(categoryID)")
    session.write_transaction(execute_tx, "CREATE INDEX ON :Supplier(supplierID)")
    session.write_transaction(execute_tx, "CREATE INDEX ON :Store(StoreID)")
    session.write_transaction(execute_tx, "CREATE INDEX ON :Order(orderID)")
    session.write_transaction(execute_tx, "CREATE INDEX ON :Customer(customerID)")


def build_connections(session):

    print("CP61")
    print("UPS!!!")

    product_to_category = "MATCH (p:Product),(c:Category) \
                           WHERE p.categoryID = c.categoryID \
                           CREATE (p)-[:PART_OF]->(c)"

    #session.write_transaction(execute_tx,product_to_category)

    print("CP62")
    product_to_supplier = "MATCH (p:Product),(s:Supplier) \
                          WHERE p.supplierID = s.supplierID \
                          CREATE (s)-[:SUPPLIES]->(p)"

    #session.write_transaction(execute_tx,product_to_supplier)

    print("CP63")
    customer_to_order = "MATCH (c:Customer),(o:Order) \
                         WHERE c.customerID = o.customerID \
                         CREATE (c)-[:PURCHASED]->(o)"

    session.write_transaction(execute_tx,customer_to_order)

    print("CP64")
    order_to_store = "MATCH (o:Order), (s:Store) \
                         WHERE o.storeID = s.storeID \
                         CREATE (o)-[:BOUGHT_IN]->(s)"

    #session.write_transaction(execute_tx,order_to_store)


if __name__ == "__main__":

    uri = "neo4j://159.89.19.86:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j", "test"))
    
    stores = "LOAD CSV WITH HEADERS FROM \"file:///store.csv\" AS row CREATE (s:Store) SET s = row, s.storeID=toInteger(row.storeID)"
    suppliers = "LOAD CSV WITH HEADERS FROM \"file:///suppliers.csv\" AS row CREATE (b:Supplier) SET b = row, b.supplierID=toInteger(row.supplierID)"
    customers = "LOAD CSV WITH HEADERS FROM \"file:///customers.csv\" AS row CREATE (c:Customer) SET c = row, c.customerID=toInteger(row.customerID)"
    categories = "LOAD CSV WITH HEADERS FROM \"file:///categories.csv\" AS row CREATE (k:Category) SET k = row, k.categoryID=toInteger(row.categoryID)"

    with driver.session() as session:
        
        print("CP1")
        #Stores
        #session.write_transaction(execute_tx, stores)
        #session.write_transaction(execute_tx, suppliers)
        #session.write_transaction(execute_tx, customers)
        #session.write_transaction(execute_tx, categories)

        print("CP2")
        #Products
        #import_products(session)

        print("CP3")
        #Orders
        #import_orders(session)

        print("CP4")
        #Ordefr-Details
        #create_index(session)

    driver.close()



    with driver.session() as session:

        print("CP5")
        #Orders
        #import_order_details(session)

        print("CP6")
        #Relations
        build_connections(session)
    driver.close()
