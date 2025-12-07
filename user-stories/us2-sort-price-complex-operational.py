from common import *

us='''
Complex Operational US: Sort price

   As a:  Customer
 I want:  To sort items from lowest list price to highest list price
So That:  I can easily find items that fit my budget.
'''

print(us)

def sort_price(store_id):
    print("\nStore_Items table BEFORE sorting by price")
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

    print("\nItems table BEFORE sorting by price")
    before_sort_items_sql = '''
SELECT *
  FROM Items
'''
    before_sort_items_cmd = cur.mogrify(before_sort_items_sql, ())
    print_cmd(before_sort_items_cmd)
    cur.execute(before_sort_items_sql, ())
    items_rows = cur.fetchall()
    show_table(items_rows, 'item_id preferences item_name item_description')

    print("\nItems for Store BEFORE sorting by price")
    before_sort_price_sql = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.item_rating, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
 WHERE si.store_id = %s
'''
    before_sort_price_cmd = cur.mogrify(before_sort_price_sql, (store_id,))
    print_cmd(before_sort_price_cmd)
    cur.execute(before_sort_price_sql, (store_id,))
    before_sort_price_rows = cur.fetchall()
    show_table(before_sort_price_rows, 'store_id item_id item_name price item_rating count') 

    print("\nItems for Store AFTER sorting by price")
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
    show_table(sort_price_rows, 'store_id item_id item_name price item_rating count')

sort_price(1)