-- Created by Redgate Data Modeler (https://datamodeler.redgate-platform.com)
-- Last modification date: 2025-12-05 02:27:40.413

-- tables
-- Table: Addresses
CREATE TABLE Addresses (
    address_id int  NOT NULL,
    street_address text  NOT NULL,
    city text  NOT NULL,
    state text  NOT NULL,
    zip_code int  NOT NULL,
    zone int  NOT NULL,
    CONSTRAINT Addresses_pk PRIMARY KEY (address_id)
);

-- Table: Batches
CREATE TABLE Batches (
    batch_id int  NOT NULL,
    shopper_id int  NOT NULL,
    start_time time  NOT NULL,
    end_time time  NOT NULL,
    delivery_date date  NOT NULL,
    shopper_earnings decimal(10,2)  NOT NULL,
    delivery_distance decimal(3,1)  NOT NULL,
    CONSTRAINT Batches_pk PRIMARY KEY (batch_id)
);

-- Table: Cart_Items
CREATE TABLE Cart_Items (
    cart_id int  NOT NULL,
    item_id int  NOT NULL,
    CONSTRAINT Cart_Items_pk PRIMARY KEY (cart_id,item_id)
);

-- Table: Carts
CREATE TABLE Carts (
    cart_id int  NOT NULL,
    store_id int  NOT NULL,
    customer_id int  NOT NULL,
    CONSTRAINT Carts_pk PRIMARY KEY (cart_id)
);

-- Table: Categories
CREATE TABLE Categories (
    category_id int  NOT NULL,
    store_id int  NOT NULL,
    category_name text  NOT NULL,
    CONSTRAINT Categories_pk PRIMARY KEY (category_id)
);

-- Table: Customers
CREATE TABLE Customers (
    customer_id int  NOT NULL,
    customer_address_id int  NOT NULL,
    preferences text  NOT NULL,
    membership text  NOT NULL,
    CONSTRAINT Customers_pk PRIMARY KEY (customer_id)
);

-- Table: Item_Categories
CREATE TABLE Item_Categories (
    item_id int  NOT NULL,
    category_id int  NOT NULL,
    CONSTRAINT Item_Categories_pk PRIMARY KEY (item_id,category_id)
);

-- Table: Items
CREATE TABLE Items (
    item_id int  NOT NULL,
    preferences text  NOT NULL,
    item_name text  NOT NULL,
    item_description text  NOT NULL,
    CONSTRAINT Items_pk PRIMARY KEY (item_id)
);

-- Table: List_Items
CREATE TABLE List_Items (
    list_id int  NOT NULL,
    item_id int  NOT NULL,
    CONSTRAINT List_Items_pk PRIMARY KEY (list_id,item_id)
);

-- Table: Lists
CREATE TABLE Lists (
    list_id int  NOT NULL,
    store_id int  NOT NULL,
    customer_id int  NOT NULL,
    CONSTRAINT Lists_pk PRIMARY KEY (list_id)
);

-- Table: Orders
CREATE TABLE Orders (
    order_id int  NOT NULL,
    cart_id int  NOT NULL,
    batch_id int  NOT NULL,
    order_date date  NOT NULL,
    status text  NOT NULL,
    total_cost decimal(10,2)  NOT NULL,
    payment_method text  NOT NULL,
    CONSTRAINT Orders_pk PRIMARY KEY (order_id)
);

-- Table: Shoppers
CREATE TABLE Shoppers (
    shopper_id int  NOT NULL,
    drivers_license int  NOT NULL,
    vehicle text  NOT NULL,
    shopper_rating decimal(2,1)  NOT NULL,
    start_date date  NOT NULL,
    CONSTRAINT Shoppers_pk PRIMARY KEY (shopper_id)
);

-- Table: Store_Categories
CREATE TABLE Store_Categories (
    store_id int  NOT NULL,
    category_id int  NOT NULL,
    CONSTRAINT Store_Categories_pk PRIMARY KEY (store_id,category_id)
);

-- Table: Store_Items
CREATE TABLE Store_Items (
    store_id int  NOT NULL,
    item_id int  NOT NULL,
    price decimal(10,2)  NOT NULL,
    item_rating decimal(2,1)  NOT NULL,
    count int  NOT NULL,
    CONSTRAINT Store_Items_pk PRIMARY KEY (store_id,item_id)
);

-- Table: Stores
CREATE TABLE Stores (
    store_id int  NOT NULL,
    store_name text  NOT NULL,
    store_address_id int  NOT NULL,
    CONSTRAINT Stores_pk PRIMARY KEY (store_id)
);

-- Table: Users
CREATE TABLE Users (
    user_id int  NOT NULL,
    first_name text  NOT NULL,
    last_name text  NOT NULL,
    email text  NOT NULL,
    phone_number varchar(10)  NOT NULL,
    registration_date date  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (user_id)
);

-- foreign keys
-- Reference: Batches_Shoppers (table: Batches)
ALTER TABLE Batches ADD CONSTRAINT Batches_Shoppers
    FOREIGN KEY (shopper_id)
    REFERENCES Shoppers (shopper_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Cart_Items_Carts (table: Cart_Items)
ALTER TABLE Cart_Items ADD CONSTRAINT Cart_Items_Carts
    FOREIGN KEY (cart_id)
    REFERENCES Carts (cart_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Cart_Items_Items (table: Cart_Items)
ALTER TABLE Cart_Items ADD CONSTRAINT Cart_Items_Items
    FOREIGN KEY (item_id)
    REFERENCES Items (item_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Carts_Customers (table: Carts)
ALTER TABLE Carts ADD CONSTRAINT Carts_Customers
    FOREIGN KEY (customer_id)
    REFERENCES Customers (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Carts_Stores (table: Carts)
ALTER TABLE Carts ADD CONSTRAINT Carts_Stores
    FOREIGN KEY (store_id)
    REFERENCES Stores (store_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Categories_Stores (table: Categories)
ALTER TABLE Categories ADD CONSTRAINT Categories_Stores
    FOREIGN KEY (store_id)
    REFERENCES Stores (store_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customers_Addresses (table: Customers)
ALTER TABLE Customers ADD CONSTRAINT Customers_Addresses
    FOREIGN KEY (customer_address_id)
    REFERENCES Addresses (address_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customers_Users (table: Customers)
ALTER TABLE Customers ADD CONSTRAINT Customers_Users
    FOREIGN KEY (customer_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Item_Categories_Categories (table: Item_Categories)
ALTER TABLE Item_Categories ADD CONSTRAINT Item_Categories_Categories
    FOREIGN KEY (category_id)
    REFERENCES Categories (category_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Item_Categories_Items (table: Item_Categories)
ALTER TABLE Item_Categories ADD CONSTRAINT Item_Categories_Items
    FOREIGN KEY (item_id)
    REFERENCES Items (item_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: List_Items_Items (table: List_Items)
ALTER TABLE List_Items ADD CONSTRAINT List_Items_Items
    FOREIGN KEY (item_id)
    REFERENCES Items (item_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: List_Items_Lists (table: List_Items)
ALTER TABLE List_Items ADD CONSTRAINT List_Items_Lists
    FOREIGN KEY (list_id)
    REFERENCES Lists (list_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Lists_Customers (table: Lists)
ALTER TABLE Lists ADD CONSTRAINT Lists_Customers
    FOREIGN KEY (customer_id)
    REFERENCES Customers (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Lists_Stores (table: Lists)
ALTER TABLE Lists ADD CONSTRAINT Lists_Stores
    FOREIGN KEY (store_id)
    REFERENCES Stores (store_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Orders_Batches (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Batches
    FOREIGN KEY (batch_id)
    REFERENCES Batches (batch_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Orders_Carts (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Carts
    FOREIGN KEY (cart_id)
    REFERENCES Carts (cart_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Shoppers_Users (table: Shoppers)
ALTER TABLE Shoppers ADD CONSTRAINT Shoppers_Users
    FOREIGN KEY (shopper_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Store_Categories_Categories (table: Store_Categories)
ALTER TABLE Store_Categories ADD CONSTRAINT Store_Categories_Categories
    FOREIGN KEY (category_id)
    REFERENCES Categories (category_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Store_Categories_Stores (table: Store_Categories)
ALTER TABLE Store_Categories ADD CONSTRAINT Store_Categories_Stores
    FOREIGN KEY (store_id)
    REFERENCES Stores (store_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Store_Items_Items (table: Store_Items)
ALTER TABLE Store_Items ADD CONSTRAINT Store_Items_Items
    FOREIGN KEY (item_id)
    REFERENCES Items (item_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Store_Items_Stores (table: Store_Items)
ALTER TABLE Store_Items ADD CONSTRAINT Store_Items_Stores
    FOREIGN KEY (store_id)
    REFERENCES Stores (store_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Stores_Addresses (table: Stores)
ALTER TABLE Stores ADD CONSTRAINT Stores_Addresses
    FOREIGN KEY (store_address_id)
    REFERENCES Addresses (address_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

