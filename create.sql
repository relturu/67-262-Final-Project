-- Created by Redgate Data Modeler (https://datamodeler.redgate-platform.com)
-- Last modification date: 2025-11-22 01:31:31.784

-- tables
-- Table: Cart
CREATE TABLE Cart (
    cart_id int  NOT NULL,
    store_id int  NOT NULL,
    customer_id int  NOT NULL,
    CONSTRAINT Cart_pk PRIMARY KEY (cart_id)
);

-- Table: Customer
CREATE TABLE Customer (
    customer_id int  NOT NULL,
    customer_address text  NOT NULL,
    preferences text  NOT NULL,
    membership text  NOT NULL,
    CONSTRAINT Customer_pk PRIMARY KEY (customer_id)
);

-- Table: Orders
CREATE TABLE Orders (
    order_id int  NOT NULL,
    order_date date  NOT NULL,
    status text  NOT NULL,
    total_cost decimal(10,2)  NOT NULL,
    customer_id int  NOT NULL,
    cart_id int  NOT NULL,
    CONSTRAINT Orders_pk PRIMARY KEY (order_id)
);

-- Table: Payment
CREATE TABLE Payment (
    payment_id int  NOT NULL,
    payment_amount decimal(10,2)  NOT NULL,
    payment_method text  NOT NULL,
    order_id int  NOT NULL,
    CONSTRAINT Payment_pk PRIMARY KEY (payment_id)
);

-- Table: Store
CREATE TABLE Store (
    store_id int  NOT NULL,
    store_name text  NOT NULL,
    store_address text  NOT NULL,
    zone_id int  NOT NULL,
    CONSTRAINT Store_pk PRIMARY KEY (store_id)
);

-- Table: Users
CREATE TABLE Users (
    user_id int  NOT NULL,
    f_name text  NOT NULL,
    l_name text  NOT NULL,
    email text  NOT NULL,
    phone_number varchar(10)  NOT NULL,
    registration_date date  NOT NULL,
    CONSTRAINT Users_pk PRIMARY KEY (user_id)
);

-- Table: ZipCodeZones
CREATE TABLE ZipCodeZones (
    zone_id int  NOT NULL,
    zip_code int  NOT NULL,
    CONSTRAINT ZipCodeZones_pk PRIMARY KEY (zone_id)
);

-- foreign keys
-- Reference: Cart_Customer (table: Cart)
ALTER TABLE Cart ADD CONSTRAINT Cart_Customer
    FOREIGN KEY (customer_id)
    REFERENCES Customer (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Cart_Store (table: Cart)
ALTER TABLE Cart ADD CONSTRAINT Cart_Store
    FOREIGN KEY (store_id)
    REFERENCES Store (store_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Customer_Users (table: Customer)
ALTER TABLE Customer ADD CONSTRAINT Customer_Users
    FOREIGN KEY (customer_id)
    REFERENCES Users (user_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Orders_Cart (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Cart
    FOREIGN KEY (cart_id)
    REFERENCES Cart (cart_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Orders_Customer (table: Orders)
ALTER TABLE Orders ADD CONSTRAINT Orders_Customer
    FOREIGN KEY (customer_id)
    REFERENCES Customer (customer_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Store_ZipCodeZones (table: Store)
ALTER TABLE Store ADD CONSTRAINT Store_ZipCodeZones
    FOREIGN KEY (zone_id)
    REFERENCES ZipCodeZones (zone_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- Reference: Transaction_Orders (table: Payment)
ALTER TABLE Payment ADD CONSTRAINT Transaction_Orders
    FOREIGN KEY (order_id)
    REFERENCES Orders (order_id)  
    NOT DEFERRABLE 
    INITIALLY IMMEDIATE
;

-- End of file.

