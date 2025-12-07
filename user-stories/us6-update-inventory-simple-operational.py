from common import *

us='''
Simple Analytical US: Update Inventory

   As a:  Store
 I want:  To update the price and inventory count for a specific item
So That:  I can ensure both customers and shoppers see accurate information for inventory.
'''

print(us)

def update_inventory(store_id, item_id, new_price, new_count):
    print("\nItem in Store_Items table BEFORE update inventory")
    before_sql1 = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
 WHERE si.store_id = %s AND si.item_id = %s
'''
    before_cmd1 = cur.mogrify(before_sql1, (store_id, item_id,))
    print_cmd(before_cmd1)
    cur.execute(before_cmd1)
    before_rows1 = cur.fetchall()

    if not before_rows1:
        print(f"No item found with store_id = {store_id} and item_id = {item_id}")
        return

    show_table(before_rows1, 'store_id item_id item_name price count')

    print("\nStore_Items table BEFORE update inventory")
    before_sql2 = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
'''
    before_cmd2 = cur.mogrify(before_sql2, ())
    print_cmd(before_cmd2)
    cur.execute(before_cmd2)
    before_rows2 = cur.fetchall()
    show_table(before_rows2, 'store_id item_id item_name price count')

    update_inventory_sql = '''
UPDATE Store_Items
   SET price = %s, count = %s
 WHERE store_id = %s AND item_id = %s
RETURNING store_id, item_id, price, count
'''
    update_inventory_cmd = cur.mogrify(update_inventory_sql, (new_price, new_count, store_id, item_id,))
    print_cmd(update_inventory_cmd)
    cur.execute(update_inventory_cmd)
    update_inventory_rows = cur.fetchall()
    print("\nUpdated item")
    show_table(update_inventory_rows, 'store_id item_id price count')

    print("\nItem in Store_Items table AFTER update inventory")
    after_sql1 = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
 WHERE si.store_id = %s AND si.item_id = %s
'''
    after_cmd1 = cur.mogrify(after_sql1, (store_id, item_id,))
    print_cmd(after_cmd1)
    cur.execute(after_cmd1)
    after_rows1 = cur.fetchall()
    show_table(after_rows1, 'store_id item_id item_name price count')

    print("\nStore_Items table AFTER update inventory")
    after_sql2 = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
'''
    after_cmd2 = cur.mogrify(after_sql2, ())
    print_cmd(after_cmd2)
    cur.execute(after_cmd2)
    after_rows2 = cur.fetchall()
    show_table(after_rows2, 'store_id item_id item_name price count')

update_inventory(1, 1, 2.49, 75)