from common import *

us='''
Simple Analytical US: View hours worked

   As a:  Shopper
 I want:  To view the hours I have worked for the current week (Sunday to following Saturday)
So That:  I can track how many hours I have completed and manage my time.
'''

print(us)

def view_hours_worked(shopper_id):
    print("\nBatches table BEFORE viewing hours worked")
    before_sql = '''
SELECT *
  FROM Batches
'''
    before_cmd = cur.mogrify(before_sql, ())
    print_cmd(before_cmd)
    cur.execute(before_cmd)
    before_rows = cur.fetchall()
    show_table(before_rows, 'batch_id shopper_id start_time end_time delivery_date shopper_earnings delivery_distance')

    print("\nResult table displays hours worked for shopper in the week of Nov 29 - Dec 7")
    view_hours_worked_sql = '''
SELECT shopper_id,
       batch_id, 
       delivery_date, 
       start_time, 
       end_time, 
       ROUND(EXTRACT(HOUR FROM (end_time - start_time)) + EXTRACT(MINUTE FROM (end_time - start_time)) / 60.0, 2) as hours_worked
  FROM Batches
 WHERE shopper_id = %s
   AND delivery_date BETWEEN '2025-11-30' AND '2025-12-06'
'''
    view_hours_worked_cmd = cur.mogrify(view_hours_worked_sql, (shopper_id,))
    print_cmd(view_hours_worked_cmd)
    cur.execute(view_hours_worked_cmd)
    view_hours_worked_rows = cur.fetchall()
    show_table(view_hours_worked_rows, 'shopper_id batch_id delivery_date start_time end_time hours_worked')
    if view_hours_worked_rows:
        total_hours = 0
        for row in view_hours_worked_rows:
            hours = row[5]
            total_hours += hours
        print(f"\nShopper {shopper_id} worked {total_hours} hours for the week of Nov 29 - Dec 7.")
    else:
        print(f"No batches found for shopper {shopper_id} in the week of Nov 29 - Dec 7.")

view_hours_worked(6)