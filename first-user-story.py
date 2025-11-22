# Example from Lab

from common import *

us='''
* Complex US: Cancel an order & issue a refund for customer

   As a:  Customer
 I want:  To cancel my order before a shopper begins shopping
So That:  I can get a refund
'''

print(us)

def cancel_order(order_id):
    # Step 1: Cancel the order
    cancel_sql = '''
UPDATE Orders
   SET status = 'cancelled'
 WHERE order_id = %s
 RETURNING order_id, cart_id, customer_id, order_date, status, total_cost;
'''
    cmd = cur.mogrify(cancel_sql, (order_id,))
    print_cmd(cmd)
    cur.execute(cancel_sql, (order_id,))
    cancelled = cur.fetchall()
    
    if not cancelled:
        print(f"No order found with order_id = {order_id}")
        return
    
    print("\nCancelled Order:")
    show_table(cancelled, 'order_id cart_id customer_id order_date status total_cost')

    # Step 2: Show all orders for this customer (including refund)
    customer_id = cancelled[0][2]  # grab customer_id from cancelled order
    show_orders_sql = '''
SELECT order_id, cart_id, customer_id, order_date, status, total_cost
  FROM Orders
 WHERE customer_id = %s
 ORDER BY order_date;
'''
    cmd2 = cur.mogrify(show_orders_sql, (customer_id,))
    print("\nAll Orders for Customer (including refunds):")
    print_cmd(cmd2)
    cur.execute(show_orders_sql, (customer_id,))
    all_orders = cur.fetchall()
    show_table(all_orders, 'order_id cart_id customer_id order_date status total_cost')


# Example usage
cancel_order(5)


# Original Version no trigger


# print(us)

# def show_cancel_order_feature( order_id):

#     cols = 'order_id order_date status total_cost customer_id cart_id'

#     tmpl =  f'''
# UPDATE Orders
#    SET status = 'cancelled'
#  WHERE order_id = %s AND
#        status = 'pending';

#  SELECT order_id, order_date, status, total_cost, customer_id, cart_id
#    FROM Orders
#   WHERE order_id = %s
# '''
#     cmd = cur.mogrify(tmpl, (order_id,order_id,))
#     print_cmd(cmd)
#     cur.execute(cmd)
#     rows = cur.fetchall()
#     pp(rows)
#     show_table( rows, cols) 

# show_cancel_order_feature( 5 )





# use trigger to cancel order:

# trigger on: update to order status
# --> if cancelled
#     adds to customer_orders the refund -total cost of prev one
#     adds to transaction/payments table w/ refund info 
# --> else nothing

# function cancel_order
#     updates order status to cancelled
#     for specified order_id

#