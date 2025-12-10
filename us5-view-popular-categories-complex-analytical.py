from common import *

us='''
Complex Analytical US5: View popular categories

   As a:  Store
 I want:  I want to view the most popular categories
So That:  I can know which categories to focus on for promotions.
'''

print(us)

def view_popular_categories(store_id):
    # Step 1: Show contents of relevant tables BEFORE execution

    # Show categories available at this store
    print(f"\nCategories table (categories available at store_id = {store_id}):")
    before_categories_sql = '''
SELECT sc.store_id, c.category_id, c.category_name
  FROM Categories AS c
       JOIN Store_Categories AS sc ON c.category_id = sc.category_id
 WHERE sc.store_id = %s
 ORDER BY c.category_id
'''
    before_categories_cmd = cur.mogrify(before_categories_sql, (store_id,))
    print_cmd(before_categories_cmd)
    cur.execute(before_categories_sql, (store_id,))
    before_categories_rows = cur.fetchall()
    show_table(before_categories_rows, 'store_id category_id category_name')

    # Step 2: Execute SQL query that implement the user story
    print(f"\nSQL Query: Identify most popular categories for store_id = {store_id}:")
    print("(Note: popularity is based on number of items sold (i.e. orders delivered))")
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

    # Step 3: Show contents of relevant tables AFTER execution
    print(f"\nMost popular categories for store {store_id} (ranked by items sold):")
    show_table(view_popular_categories_rows, 'category_id category_name items_sold popularity_rank')

    if view_popular_categories_rows:
        top_category = view_popular_categories_rows[0]
        category_name = top_category[1]
        items_sold = top_category[2]
        print(f"\nThe most popular category for store {store_id} is: {category_name}. The items sold in this category for store {store_id} are: {items_sold}.")
    else:
        print(f"\nNo sales data found for store {store_id}.")

view_popular_categories(1);