from common import *

us='''
Complex Operational US: Make Multi-Store Grocery List

   As a:  Customer
 I want:  Make a list with items from multiple stores
So That:  I can make a more holistic shopping list.

(This is a NEW user story)
'''

print(us)

def make_multi_store_grocery_list(customer_id):

    # Step 1: Show multi-store lists before new list added
    print("\nMulti-Store Lists BEFORE new list added")
    before_specific_list_sql = '''
SELECT *
  FROM MultiStoreLists
'''
    before_specific_list_cmd = cur.mogrify(before_specific_list_sql)
    print_cmd(before_specific_list_cmd)
    cur.execute(before_specific_list_sql)
    before_specific_list_rows = cur.fetchall()
    show_table(before_specific_list_rows, 'multilist_id customer_id')

    # Step 2: Add New Multi-Store List w/ hardcoded list ID
    hardcoded_multilist_id = 8

    make_list_sql = '''
INSERT INTO MultiStoreLists (multilist_id, customer_id)
VALUES (%s, %s);
'''
    make_list_cmd = cur.mogrify(make_list_sql, (hardcoded_multilist_id, customer_id))
    print_cmd(make_list_cmd)
    cur.execute(make_list_sql, (hardcoded_multilist_id, customer_id))
    
    print("\nNew Multi-Store List Created:")
    print(f"Multi-List ID: {hardcoded_multilist_id}, Customer ID: {customer_id}")
    
    new_multilist_id = hardcoded_multilist_id 

    # Step 2.5: Show the customer name and multilist id
    show_list_info_sql='''
SELECT u.first_name || ' ' || u.last_name AS customer_name, m.multilist_id
  FROM MultiStoreLists m
    JOIN Customers c ON m.customer_id = c.customer_id
    JOIN Users u ON c.customer_id = u.user_id
  WHERE m.multilist_id = %s;
'''
    make_list_cmd = cur.mogrify(show_list_info_sql, (new_multilist_id,))
    print_cmd(make_list_cmd)
    cur.execute(show_list_info_sql, (new_multilist_id,))
    newlist = cur.fetchall()
    
    print("\nInfo About Your New Multi-Store List:")
    show_table(newlist, 'customer_name multilist_id')


    # Step 3: View Items from Store 1
    store_id_1 = 1
    show_items_sql = '''
SELECT s.item_id, i.item_name, s.price, s.item_rating, s.count, i.item_description, i.preferences, st.store_name
  FROM Store_Items s
    JOIN Items i ON s.item_id = i.item_id
    JOIN Stores st ON s.store_id = st.store_id
 WHERE s.store_id = %s;
'''
    show_items_cmd = cur.mogrify(show_items_sql, (store_id_1,))
    print_cmd(show_items_cmd)
    cur.execute(show_items_sql, (store_id_1,))
    items_store_1 = cur.fetchall()
    
    print(f"\nAvailable Items from Store {store_id_1}:")
    show_table(items_store_1, 'item_id item_name price item_rating count item_description preferences store_name')

    # Step 3.5: View Items from Store 2
    store_id_2 = 2
    show_items_cmd = cur.mogrify(show_items_sql, (store_id_2,))
    print_cmd(show_items_cmd)
    cur.execute(show_items_sql, (store_id_2,))
    items_store_2 = cur.fetchall()
    
    print(f"\nAvailable Items from Store {store_id_2}:")
    show_table(items_store_2, 'item_id item_name price item_rating count item_description preferences store_name')

    # Step 4: Add items from multiple stores to the multi-store list
    print("\nAdding items from multiple stores to list...")
    
    # Add items from Store 1
    add_item_sql = '''
INSERT INTO Multi_List_Items (multilist_id, item_id)
VALUES (%s, %s);
'''
    items_to_add_store_1 = [1, 3, 4]  # item IDs from store 1
    for item_id in items_to_add_store_1:
        cur.execute(add_item_sql, (new_multilist_id, item_id))
        print(f"Added item {item_id} from Store 1")
    
    # Add items from Store 2
    items_to_add_store_2 = [2]  # Example item IDs from store 2
    for item_id in items_to_add_store_2:
        cur.execute(add_item_sql, (new_multilist_id, item_id))
        print(f"Added item {item_id} from Store 2")

    # Step 5: Show updated list content with items from multiple stores (using cheapest price only)
    show_multilist_contents_sql = '''
SELECT DISTINCT ON (mi.item_id) 
       mi.multilist_id, 
       i.item_id, 
       i.item_name, 
       si.price, 
       st.store_name
  FROM Multi_List_Items mi
    JOIN Items i ON mi.item_id = i.item_id
    JOIN Store_Items si ON i.item_id = si.item_id
    JOIN Stores st ON si.store_id = st.store_id
 WHERE mi.multilist_id = %s
 ORDER BY mi.item_id, si.price ASC;
'''
    cur.execute(show_multilist_contents_sql, (new_multilist_id,))
    multilist_contents = cur.fetchall()
    
    print(f"\nContents of Multi-Store List {new_multilist_id}:")
    show_table(multilist_contents, 'multilist_id item_id item_name price store_name')

    # Step 6: Show all Multi-Store Lists for this customer
    show_lists_sql = '''
SELECT m.multilist_id, m.customer_id
  FROM MultiStoreLists m
 WHERE m.customer_id = %s
'''
    show_lists_cmd = cur.mogrify(show_lists_sql, (customer_id,))
    print("\nAll Multi-Store Lists for Customer (including the new list):")
    print_cmd(show_lists_cmd)
    cur.execute(show_lists_sql, (customer_id,))
    all_lists = cur.fetchall()
    show_table(all_lists, 'multilist_id customer_id')

    # Step 7: Show all Multi-Store Lists for all customers 
    print("\nMulti-Store Lists AFTER adding new")
    after_specific_list_sql = '''
SELECT *
  FROM MultiStoreLists
'''
    after_specific_list_cmd = cur.mogrify(after_specific_list_sql)
    print_cmd(after_specific_list_cmd)
    cur.execute(after_specific_list_sql)
    after_specific_list_rows = cur.fetchall()
    show_table(after_specific_list_rows, 'multilist_id customer_id')
    
make_multi_store_grocery_list(1)