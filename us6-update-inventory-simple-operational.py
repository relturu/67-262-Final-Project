from common import *

us='''
Simple Operational US6: Update Inventory

   As a:  Store
 I want:  To update the price and inventory count for a specific item
So That:  I can ensure both customers and shoppers see accurate information for inventory.
'''

print(us)

def update_inventory(store_id, item_id, new_price, new_count):
    # Step 1: Show contents of relevant tables BEFORE execution

    # Show the specific item to be updated
    print(f"\nItem in Store_Items table (store_id = {store_id}, item_id = {item_id}):")
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

    old_price = before_rows1[0][3]
    old_count = before_rows1[0][4]

    # Show all items in Store_Items table BEFORE update
    print("\nStore_Items table BEFORE updating inventory")
    before_sql2 = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
 ORDER BY si.store_id, si.item_id
'''
    before_cmd2 = cur.mogrify(before_sql2, ())
    print_cmd(before_cmd2)
    cur.execute(before_cmd2)
    before_rows2 = cur.fetchall()
    show_table(before_rows2, 'store_id item_id item_name price count')

    # Step 2: Execute SQL query that implement the user story
    print(f"\nSQL Query: Update inventory for store_id = {store_id} and item_id = {item_id}")
    print(f"New price: ${new_price} (old: ${old_price})")
    print(f"New price: {new_count} items (old: {old_count} items)")
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

    # Show updated item
    print("\nUpdated item:")
    show_table(update_inventory_rows, 'store_id item_id price count')

    # Step 3: Show contents of relevant tables AFTER execution

    # Show updated item in Store_Items table
    print("\nItem in Store_Items table AFTER updating inventory")
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

    # Show all items in Store_Items table AFTER update
    print("\nStore_Items table AFTER update inventory")
    after_sql2 = '''
SELECT si.store_id, si.item_id, i.item_name, si.price, si.count
  FROM Store_Items AS si
       JOIN Items AS i ON si.item_id = i.item_id
 ORDER BY si.store_id, si.item_id
'''
    after_cmd2 = cur.mogrify(after_sql2, ())
    print_cmd(after_cmd2)
    cur.execute(after_cmd2)
    after_rows2 = cur.fetchall()
    show_table(after_rows2, 'store_id item_id item_name price count')

update_inventory(1, 1, 2.49, 75)