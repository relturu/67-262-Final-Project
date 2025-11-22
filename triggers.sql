-- Trigger function for cancelling an order
CREATE OR REPLACE FUNCTION cancel_order_refund()
RETURNS TRIGGER AS $$
BEGIN
    -- Only do something if the status is updated to 'cancelled'
    IF NEW.status = 'cancelled' AND OLD.status <> 'cancelled' THEN
        -- Insert a "refund" order as a negative total_cost
        INSERT INTO Orders(order_date, status, total_cost, customer_id, cart_id)
        VALUES (
            now(),                    -- current timestamp
            'refund',                 -- mark as refund
            -OLD.total_cost,          -- negative of original
            OLD.customer_id, 
            OLD.cart_id
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Attach trigger to Orders table on UPDATE
DROP TRIGGER IF EXISTS trigger_cancel_order ON Orders;
CREATE TRIGGER trigger_cancel_order
AFTER UPDATE OF status ON Orders
FOR EACH ROW
EXECUTE FUNCTION cancel_order_refund();