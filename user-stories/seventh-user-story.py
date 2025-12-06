# from common import *

# us='''
# * Complex Operational US: Make Store Specific Grocery List

#    As a:  Customer
#  I want:  Make a list for a specific store
# So That:  I can plan out my shopping trip before I go.
# '''

# print(us)

# def store_specific_list(order_id):
#     # Step 0: Show orders before cancel
#     print("\nOrders BEFORE cancel")
#     before_cancel_sql = '''
# SELECT *
#   FROM Orders
# '''
#     cmd = cur.mogrify(before_cancel_sql)
#     print_cmd(cmd)
#     cur.execute(before_cancel_sql)
#     before_cancel_rows = cur.fetchall()
#     show_table(before_cancel_rows, 'order_id, order_date, status, total_cost, customer_id, cart_id')

#     # Step 1: Cancel the order
#     cancel_sql = '''
# UPDATE Orders
#    SET status = 'cancelled'
#  WHERE order_id = %s
#  RETURNING order_id, cart_id, customer_id, order_date, status, total_cost;
# '''
#     cmd1 = cur.mogrify(cancel_sql, (order_id,))
#     print_cmd(cmd1)
#     cur.execute(cancel_sql, (order_id,))
#     cancelled = cur.fetchall()
    
#     if not cancelled:
#         print(f"No order found with order_id = {order_id}")
#         return
    
#     print("\nCancelled Order:")
#     show_table(cancelled, 'order_id cart_id customer_id order_date status total_cost')

#     # Step 2: Show all orders for this customer (including refund)
#     customer_id = cancelled[0][2]  # grab customer_id from cancelled order
#     show_orders_sql = '''
# SELECT order_id, cart_id, customer_id, order_date, status, total_cost
#   FROM Orders
#  WHERE customer_id = %s
#  ORDER BY order_date;
# '''
#     cmd2 = cur.mogrify(show_orders_sql, (customer_id,))
#     print("\nAll Orders for Customer (including refunds):")
#     print_cmd(cmd2)
#     cur.execute(show_orders_sql, (customer_id,))
#     all_orders = cur.fetchall()
#     show_table(all_orders, 'order_id cart_id customer_id order_date status total_cost')

#     # Step 3: Show orders after cancel
#     print("\nOrders AFTER cancel")
#     after_cancel_sql = '''
# SELECT *
#   FROM Orders
# '''
#     cmd3 = cur.mogrify(after_cancel_sql)
#     print_cmd(cmd3)
#     cur.execute(after_cancel_sql)
#     after_cancel_rows = cur.fetchall()
#     show_table(after_cancel_rows, 'order_id, order_date, status, total_cost, customer_id, cart_id')

# cancel_order(5)