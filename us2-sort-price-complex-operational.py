from common import *

us='''
Complex Operational US2: Sort price

   As a:  Customer
 I want:  To sort items from lowest list price to highest list price
So That:  I can easily find items that fit my budget.
'''

print(us)

def sort_price(store_id):
    # Step 1: Show contents of relevants table BEFORE execution

    # Show Store_Items table filtered by store_id
    print("\nStore_Items table (for store_id = %s):" % store_id)
    before_sort_store_items_sql = '''
SELECT *
  FROM Store_Items
 WHERE store_id = %s
'''
    before_sort_store_items_cmd = cur.mogrify(before_sort_store_items_sql, (store_id,))
    print_cmd(before_sort_store_items_cmd)
    cur.execute(before_sort_store_items_sql, (store_id,))
    store_items_rows = cur.fetchall()
    show_table(store_items_rows, 'store_id item_id price item_rating count')

    # Show Items table (only items available at this store)
    print("\nItems table (items available at store_id = %s):" % store_id)
    before_sort_items_sql = '''
SELECT i.item_id, i.preferences, i.item_name, i.item_description
  FROM Items AS i
       JOIN Store_Items AS si ON i.item_id = si.item_id
 WHERE si.store_id = %s
'''
    before_sort_items_cmd = cur.mogrify(before_sort_items_sql, (store_id,))
    print_cmd(before_sort_items_cmd)
    cur.execute(before_sort_items_cmd)
    items_rows = cur.fetchall()
    show_table(items_rows, 'item_id preferences item_name item_description')

    # Step 2: Execute SQL query that implement the user story
    print("\nSQL Query: sort items by price (lowest to highest) for store_id = %s:" % store_id)
    sort_price_sql = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.item_rating, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
 WHERE si.store_id = %s
 ORDER BY si.price ASC
'''
    sort_price_cmd = cur.mogrify(sort_price_sql, (store_id,))
    print_cmd(sort_price_cmd)
    cur.execute(sort_price_sql, (store_id,))
    sort_price_rows = cur.fetchall()

    # Step 3: Show contents of relevant tables AFTER execution
    print("\nItems sorted by price (lowest to highest) for store_id = %s:" % store_id)
    show_table(sort_price_rows, 'store_id item_id item_name price item_rating count')

sort_price(1)