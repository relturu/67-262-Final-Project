from common import *

us='''
Simple Analytical US: View peak earning days

   As a:  Shopper
 I want:  To view which days I get paid the most on
So That:  I can plan out my shopping schedule so that I can shop on the most profitable days.
'''

print(us)

def view_peak_earning_days(shopper_id):
    print("\nBatches table BEFORE viewing peak earning days")
    before_sql = '''
SELECT *
  FROM Batches
'''
    before_cmd = cur.mogrify(before_sql, ())
    print_cmd(before_cmd)
    cur.execute(before_cmd)
    before_rows = cur.fetchall()
    show_table(before_rows, 'batch_id shopper_id start_time end_time delivery_date shopper_earnings delivery_distance')

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
    print("\nPeak Earning Days (0 = Sunday, 6 = Saturday):")
    show_table(view_peak_earning_days_rows, 'day_of_week daily_earnings earning_rank')

view_peak_earning_days(6)