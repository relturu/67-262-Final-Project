from common import *

us='''
Complex Operational US: Filter by Dietary Preferences

   As a:  Customer
 I want:  Filter my recommended items by preferences
So That:  I can avoid foods I don’t eat, and more easily find foods I want to eat.
'''

print(us)

def filter_diet_preference(customer_id):

    # Step 2: Show store options for customer to choose from
    print("\nCurrent Store Options")
    store_info_sql = '''
SELECT store_id, store_name
  FROM Stores
'''
    store_info_cmd = cur.mogrify(store_info_sql)
    print_cmd(store_info_cmd)
    cur.execute(store_info_sql)
    user_info_rows = cur.fetchall()
    show_table(user_info_rows, 'store_id store_name')

    # Step 2.5: Show the selected store
    print("\nChosen Store")
    store_info_sql = '''
SELECT store_id, store_name
  FROM Stores
 WHERE store_id = 1;
'''
    store_info_cmd = cur.mogrify(store_info_sql)
    print_cmd(store_info_cmd)
    cur.execute(store_info_sql)
    user_info_rows = cur.fetchall()
    show_table(user_info_rows, 'store_id store_name')

    # Step 3: Show items available in the store along w/ the preference and items info for each

    show_items_sql = '''
SELECT s.item_id, i.item_name, s.price, s.item_rating, s.count, i.item_description, i.preferences
  FROM Store_Items s
    JOIN Items i ON s.item_id = i.item_id
    JOIN customers c ON i.preferences = c.preferences
 WHERE customer_id = %s;
'''
    show_items_cmd = cur.mogrify(show_items_sql, (customer_id,))
    print_cmd(show_items_cmd)
    cur.execute(show_items_sql, (customer_id,))
    newlist = cur.fetchall()
    
    print("\nAvailable Store Items to add given preference:")
    show_table(newlist, 'item_id item_name price item_rating count item_description preferences')

    # Step 3.999: Show Users current dietary preferences 
    print("\nUser Current Preferences BEFORE")
    user_info_sql = '''
SELECT u.first_name || ' ' || u.last_name AS customer_name, c.preferences
  FROM Customers c
    JOIN Users u ON c.customer_id = u.user_id
 WHERE c.customer_id = %s;
'''
    user_info_cmd = cur.mogrify(user_info_sql, (customer_id,))
    print_cmd(user_info_cmd)
    cur.execute(user_info_sql, (customer_id,))
    user_info_rows = cur.fetchall()
    show_table(user_info_rows, 'customer_name preferences')

    # Step 4: Update user preferneces showing before and after
    print("\nChanging Preferences to Vegetarian")
    store_info_sql = '''
UPDATE Customers
   SET preferences = 'Vegetarian'
 WHERE customer_id = %s;
'''
    store_info_cmd = cur.mogrify(store_info_sql, (customer_id,))
    print_cmd(store_info_cmd)
    cur.execute(store_info_sql, (customer_id,))  
    print("Preferences updated!")

    #  Step 4.111: Show Users current dietary preferences 
    print("\nUser Current Preferences AFTER")
    user_info_sql = '''
SELECT u.first_name || ' ' || u.last_name AS customer_name, c.preferences
  FROM Customers c
    JOIN Users u ON c.customer_id = u.user_id
 WHERE c.customer_id = %s;
'''
    user_info_cmd = cur.mogrify(user_info_sql, (customer_id,))
    print_cmd(user_info_cmd)
    cur.execute(user_info_sql, (customer_id,))
    user_info_rows = cur.fetchall()
    show_table(user_info_rows, 'customer_name preferences')


    # Step 5: show selected store + items available that changed now w/ preferneces
    show_items_sql = '''
SELECT s.item_id, i.item_name, s.price, s.item_rating, s.count, i.item_description, i.preferences
  FROM Store_Items s
    JOIN Items i ON s.item_id = i.item_id
    JOIN Customers c ON i.preferences = c.preferences
 WHERE customer_id = %s AND
       s.store_id = 1;
'''
    show_items_cmd = cur.mogrify(show_items_sql, (customer_id,))
    print_cmd(show_items_cmd)
    cur.execute(show_items_sql, (customer_id,))
    newlist = cur.fetchall()
    
    print("\nAvailable Store Items to add given NEW preference:")
    show_table(newlist, 'item_id item_name price item_rating count item_description preferences')


    
filter_diet_preference(2)