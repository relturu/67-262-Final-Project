# Example from Lab

from common import *

us='''
* Complex US: Cancel an order & issue a refund for customer

   As a:  Customer
 I want:  To cancel my order before a shopper begins shopping
So That:  I can get a refund
'''

print(us)

def show_cancel_order_feature( order_id):

    cols = 'order_id order_date status total_cost customer_id cart_id'

    tmpl =  f'''
UPDATE Orders
   SET status = 'cancelled'
 WHERE order_id = %s AND
       status = 'pending';

 SELECT order_id, order_date, status, total_cost, customer_id, cart_id
   FROM Orders
  WHERE order_id = %s
'''
    cmd = cur.mogrify(tmpl, (order_id,order_id,))
    print_cmd(cmd)
    cur.execute(cmd)
    rows = cur.fetchall()
    pp(rows)
    show_table( rows, cols) 

show_cancel_order_feature( 5 )





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