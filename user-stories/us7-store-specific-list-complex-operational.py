from common import *

us='''
Complex Operational US: Make Store Specific Lists

   As a:  Customer
 I want:  Make a list for a specific store
So That:  I can plan out my shopping trip before I go.
'''

print(us)

def make_specific_list(store_id, customer_id):
    # Step 1: Show lists before new list added
    print("\nLists BEFORE new list added")
    before_specific_list_sql = '''
SELECT *
  FROM Lists
'''
    before_specific_list_cmd = cur.mogrify(before_specific_list_sql)
    print_cmd(before_specific_list_cmd)
    cur.execute(before_specific_list_sql)
    before_specific_list_rows = cur.fetchall()
    show_table(before_specific_list_rows, 'list_id store_id customer_id')

    # Step 2: Add New List w/ hardcoded list ID
    hardcoded_list_id = 6

    make_list_sql = '''
INSERT INTO Lists (list_id, store_id, customer_id)
VALUES (%s, %s, %s);
'''
    make_list_cmd = cur.mogrify(make_list_sql, (hardcoded_list_id, store_id, customer_id))
    print_cmd(make_list_cmd)
    cur.execute(make_list_sql, (hardcoded_list_id, store_id, customer_id))
    
    print("\nNew List Created:")
    print(f"List ID: {hardcoded_list_id}, Store ID: {store_id}, Customer ID: {customer_id}")
    
    new_list_id = hardcoded_list_id 

    # Step 2.5: Show the store name, customer name, and list id
    show_list_info_sql='''
SELECT s.store_name, u.first_name || ' ' || u.last_name AS customer_name, l.list_id
  FROM Lists l
    JOIN Stores s ON l.store_id = s.store_id
    JOIN Customers c ON l.customer_id = c.customer_id
    JOIN Users u ON c.customer_id = u.user_id
  WHERE l.list_id = %s;
'''
    make_list_cmd = cur.mogrify(show_list_info_sql, (new_list_id,))
    print_cmd(make_list_cmd)
    cur.execute(show_list_info_sql, (new_list_id,))
    newlist = cur.fetchall()
    
    print("\nInfo About Your New List:")
    show_table(newlist, 'store_name customer_name list_id')


    # Step 3: View Items to List from Store (dem current items/stock/price in store)
    show_items_sql = '''
SELECT s.item_id, i.item_name, s.price, s.item_rating, s.count, i.item_description, i.preferences
  FROM Store_Items s
    JOIN Items i ON s.item_id = i.item_id
 WHERE s.store_id = %s;
'''
    show_items_cmd = cur.mogrify(show_items_sql, (store_id,))
    print_cmd(show_items_cmd)
    cur.execute(show_items_sql, (store_id,))
    newlist = cur.fetchall()
    
    print("\nAvailable Store Items to add:")
    show_table(newlist, 'item_id item_name price item_rating count item_description preferences')

#     # Step 4: Add items to that list
#     add_item_sql = '''
# INSERT INTO List_Items
# VALUES (%s, %s, %s)
# WHERE list_id = 
# '''
#     show_items_cmd = cur.mogrify(show_items_sql, (item_id1, item_id2, item_id3))
#     print_cmd(show_items_cmd)
#     cur.execute(show_items_sql, (store_id))
#     newlist = cur.fetchall()
    
#     print("\nAvailable Store Items:")
#     show_table(newlist, 'item_id item_name price item_rating count item_description preferences')

#     # Step 5: show updated list content


    # Step 6: Show all Lists for this customer (including the new list)
    show_lists_sql = '''
SELECT l.list_id, l.store_id, l.customer_id
  FROM Lists l
 WHERE l.customer_id = %s
'''
    show_lists_cmd = cur.mogrify(show_lists_sql, (customer_id,))
    print("\nAll Lists for Customer (including the new list):")
    print_cmd(show_lists_cmd)
    cur.execute(show_lists_sql, (customer_id,))
    all_lists = cur.fetchall()
    show_table(all_lists, 'list_id store_id customer_id')

    # Step 7: Show all Lists for all customers 
    print("\nLists AFTER adding new")
    after_specific_list_sql = '''
SELECT *
  FROM Lists
'''
    after_specific_list_cmd = cur.mogrify(after_specific_list_sql)
    print_cmd(after_specific_list_cmd)
    cur.execute(after_specific_list_sql)
    after_specific_list_rows = cur.fetchall()
    show_table(after_specific_list_rows, 'list_id store_id customer_id')
    
make_specific_list(1, 1)