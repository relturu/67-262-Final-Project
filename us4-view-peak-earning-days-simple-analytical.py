from common import *

us='''
Simple Analytical US4: View peak earning days

   As a:  Shopper
 I want:  To view which days I get paid the most on
So That:  I can plan out my shopping schedule so that I can shop on the most profitable days.
'''

print(us)

def view_peak_earning_days(shopper_id):
    # Step 1: Show contents of relevant tables BEFORE execution

    # Show all batches for the specific shopper
    print(f"\nBatches table (for shopper_id = {shopper_id}):")
    before_sql = '''
SELECT *
  FROM Batches
 WHERE shopper_id = %s
 ORDER BY delivery_date, start_time
'''
    before_cmd = cur.mogrify(before_sql, (shopper_id,))
    print_cmd(before_cmd)
    cur.execute(before_cmd)
    before_rows = cur.fetchall()
    show_table(before_rows, 'batch_id shopper_id start_time end_time delivery_date shopper_earnings delivery_distance')

    # Step 2: Execute SQL query that implement the user story
    print(f"\nSQL Query: Identify peak earning days for shopper_id = {shopper_id} (days ranked by total earnings from highest to lowest):")
    view_peak_earning_days_sql = '''
SELECT EXTRACT(DOW FROM delivery_date) AS day_of_week,
       SUM(shopper_earnings) AS daily_earnings,
       RANK() OVER w AS earning_rank
  FROM Batches
 WHERE shopper_id = %s
 GROUP BY delivery_date
WINDOW w AS (ORDER BY SUM(shopper_earnings) DESC)
ORDER BY earning_rank
'''
    view_peak_earning_days_cmd = cur.mogrify(view_peak_earning_days_sql, (shopper_id,))
    print_cmd(view_peak_earning_days_cmd)
    cur.execute(view_peak_earning_days_cmd)
    view_peak_earning_days_rows = cur.fetchall()

    # Step 3: Show contents of relevant tables AFTER execution
    print(f"\nPeak earning days for shopper {shopper_id}:")
    print("(Note: for day of week, 0 = Sunday, 1 = Monday, ..., 6 = Saturday)")
    show_table(view_peak_earning_days_rows, 'day_of_week daily_earnings earning_rank')

    if view_peak_earning_days:
        top_day = view_peak_earning_days_rows[0]
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        day_of_week = int(top_day[0])
        best_earnings = top_day[1]
        print(f"\nThe peak earning day for shopper_id {shopper_id} was {day_names[day_of_week]}, and the total earnings on that day was ${best_earnings}.")
    else:
        print(f"\nNo earning data found for shopper {shopper_id}.")

view_peak_earning_days(6)