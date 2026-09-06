-- =============================================================================
-- PROJECT: Brazilian E-Commerce Advanced Business & Operations Analysis
-- DATABASE ENGINE: MySQL
-- TARGET TABLE: ecommerce_analysis_ready
-- AUTHOR: Priyadarshan Sharma
-- =============================================================================

USE olist_ecommerce;

-- -----------------------------------------------------------------------------
-- 0. DATA INTEGRITY CHECK
-- Purpose: Verify total loaded rows in analysis-ready dataset.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_records 
FROM ecommerce_analysis_ready;


-- -----------------------------------------------------------------------------
-- 1. MONTH-OVER-MONTH (MoM) SALES GROWTH & RETENTION
-- Business Objective: Analyze monthly revenue trajectory, buyer influx, and growth percentage.
-- Advanced Concepts: Window Function (LAG), CTE, Aggregations.
-- -----------------------------------------------------------------------------
WITH monthly_sales AS (
    SELECT 
        purchase_month,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_unique_id) AS total_unique_buyers,
        ROUND(SUM(total_payment), 2) AS total_revenue,
        ROUND(AVG(total_payment), 2) AS avg_order_value
    FROM ecommerce_analysis_ready
    WHERE order_status = 'delivered'
    GROUP BY purchase_month
),
monthly_growth AS (
    SELECT 
        purchase_month,
        total_orders,
        total_unique_buyers,
        total_revenue,
        avg_order_value,
        LAG(total_revenue) OVER (ORDER BY purchase_month) AS prev_month_revenue
    FROM monthly_sales
)
SELECT 
    purchase_month,
    total_orders,
    total_unique_buyers,
    total_revenue,
    prev_month_revenue,
    ROUND(
        ((total_revenue - prev_month_revenue) / NULLIF(prev_month_revenue, 0)) * 100, 
        2
    ) AS mom_growth_pct
FROM monthly_growth
ORDER BY purchase_month;


-- -----------------------------------------------------------------------------
-- 2. CUSTOMER RFM SEGMENTATION (Recency, Frequency, Monetary)
-- Business Objective: Categorize customer base into actionable loyalty tiers.
-- Advanced Concepts: NTILE Window Functions, Subqueries, Dynamic Scoring.
-- -----------------------------------------------------------------------------
WITH customer_metrics AS (
    SELECT 
        customer_unique_id,
        MAX(order_purchase_timestamp) AS last_order_date,
        COUNT(DISTINCT order_id) AS frequency,
        ROUND(SUM(total_payment), 2) AS monetary_value
    FROM ecommerce_analysis_ready
    WHERE order_status = 'delivered'
    GROUP BY customer_unique_id
),
rfm_scores AS (
    SELECT 
        customer_unique_id,
        DATEDIFF(
            (SELECT MAX(order_purchase_timestamp) FROM ecommerce_analysis_ready), 
            last_order_date
        ) AS recency_days,
        frequency,
        monetary_value,
        NTILE(4) OVER (
            ORDER BY DATEDIFF((SELECT MAX(order_purchase_timestamp) FROM ecommerce_analysis_ready), last_order_date) DESC
        ) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary_value ASC) AS m_score
    FROM customer_metrics
)
SELECT 
    customer_unique_id,
    recency_days,
    frequency,
    monetary_value,
    r_score,
    f_score,
    m_score,
    CASE 
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
        WHEN r_score >= 3 AND f_score < 3 THEN 'Recent Active Buyers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk / Need Attention'
        ELSE 'Lost Customers'
    END AS customer_segment
FROM rfm_scores
ORDER BY monetary_value DESC;


-- -----------------------------------------------------------------------------
-- 3. LOGISTICS PERFORMANCE & CUSTOMER SATISFACTION CORRELATION
-- Business Objective: Quantify how delivery delays impact 5-star vs bad ratings.
-- Advanced Concepts: Conditional Aggregation (CASE WHEN), Data Transformation.
-- -----------------------------------------------------------------------------
WITH delivery_classified AS (
    SELECT 
        order_id,
        review_score,
        delivery_days,
        CASE 
            WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 'Delayed'
            ELSE 'On-Time / Early'
        END AS delivery_status
    FROM ecommerce_analysis_ready
    WHERE order_delivered_customer_date IS NOT NULL 
      AND review_score IS NOT NULL
)
SELECT 
    delivery_status,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
    ROUND((COUNT(CASE WHEN review_score = 5 THEN 1 END) / COUNT(order_id)) * 100, 2) AS pct_5_star_reviews,
    ROUND((COUNT(CASE WHEN review_score <= 2 THEN 1 END) / COUNT(order_id)) * 100, 2) AS pct_bad_reviews
FROM delivery_classified
GROUP BY delivery_status;


-- -----------------------------------------------------------------------------
-- 4. REGIONAL TOP 3 PRODUCT CATEGORIES (STATE-WISE RANKING)
-- Business Objective: Determine top product demand by Brazilian state for localized inventory.
-- Advanced Concepts: DENSE_RANK() PARTITION BY, Multi-level CTEs.
-- -----------------------------------------------------------------------------
WITH state_category_revenue AS (
    SELECT 
        customer_state,
        product_category_name_english AS category_name,
        ROUND(SUM(total_payment), 2) AS total_revenue,
        COUNT(DISTINCT order_id) AS total_orders
    FROM ecommerce_analysis_ready
    WHERE product_category_name_english IS NOT NULL
    GROUP BY customer_state, product_category_name_english
),
ranked_categories AS (
    SELECT 
        customer_state,
        category_name,
        total_revenue,
        total_orders,
        DENSE_RANK() OVER (
            PARTITION BY customer_state 
            ORDER BY total_revenue DESC
        ) AS category_rank
    FROM state_category_revenue
)
SELECT 
    customer_state,
    category_rank,
    category_name,
    total_revenue,
    total_orders
FROM ranked_categories
WHERE category_rank <= 3
ORDER BY customer_state, category_rank;


-- -----------------------------------------------------------------------------
-- 5. PAYMENT INSTALLMENTS & ORDER VALUE CORRELATION
-- Business Objective: Assess customer purchasing power and review scores across installments.
-- Advanced Concepts: Filtering, Grouping, Financial KPIs.
-- -----------------------------------------------------------------------------
SELECT 
    total_installments AS installment_count,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(total_payment), 2) AS total_revenue,
    ROUND(AVG(total_payment), 2) AS avg_order_value,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM ecommerce_analysis_ready
WHERE total_installments > 0
GROUP BY total_installments
ORDER BY total_orders DESC;