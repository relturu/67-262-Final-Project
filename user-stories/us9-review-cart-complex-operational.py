from common import *

us='''
Complex Operational US: Review Cart Before Purchase

   As a:  Customer
 I want:  Preview/review items in cart on purchase page
So That:  I can ensure there are no mistakes in my cart before I complete my purchase.

(This is a NEW user story)
'''

print(us)

def review_cart_before_purchase(customer_id, cart_id):

    # step 1: show current cart content + items in cart 
    print("\nCurrent Cart Info")
    store_info_sql = '''
SELECT c.cart_id, s.store_name, c.customer_id, u.first_name || ' ' || u.last_name AS customer_name
  FROM Carts c
    JOIN Stores s ON c.store_id = s.store_id
    JOIN Customers cu ON c.customer_id = cu.customer_id
    JOIN Users u ON cu.customer_id = u.user_id
 WHERE cu.customer_id = %s AND
       c.cart_id = %s;
'''
    store_info_cmd = cur.mogrify(store_info_sql, (customer_id,cart_id))
    print_cmd(store_info_cmd)
    cur.execute(store_info_sql, (customer_id,cart_id))
    user_info_rows = cur.fetchall()
    show_table(user_info_rows, 'cart_id store_name customer_id customer_name')

    print("\n Preview Current Items in Cart before purchase")
    store_info_sql = '''
SELECT ci.item_id, i.item_name, si.price 
  FROM Cart_Items ci
    JOIN Items i ON ci.item_id = i.item_id
    JOIN Store_Items si ON ci.item_id = si.item_id
 WHERE cart_id = %s;
'''
    show_items_cmd = cur.mogrify(store_info_sql, (cart_id,))
    print_cmd(show_items_cmd)
    cur.execute(store_info_sql, (cart_id,))
    newlist = cur.fetchall()
    
    print("\nCurrent Items added to your cart:")
    show_table(newlist, 'item_id item_name price')


    #step 2: Place order from cart by showing order history 
    print("\n Cart now Moved into Orders & has been Delivered after customer has made purchase ")
    store_info_sql = '''
    SELECT order_id, cart_id, order_date, status
    FROM Orders
    WHERE cart_id = %s;
    '''
    show_items_cmd = cur.mogrify(store_info_sql, (cart_id,))
    print_cmd(show_items_cmd)
    cur.execute(store_info_sql, (cart_id,))
    newlist = cur.fetchall()
    
    print("\nCurrent Items added to your cart:")
    show_table(newlist, 'order_id cart_id order_date status')

    
review_cart_before_purchase(1, 1)