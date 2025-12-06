-- Trigger function for cancelling an order
CREATE OR REPLACE FUNCTION fn_cancel_order()
RETURNS TRIGGER 
LANGUAGE plpgsql AS 
$$
DECLARE
    refund_amount DECIMAL(10,2);
BEGIN
    -- Only do something if the new status is 'Cancelled' 
    -- and old status is Pending (no shopper has accepted order yet)
    IF NEW.status = 'Cancelled' AND OLD.status = 'Pending' THEN
        -- Calculate refund amount (negative of original total cost)
        refund_amount = -OLD.total_cost;
        -- Insert the refund record into Orders table
        INSERT INTO Orders (cart_id, batch_id, order_date, status, total_cost, payment_method)
        VALUES (
            OLD.cart_id,
            OLD.batch_id,
            now(),
            'Refunded',
            refund_amount,
            'Refund'
        );
    END IF;
    RETURN NULL;
END
$$;

-- Attach trigger to Orders table on UPDATE
DROP TRIGGER IF EXISTS tr_cancel_order ON Orders;
CREATE TRIGGER tr_cancel_order
AFTER UPDATE OF status ON Orders
FOR EACH ROW
EXECUTE FUNCTION fn_cancel_order();