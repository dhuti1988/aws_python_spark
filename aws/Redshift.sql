--Create a table to store the customer analytics data
CREATE TABLE customer_analytics.public.transactions_fact (
    channel_id        VARCHAR(20),
    customer_id       INT,
    transaction_id    VARCHAR(36),
    transaction_date  DATE,
    amount            DECIMAL(10,2),
    merchant_name     VARCHAR(100)
)
DISTSTYLE AUTO
SORTKEY(transaction_date);
