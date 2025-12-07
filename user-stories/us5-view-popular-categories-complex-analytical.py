from common import *

us='''
Complex Analytical US: View popular categories

   As a:  Store
 I want:  I want to view the most popular categories
So That:  I can know which categories to focus on for promotions.
'''

print(us)

def view_popular_categories(store_id):
    print("")
    before_sql1 = '''
SELECT *
  FROM Categories
'''
    before_cmd1 = cur.mogrify(before_sql1, (store_id,))
    print_cmd(before_cmd1)
    cur.execute(before_cmd1)
    before_rows1 = cur.fetchall()
    show_table(before_rows1, 'category_id category_name')

    before_sql2 = '''
SELECT *
  FROM Store_Categories
'''
    before_cmd2 = cur.mogrify(before_sql2, (store_id,))
    print_cmd(before_cmd2)
    cur.execute(before_cmd2)
    before_rows2 = cur.fetchall()
    show_table(before_rows2, 'store_id category_id')

    print("")
    view_popular_categories_sql = '''
SELECT c.category_id,
       c.category_name,
       COUNT(ci.item_id) AS items_sold,
       DENSE_RANK() OVER w AS popularity_rank
  FROM Categories AS c
       JOIN Store_Categories AS sc ON c.category_id = sc.category_id
       JOIN Item_Categories AS ic ON c.category_id = ic.category_id
       JOIN Cart_Items AS ci ON ic.item_id = ci.item_id
       JOIN Carts AS ca ON ci.cart_id = ca.cart_id
       JOIN Orders AS o ON ca.cart_id = o.cart_id
 WHERE sc.store_id = %s
   AND ca.store_id = %s
   AND o.status = 'Delivered'
 GROUP BY c.category_id, c.category_name
WINDOW w AS (ORDER BY COUNT(ci.item_id) DESC)
 ORDER BY popularity_rank
'''
    view_popular_categories_cmd = cur.mogrify(view_popular_categories_sql, (store_id, store_id,))
    print_cmd(view_popular_categories_cmd)
    cur.execute(view_popular_categories_cmd)
    view_popular_categories_rows = cur.fetchall()
    print("")
    show_table(view_popular_categories_rows, 'category_id category_name items_sold popularity_rank')

view_popular_categories(1);