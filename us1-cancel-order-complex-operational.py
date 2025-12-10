from common import *

us='''
Complex Operational US1: Cancel order

   As a:  Customer
 I want:  To cancel my order before a shopper begins shopping
So That:  I can receive a full refund if my plans change
'''

print(us)

def cancel_order(order_id):
    # Step 1: Show orders before cancel
    print("\nOrders table BEFORE cancel")
    before_cancel_sql = '''
SELECT *
  FROM Orders
'''
    before_cancel_cmd = cur.mogrify(before_cancel_sql)
    print_cmd(before_cancel_cmd)
    cur.execute(before_cancel_sql)
    before_cancel_rows = cur.fetchall()
    show_table(before_cancel_rows, 'order_id cart_id batch_id order_date status total_cost payment_method')

    # Step 2: Cancel the order
    cancel_sql = '''
UPDATE Orders
   SET status = 'Cancelled'
 WHERE order_id = %s
 RETURNING order_id, cart_id, batch_id, order_date, status, total_cost, payment_method;
'''
    cancel_cmd = cur.mogrify(cancel_sql, (order_id,))
    print_cmd(cancel_cmd)
    cur.execute(cancel_sql, (order_id,))
    cancelled = cur.fetchall()
    
    if not cancelled:
        print(f"No order found with order_id = {order_id}")
        return
    
    print("\nCancelled Order:")
    show_table(cancelled, 'order_id cart_id batch_id order_date status total_cost payment_method')

    # Step 3: Get customer_id from Carts table using the cart_id from cancelled order
    cart_id = cancelled[0][1]  # grab cart_id from cancelled order
    get_customer_sql = '''
SELECT customer_id
  FROM Carts
 WHERE cart_id = %s
'''
    get_customer_cmd = cur.mogrify(get_customer_sql, (cart_id,))
    print_cmd(get_customer_cmd)
    cur.execute(get_customer_sql, (cart_id,))
    customer_result = cur.fetchone()
    
    if not customer_result:
        print(f"No customer found for cart_id = {cart_id}")
        return
    
    customer_id = customer_result[0]

    # Step 4: Show all orders for this customer (including the new refund order created by trigger)
    show_orders_sql = '''
SELECT o.order_id, o.cart_id, o.batch_id, o.order_date, o.status, o.total_cost, o.payment_method
  FROM Orders AS o
       JOIN Carts AS c ON o.cart_id = c.cart_id
 WHERE c.customer_id = %s
 ORDER BY o.order_date;
'''
    show_orders_cmd = cur.mogrify(show_orders_sql, (customer_id,))
    print("\nAll Orders for Customer (including the new refund order created by trigger):")
    print_cmd(show_orders_cmd)
    cur.execute(show_orders_sql, (customer_id,))
    all_orders = cur.fetchall()
    show_table(all_orders, 'order_id cart_id batch_id order_date status total_cost payment_method')

    # Step 5: Show orders after cancel (shows the new refund record)
    print("\nOrders table AFTER cancel")
    after_cancel_sql = '''
SELECT *
  FROM Orders
'''
    after_cancel_cmd = cur.mogrify(after_cancel_sql)
    print_cmd(after_cancel_cmd)
    cur.execute(after_cancel_sql)
    after_cancel_rows = cur.fetchall()
    show_table(after_cancel_rows, 'order_id cart_id batch_id order_date status total_cost payment_method')

cancel_order(5)