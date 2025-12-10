from common import *

us='''
Simple Analytical US3: View hours worked

   As a:  Shopper
 I want:  To view the hours I have worked for the current week (Sunday to following Saturday)
So That:  I can track how many hours I have completed and manage my time.
'''

print(us)

def view_hours_worked(shopper_id, week_start, week_end):
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

    # Step 2: Execute SQL query that implement that implement the user story
    print(f"SQL Query: Calculate hours worked for shopper_id = {shopper_id} from {week_start} to {week_end} (Sunday to Saturday):")
    view_hours_worked_sql = '''
SELECT shopper_id,
       batch_id, 
       delivery_date, 
       start_time, 
       end_time, 
       ROUND(EXTRACT(HOUR FROM (end_time - start_time)) + EXTRACT(MINUTE FROM (end_time - start_time)) / 60.0, 2) as hours_worked
  FROM Batches
 WHERE shopper_id = %s
   AND delivery_date BETWEEN %s AND %s
 ORDER BY delivery_date, start_time
'''
    view_hours_worked_cmd = cur.mogrify(view_hours_worked_sql, (shopper_id, week_start, week_end,))
    print_cmd(view_hours_worked_cmd)
    cur.execute(view_hours_worked_cmd)
    view_hours_worked_rows = cur.fetchall()

    # Step 3: Show contents of relevant tables AFTER execution
    print(f"\nHours worked by shopper {shopper_id} for the week of {week_start} to {week_end}:")
    show_table(view_hours_worked_rows, 'shopper_id batch_id delivery_date start_time end_time hours_worked')

    # Calculate and display total hours worked for the week
    if view_hours_worked_rows:
        total_hours = 0
        for row in view_hours_worked_rows:
            hours = row[5]
            total_hours += hours
        print(f"\nShopper {shopper_id} worked {total_hours} hours for this week.")
    else:
        print(f"No batches found for shopper {shopper_id} during this week.")

view_hours_worked(6, '2025-11-30', '2025-12-06')