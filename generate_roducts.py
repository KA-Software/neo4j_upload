import random
import time
import os
import glob

products = 700000
orders = 3000000
clients = 120000
stores = 23
categories = 500

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)

def create_customer():
    # Open a file
    fo = open("client_profiles", "r+")
    f= open("customers.csv","w+")
    f.write("customerID," + fo.readline())
    for i in range(1, clients):
        f.write(str(i) + "," + fo.readline())
        
    f.close() 
    fo.close()

def create_order():
    
    num_files = 1
    counter = 0
    f= open("orders1.csv","w+")
    f.write("orderID,customerID,orderDate,storeID\n")
    for i in range(1, orders):
        counter+=1
        if counter == 400000:
            f.close() 
            num_files+=1
            counter =0
            f= open("orders" + str(num_files) +".csv","w+")
            f.write("orderID,customerID,orderDate,storeID\n")

        f.write(str(i) + "," + str(random.randint(1,clients)) + "," + random_date("2019-1-1", "2019-12-31", random.random()) + "," + str(random.randint(1,stores)) + "\n")
    f.close() 

def create_categories():
    f= open("categories.csv","w+")
    f.write("categoryID,categoryName,description\n")
    for i in range(1, categories):
        f.write(str(i) + ",Category"+str(i) + ",Description\n")
    f.close() 

def create_products():
    num_files = 1
    counter = 0
    f= open("products1.csv","w+")
    f.write("productID,productName,supplierID,categoryID,unitPrice\n")
    for i in range(1, products):

        counter+=1
        if counter == 200000:
            f.close() 
            num_files+=1
            counter =0
            f= open("products" + str(num_files) +".csv","w+")
            f.write("productID,productName,supplierID,categoryID,unitPrice\n")


        f.write(str(i) + ",Product"+str(i) + "," + str(random.randint(1,29)) + "," + str(random.randint(1,categories)) + "," + str(random.randint(1,200))+ "\n")
    f.close() 

def create_order_detais():
    num_files = 1
    counter = 0
    f= open("order-details1.csv","w+")
    f.write("orderID,productID,quantity\n")
    for number in range(1, orders):

        counter+=1
        if counter == 40000:
            f.close() 
            num_files+=1
            counter =0
            f= open("order-details" + str(num_files) +".csv","w+")
            f.write("orderID,productID,quantity\n")


        for x in range(1, random.randint(2,10)):
            productList = []
            inSearch = True
            while inSearch:
                product = random.randint(1,products)
                if product not in productList: 
                    inSearch = False
                    productList.append(product)
                    f.write(str(number) + "," + str(product) + "," + str(random.randint(1,5)) + "\n")   
    f.close() 

def remove_files(name):
    files = glob.glob('./' + name + '*.csv')
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

if __name__ == "__main__":

    print("CP1")
    remove_files("customers")
    create_customer()

    print("CP2")
    remove_files("orders")
    create_order()

    print("CP3")
    remove_files("categories")
    create_categories()
    
    print("CP4")
    remove_files("products")
    create_products()
    
    print("CP5")
    remove_files("order-details")
    create_order_detais()
    
    