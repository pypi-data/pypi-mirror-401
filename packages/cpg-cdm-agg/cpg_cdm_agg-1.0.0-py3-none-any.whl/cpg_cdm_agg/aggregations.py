"""
CPG Gold Layer Aggregations for Snowflake
==========================================

This module contains 31 aggregation functions for creating Gold layer Iceberg tables
from Silver layer data in Snowflake using Snowpark Python.

Each function can be used individually or in combination with others.
"""

from snowflake.snowpark.functions import (
    col, datediff, avg, sum as sum_, count, max as max_, min as min_,
    to_date, to_timestamp, when, lit, coalesce, concat, substr,
    to_char, countDistinct
)


# ============================================
# HELPER FUNCTION: Write to Gold Iceberg Table
# ============================================

def write_to_gold_iceberg(df, table_name, gold_db, gold_schema):
    """
    Write DataFrame to Gold layer Iceberg table.
    
    Args:
        df: Snowpark DataFrame to write
        table_name: Name of the target table
        gold_db: Gold layer database name
        gold_schema: Gold layer schema name
        
    Returns:
        int: Number of rows written
    """
    full_table_name = f"{gold_db}.{gold_schema}.{table_name}"
    df.write.mode("overwrite").save_as_table(full_table_name)
    return df.count()


# ============================================
# 1. DIMENSION TABLE FUNCTIONS
# ============================================

def dim_dates(dim_date):
    """
    Gold dimension date table.
    
    Args:
        dim_date: Silver layer dim_date table DataFrame
        
    Returns:
        Snowpark DataFrame with date dimension columns
    """
    return dim_date.select(
        col('"date_id"'),
        col('"full_date"'),
        col('"year"'),
        col('"quarter"'),
        col('"month"'),
        col('"month_name"'),
        col('"week"'),
        col('"day"'),
        col('"day_of_week"'),
        col('"day_name"'),
        col('"fiscal_year"'),
        col('"fiscal_quarter"'),
        col('"is_weekend"'),
        col('"is_holiday"'),
        col('"is_month_end"'),
        col('"is_year_end"')
    )


# ============================================
# 2-5. RMS (Raw Material Sourcing) FUNCTIONS
# ============================================

def rms_fact_sustainability(dim_supplier_master):
    """
    RMS Sustainability facts - raw columns for scoring.
    
    Args:
        dim_supplier_master: Silver layer dim_supplier_master table DataFrame
        
    Returns:
        Snowpark DataFrame with supplier sustainability metrics
    """
    d = dim_supplier_master
    
    return d.select(
        d['"supplier_name"'],
        d['"country"'],
        d['"region"'],
        d['"vendor_category"'],
        d['"sustainability_rating"'],
        d['"compliance_score"']
    )


def rms_delivery_delay(fact_goods_receipt, fact_purchase_order_line, fact_purchase_order_header, 
                       dim_supplier_master, dim_material_master, dim_product_master):
    """
    RMS Delivery delay analysis - raw columns.
    
    Args:
        fact_goods_receipt: Silver layer fact_goods_receipt table DataFrame
        fact_purchase_order_line: Silver layer fact_purchase_order_line table DataFrame
        fact_purchase_order_header: Silver layer fact_purchase_order_header table DataFrame
        dim_supplier_master: Silver layer dim_supplier_master table DataFrame
        dim_material_master: Silver layer dim_material_master table DataFrame
        dim_product_master: Silver layer dim_product_master table DataFrame
        
    Returns:
        Snowpark DataFrame with delivery delay metrics
    """
    g = fact_goods_receipt
    pol = fact_purchase_order_line
    poh = fact_purchase_order_header
    sup = dim_supplier_master
    mat = dim_material_master
    prod = dim_product_master
    
    result = g.join(pol, 
                   (g['"po_id"'] == pol['"po_id"']) & 
                   (g['"line_item_no"'] == pol['"line_item_no"']), 
                   "inner") \
        .join(poh, pol['"po_id"'] == poh['"po_id"'], "inner") \
        .join(sup, poh['"supplier_id"'] == sup['"supplier_id"'], "inner") \
        .join(mat, pol['"material_id"'] == mat['"material_id"'], "inner") \
        .join(prod, pol['"product_id"'] == prod['"product_id"'], "inner")
    
    return result.select(
        sup['"supplier_name"'],
        sup['"country"'],
        sup['"region"'],
        mat['"material_name"'],
        prod['"product_name"'],
        g['"receipt_date"'],
        pol['"expected_delivery_date"'],
        datediff("day", pol['"expected_delivery_date"'], g['"receipt_date"']).alias("delivery_delay_days")
    )


def rms_procurement_lead_time(fact_goods_receipt, fact_purchase_order_line, fact_purchase_order_header, 
                              dim_supplier_master, dim_material_master, dim_product_master):
    """
    RMS Procurement lead time analysis - raw columns.
    
    Args:
        fact_goods_receipt: Silver layer fact_goods_receipt table DataFrame
        fact_purchase_order_line: Silver layer fact_purchase_order_line table DataFrame
        fact_purchase_order_header: Silver layer fact_purchase_order_header table DataFrame
        dim_supplier_master: Silver layer dim_supplier_master table DataFrame
        dim_material_master: Silver layer dim_material_master table DataFrame
        dim_product_master: Silver layer dim_product_master table DataFrame
        
    Returns:
        Snowpark DataFrame with procurement lead time metrics
    """
    g = fact_goods_receipt
    pol = fact_purchase_order_line
    poh = fact_purchase_order_header
    sup = dim_supplier_master
    mat = dim_material_master
    prod = dim_product_master
    
    result = g.join(pol, 
                   (g['"po_id"'] == pol['"po_id"']) & 
                   (g['"line_item_no"'] == pol['"line_item_no"']), 
                   "inner") \
        .join(poh, pol['"po_id"'] == poh['"po_id"'], "inner") \
        .join(sup, poh['"supplier_id"'] == sup['"supplier_id"'], "inner") \
        .join(mat, pol['"material_id"'] == mat['"material_id"'], "inner") \
        .join(prod, pol['"product_id"'] == prod['"product_id"'], "inner")
    
    return result.select(
        sup['"supplier_name"'],
        sup['"country"'],
        sup['"region"'],
        mat['"material_name"'],
        prod['"product_name"'],
        g['"receipt_date"'],
        poh['"order_date"'],
        datediff("day", poh['"order_date"'], g['"receipt_date"']).alias("procurement_lead_time_days")
    )


def rms_grn_to_po(fact_goods_receipt, fact_purchase_order_line, fact_purchase_order_header, 
                  dim_supplier_master, dim_product_master, dim_material_master):
    """
    RMS aggregated metrics (raw aggregates only).
    
    Args:
        fact_goods_receipt: Silver layer fact_goods_receipt table DataFrame
        fact_purchase_order_line: Silver layer fact_purchase_order_line table DataFrame
        fact_purchase_order_header: Silver layer fact_purchase_order_header table DataFrame
        dim_supplier_master: Silver layer dim_supplier_master table DataFrame
        dim_product_master: Silver layer dim_product_master table DataFrame
        dim_material_master: Silver layer dim_material_master table DataFrame
        
    Returns:
        Snowpark DataFrame with GRN to PO aggregated metrics
    """
    g = fact_goods_receipt
    pol = fact_purchase_order_line
    poh = fact_purchase_order_header
    sup = dim_supplier_master
    prod = dim_product_master
    mat = dim_material_master
    
    result = g.join(pol, 
                   (g['"po_id"'] == pol['"po_id"']) & 
                   (g['"line_item_no"'] == pol['"line_item_no"']), 
                   "inner") \
        .join(poh, pol['"po_id"'] == poh['"po_id"'], "inner") \
        .join(sup, poh['"supplier_id"'] == sup['"supplier_id"'], "inner") \
        .join(prod, pol['"product_id"'] == prod['"product_id"'], "inner") \
        .join(mat, pol['"material_id"'] == mat['"material_id"'], "inner")

    grouped = result.group_by(
        sup['"supplier_name"'],
        sup['"country"'],
        sup['"region"'],
        mat['"material_name"'],
        prod['"product_name"'],
        g['"receipt_date"']
    )

    return grouped.agg(
        sum_(g['"received_qty"']).alias("total_received_qty"),
        sum_(pol['"quantity"']).alias("total_ordered_qty"),
        sum_(g['"rejected_qty"']).alias("total_rejected_qty"),
        countDistinct(g['"grn_id"']).alias("grn_count"),
        countDistinct(poh['"po_id"']).alias("po_count")
    )


# ============================================
# 6-9. PM (Production Management) FUNCTIONS
# ============================================

def pm_scrap_and_raw(fact_production_batch, fact_shift_log, dim_production_line, dim_facility_master):
    """
    Production metrics - raw columns for KPI calculation.
    
    Args:
        fact_production_batch: Silver layer fact_production_batch table DataFrame
        fact_shift_log: Silver layer fact_shift_log table DataFrame
        dim_production_line: Silver layer dim_production_line table DataFrame
        dim_facility_master: Silver layer dim_facility_master table DataFrame
        
    Returns:
        Snowpark DataFrame with production scrap and raw material metrics
    """
    fpb = fact_production_batch
    fsl = fact_shift_log
    dpl = dim_production_line
    dfm = dim_facility_master
    
    result = fpb.join(fsl, fpb['"batch_id"'] == fsl['"batch_id"'], "inner") \
        .join(dpl, fsl['"line_id"'] == dpl['"line_id"'], "inner") \
        .join(dfm, dpl['"facility_id"'] == dfm['"facility_id"'], "inner")
    
    return result.select(
        dfm['"country"'],
        dfm['"state"'],
        dfm['"city"'],
        dfm['"location"'],
        dfm['"name"'].alias("facility_name"),
        fpb['"good_qty"'],
        fpb['"produced_qty"'],
        fpb['"scrap_qty"'],
        fpb['"raw_material_used_qty"'],
        fpb['"start_time"'],
        fpb['"end_time"']
    )


def pm_plan_adherence(fact_production_schedule_line, fact_production_schedule_header, 
                      dim_production_line, dim_facility_master):
    """
    Production plan adherence - raw columns.
    
    Args:
        fact_production_schedule_line: Silver layer fact_production_schedule_line table DataFrame
        fact_production_schedule_header: Silver layer fact_production_schedule_header table DataFrame
        dim_production_line: Silver layer dim_production_line table DataFrame
        dim_facility_master: Silver layer dim_facility_master table DataFrame
        
    Returns:
        Snowpark DataFrame with plan adherence metrics
    """
    psl = fact_production_schedule_line
    psh = fact_production_schedule_header
    dpl = dim_production_line
    dfm = dim_facility_master
    
    result = psl.join(psh, psl['"schedule_id"'] == psh['"schedule_id"'], "inner") \
        .join(dpl, psh['"line_id"'] == dpl['"line_id"'], "inner") \
        .join(dfm, dpl['"facility_id"'] == dfm['"facility_id"'], "inner")
    
    return result.select(
        dfm['"country"'],
        dfm['"state"'],
        dfm['"city"'],
        dfm['"location"'],
        dfm['"name"'].alias("facility_name"),
        psl['"planned_qty"'],
        psl['"actual_qty"']
    )


def pm_downtime_per_shift_aggregated(fact_line_efficiency_log, fact_shift_log, fact_equipment_downtime_log, 
                                      dim_production_line, dim_facility_master):
    """
    Production downtime per shift - aggregated metrics.
    
    Args:
        fact_line_efficiency_log: Silver layer fact_line_efficiency_log table DataFrame
        fact_shift_log: Silver layer fact_shift_log table DataFrame
        fact_equipment_downtime_log: Silver layer fact_equipment_downtime_log table DataFrame
        dim_production_line: Silver layer dim_production_line table DataFrame
        dim_facility_master: Silver layer dim_facility_master table DataFrame
        
    Returns:
        Snowpark DataFrame with downtime aggregated metrics
    """
    fle = fact_line_efficiency_log
    fsl = fact_shift_log
    fedl = fact_equipment_downtime_log
    dpl = dim_production_line
    dfm = dim_facility_master
    
    result = fle.join(fsl, fle['"shift_id"'] == fsl['"shift_id"'], "inner") \
        .join(fedl, fsl['"shift_id"'] == fedl['"log_id"'], "inner") \
        .join(dpl, fle['"line_id"'] == dpl['"line_id"'], "inner") \
        .join(dfm, dpl['"facility_id"'] == dfm['"facility_id"'], "inner")
    
    # Add facility_name column before grouping
    result = result.with_column("facility_name", dfm['"name"'])
    
    grouped = result.group_by(
        dfm['"country"'],
        dfm['"state"'],
        dfm['"city"'],
        dfm['"location"'],
        col("facility_name")
    )
    
    return grouped.agg(
        sum_(datediff("second", fedl['"start_time"'], fedl['"end_time"']) / 60).alias("total_downtime_minutes"),
        count(fle['"shift_id"']).alias("total_shifts")
    )


def pm_downtime_per_shift_oeee(fact_line_efficiency_log, fact_shift_log, dim_production_line, dim_facility_master):
    """
    Production OEEE percentage - separate function for non-aggregated column.
    
    Args:
        fact_line_efficiency_log: Silver layer fact_line_efficiency_log table DataFrame
        fact_shift_log: Silver layer fact_shift_log table DataFrame
        dim_production_line: Silver layer dim_production_line table DataFrame
        dim_facility_master: Silver layer dim_facility_master table DataFrame
        
    Returns:
        Snowpark DataFrame with OEEE percentage metrics
    """
    fle = fact_line_efficiency_log
    fsl = fact_shift_log
    dpl = dim_production_line
    dfm = dim_facility_master
    
    result = fle.join(fsl, fle['"shift_id"'] == fsl['"shift_id"'], "inner") \
        .join(dpl, fle['"line_id"'] == dpl['"line_id"'], "inner") \
        .join(dfm, dpl['"facility_id"'] == dfm['"facility_id"'], "inner")
    
    return result.select(
        dfm['"country"'],
        dfm['"state"'],
        dfm['"city"'],
        dfm['"location"'],
        dfm['"name"'].alias("facility_name"),
        fle['"oeee_pct"']
    )


# ============================================
# 10-15. DSC (Distribution & Supply Chain) FUNCTIONS
# ============================================

def dsc_cogs(fact_product_inventory, dim_warehouse_master, dim_product_master, fact_sales_order_line):
    """
    Distribution & Supply Chain metrics - raw columns for KPI calculation.
    
    Args:
        fact_product_inventory: Silver layer fact_product_inventory table DataFrame
        dim_warehouse_master: Silver layer dim_warehouse_master table DataFrame
        dim_product_master: Silver layer dim_product_master table DataFrame
        fact_sales_order_line: Silver layer fact_sales_order_line table DataFrame
        
    Returns:
        Snowpark DataFrame with COGS metrics
    """
    fpi = fact_product_inventory
    dwm = dim_warehouse_master
    dpm = dim_product_master
    fsol = fact_sales_order_line
    
    result = fpi.join(dwm, fpi['"warehouse_id"'] == dwm['"warehouse_id"'], "inner") \
        .join(dpm, fpi['"product_id"'] == dpm['"product_id"'], "inner") \
        .join(fsol, fpi['"product_id"'] == fsol['"product_id"'], "left")
    
    # Add date column before grouping
    result = result.with_column("date", fpi['"updated_date"'])
    
    grouped = result.group_by(
        dwm['"warehouse_name"'],
        dpm['"product_name"'],
        col("date")
    )
    
    return grouped.agg(
        sum_(fpi['"quantity_on_hand"']).alias("total_quantity_on_hand"),
        sum_(dwm['"capacity_units"']).alias("total_capacity_units"),
        sum_(fsol['"cogs"']).alias("total_cogs")
    )


def dsc_inventory_days(fact_product_inventory, dim_warehouse_master, dim_product_master, fact_sales_order_line):
    """
    Distribution & Supply Chain - separate function for inventory days calculation.
    
    Args:
        fact_product_inventory: Silver layer fact_product_inventory table DataFrame
        dim_warehouse_master: Silver layer dim_warehouse_master table DataFrame
        dim_product_master: Silver layer dim_product_master table DataFrame
        fact_sales_order_line: Silver layer fact_sales_order_line table DataFrame
        
    Returns:
        Snowpark DataFrame with inventory days metrics
    """
    fpi = fact_product_inventory
    dwm = dim_warehouse_master
    dpm = dim_product_master
    fsol = fact_sales_order_line
    
    result = fpi.join(dwm, fpi['"warehouse_id"'] == dwm['"warehouse_id"'], "inner") \
        .join(dpm, fpi['"product_id"'] == dpm['"product_id"'], "inner") \
        .join(fsol, fpi['"product_id"'] == fsol['"product_id"'], "left")
    
    return result.select(
        dwm['"warehouse_name"'],
        dpm['"product_name"'],
        fpi['"updated_date"'].alias("date"),
        fpi['"quantity_on_hand"'],
        fsol['"cogs"']
    )


def dsc_damaged_return(fact_outbound_shipment, dim_carrier_master, fact_shipment_line, fact_return_order, 
                       fact_purchase_order_line, fact_purchase_order_header, dim_supplier_master):
    """
    DSC Damaged goods and returns analysis - raw columns.
    
    Args:
        fact_outbound_shipment: Silver layer fact_outbound_shipment table DataFrame
        dim_carrier_master: Silver layer dim_carrier_master table DataFrame
        fact_shipment_line: Silver layer fact_shipment_line table DataFrame
        fact_return_order: Silver layer fact_return_order table DataFrame
        fact_purchase_order_line: Silver layer fact_purchase_order_line table DataFrame
        fact_purchase_order_header: Silver layer fact_purchase_order_header table DataFrame
        dim_supplier_master: Silver layer dim_supplier_master table DataFrame
        
    Returns:
        Snowpark DataFrame with damaged goods and returns metrics
    """
    fos = fact_outbound_shipment
    dcm = dim_carrier_master
    fsl = fact_shipment_line
    fro = fact_return_order
    fpol = fact_purchase_order_line
    fpoh = fact_purchase_order_header
    dsm = dim_supplier_master
    
    result = fos.join(dcm, fos['"carrier_id"'] == dcm['"carrier_id"'], "inner") \
        .join(fsl, fos['"shipment_id"'] == fsl['"shipment_id"'], "inner") \
        .join(fro, (fro['"product_id"'] == fsl['"product_id"']) & (fro['"warehouse_id"'] == fos['"origin_warehouse_id"']), "left") \
        .join(fpol, fpol['"product_id"'] == fsl['"product_id"'], "left") \
        .join(fpoh, fpoh['"po_id"'] == fpol['"po_id"'], "left") \
        .join(dsm, dsm['"supplier_id"'] == fpoh['"supplier_id"'], "left")
    
    grouped = result.group_by(
        dcm['"carrier_name"'],
        dsm['"supplier_name"']
    )
    
    return grouped.agg(
        sum_(fsl['"quantity"']).alias("total_shipped_quantity"),
        sum_(fro['"quantity"']).alias("total_returned_quantity"),
        sum_(when(fro['"condition_on_return"'] == lit("Damaged"), fro['"quantity"']).otherwise(lit(0))).alias("total_damaged_quantity")
    )


def dsc_transport_cost_per_unit(fact_transportation_cost, dim_carrier_master, dim_truck_route, fact_outbound_shipment):
    """
    DSC Transportation cost per unit - raw columns.
    
    Args:
        fact_transportation_cost: Silver layer fact_transportation_cost table DataFrame
        dim_carrier_master: Silver layer dim_carrier_master table DataFrame
        dim_truck_route: Silver layer dim_truck_route table DataFrame
        fact_outbound_shipment: Silver layer fact_outbound_shipment table DataFrame
        
    Returns:
        Snowpark DataFrame with transportation cost metrics
    """
    ftc = fact_transportation_cost
    dcm = dim_carrier_master
    dtr = dim_truck_route
    fos = fact_outbound_shipment
    
    result = ftc.join(dcm, ftc['"carrier_id"'] == dcm['"carrier_id"'], "inner") \
        .join(dtr, ftc['"route_id"'] == dtr['"route_id"'], "inner") \
        .join(fos, (ftc['"carrier_id"'] == fos['"carrier_id"']) & (ftc['"shipment_date"'] <= fos['"planned_ship_date"']), "left")
    
    grouped = result.group_by(
        dcm['"carrier_name"'],
        dtr['"route_type"'],
        ftc['"shipment_date"']
    )
    
    return grouped.agg(
        sum_(ftc['"total_cost"']).alias("total_transportation_cost"),
        sum_(fos['"total_qty"']).alias("total_quantity")
    )


def dsc_on_time_shipment_rate(fact_outbound_shipment, dim_carrier_master, dim_distribution_center):
    """
    DSC On-time shipment rate - raw columns.
    
    Args:
        fact_outbound_shipment: Silver layer fact_outbound_shipment table DataFrame
        dim_carrier_master: Silver layer dim_carrier_master table DataFrame
        dim_distribution_center: Silver layer dim_distribution_center table DataFrame
        
    Returns:
        Snowpark DataFrame with on-time shipment rate metrics
    """
    fos = fact_outbound_shipment
    dcm = dim_carrier_master
    ddc = dim_distribution_center
    
    result = fos.join(dcm, fos['"carrier_id"'] == dcm['"carrier_id"'], "inner") \
        .join(ddc, fos['"origin_warehouse_id"'] == ddc['"dc_id"'], "inner")
    
    # Add columns before grouping
    result = result.with_column("distribution_center", ddc['"dc_name"'])
    result = result.with_column("month", to_char(fos['"planned_ship_date"'], lit("YYYY-MM")))
    
    grouped = result.group_by(
        dcm['"carrier_name"'],
        col("distribution_center"),
        col("month")
    )
    
    return grouped.agg(
        count(when(fos['"ship_date"'] <= fos['"planned_ship_date"'], lit(1))).alias("on_time_shipments"),
        count(lit(1)).alias("total_shipments")
    )


def dsc_inbound_delivery_accuracy(fact_inbound_shipment, dim_supplier_master, dim_warehouse_master):
    """
    DSC Inbound delivery accuracy - raw columns.
    
    Args:
        fact_inbound_shipment: Silver layer fact_inbound_shipment table DataFrame
        dim_supplier_master: Silver layer dim_supplier_master table DataFrame
        dim_warehouse_master: Silver layer dim_warehouse_master table DataFrame
        
    Returns:
        Snowpark DataFrame with inbound delivery accuracy metrics
    """
    fis = fact_inbound_shipment
    dsm = dim_supplier_master
    dwm = dim_warehouse_master
    
    result = fis.join(dsm, fis['"source_id"'] == dsm['"supplier_id"'], "inner") \
        .join(dwm, fis['"destination_warehouse_id"'] == dwm['"warehouse_id"'], "inner")
    
    # Add date column before grouping
    result = result.with_column("date", fis['"actual_delivery_date"'])
    
    grouped = result.group_by(
        dsm['"supplier_name"'],
        dwm['"warehouse_name"'],
        col("date")
    )
    
    return grouped.agg(
        count(when(fis['"actual_delivery_date"'] <= fis['"expected_delivery_date"'], lit(1))).alias("on_time_deliveries"),
        count(lit(1)).alias("total_deliveries")
    )


# ============================================
# 16-21. REUS (Retail & End User Sales) FUNCTIONS
# ============================================

def reus_customer_retention_monthly_totals(fact_sales_order, fact_customer_visit):
    """
    Customer retention monthly analysis - aggregated totals.
    
    Args:
        fact_sales_order: Silver layer fact_sales_order table DataFrame
        fact_customer_visit: Silver layer fact_customer_visit table DataFrame
        
    Returns:
        Snowpark DataFrame with monthly customer totals
    """
    fso = fact_sales_order
    fcv = fact_customer_visit
    
    # CTE: customer_orders - use explicit column names
    customer_orders = fso.select(
        col('"customer_id"').alias("co_customer_id"),
        col('"channel"').alias("co_channel"),
        to_char(col('"order_date"'), lit("YYYY-MM")).alias("co_month_year")
    )
    
    # CTE: customer_visits_device
    customer_visits_device = fcv.select(
        col('"customer_id"').alias("cvd_customer_id"),
        col('"channel"').alias("cvd_channel"),
        col('"device_type"').alias("cvd_device_type"),
        to_char(col('"visit_timestamp"'), lit("YYYY-MM")).alias("cvd_month_year")
    )
    
    # CTE: customer_month_visits - use aliased column names
    customer_month_visits = customer_orders.join(
        customer_visits_device,
        (col("co_customer_id") == col("cvd_customer_id")) & 
        (col("co_channel") == col("cvd_channel")) & 
        (col("co_month_year") == col("cvd_month_year")),
        "left"
    ).select(
        col("co_customer_id").alias("customer_id"),
        col("co_channel").alias("channel"),
        coalesce(col("cvd_device_type"), lit("Unknown")).alias("device_type"),
        col("co_month_year").alias("month_year")
    )
    
    # Monthly totals
    monthly_totals = customer_month_visits.group_by(
        col("channel"), 
        col("device_type"), 
        col("month_year")
    ).agg(
        countDistinct(col("customer_id")).alias("total_customers")
    )
    
    return monthly_totals


def reus_customer_retention_monthly_retained(fact_sales_order, fact_customer_visit):
    """
    Customer retention monthly analysis - retained customers.
    
    Args:
        fact_sales_order: Silver layer fact_sales_order table DataFrame
        fact_customer_visit: Silver layer fact_customer_visit table DataFrame
        
    Returns:
        Snowpark DataFrame with retained customer counts
    """
    fso = fact_sales_order
    fcv = fact_customer_visit
    
    # CTE: customer_orders - use explicit column names
    customer_orders = fso.select(
        col('"customer_id"').alias("co_customer_id"),
        col('"channel"').alias("co_channel"),
        to_char(col('"order_date"'), lit("YYYY-MM")).alias("co_month_year")
    )
    
    # CTE: customer_visits_device
    customer_visits_device = fcv.select(
        col('"customer_id"').alias("cvd_customer_id"),
        col('"channel"').alias("cvd_channel"),
        col('"device_type"').alias("cvd_device_type"),
        to_char(col('"visit_timestamp"'), lit("YYYY-MM")).alias("cvd_month_year")
    )
    
    # CTE: customer_month_visits
    customer_month_visits = customer_orders.join(
        customer_visits_device,
        (col("co_customer_id") == col("cvd_customer_id")) & 
        (col("co_channel") == col("cvd_channel")) & 
        (col("co_month_year") == col("cvd_month_year")),
        "left"
    ).select(
        col("co_customer_id").alias("customer_id"),
        col("co_channel").alias("channel"),
        coalesce(col("cvd_device_type"), lit("Unknown")).alias("device_type"),
        col("co_month_year").alias("month_year")
    )
    
    # Create current and previous month dataframes with explicit aliases
    curr = customer_month_visits.select(
        col("customer_id").alias("curr_customer_id"),
        col("channel").alias("curr_channel"),
        col("device_type").alias("curr_device_type"),
        col("month_year").alias("curr_month_year"),
        to_date(concat(substr(col("month_year"), 1, 4), lit("-"), substr(col("month_year"), 6, 2), lit("-01"))).alias("curr_date")
    )
    
    prev = customer_month_visits.select(
        col("customer_id").alias("prev_customer_id"),
        col("channel").alias("prev_channel"),
        col("device_type").alias("prev_device_type"),
        col("month_year").alias("prev_month_year"),
        to_date(concat(substr(col("month_year"), 1, 4), lit("-"), substr(col("month_year"), 6, 2), lit("-01"))).alias("prev_date")
    )
    
    # Join for retained customers (same customer in consecutive months)
    pairs = curr.join(
        prev,
        (col("curr_channel") == col("prev_channel")) &
        (col("curr_device_type") == col("prev_device_type")) &
        (col("curr_customer_id") == col("prev_customer_id")) &
        (datediff("day", col("prev_date"), col("curr_date")) >= 28) &
        (datediff("day", col("prev_date"), col("curr_date")) <= 31),
        "inner"
    )
    
    result = pairs.group_by(
        col("curr_channel").alias("channel"),
        col("curr_device_type").alias("device_type"),
        col("curr_month_year").alias("month")
    ).agg(
        countDistinct(col("curr_customer_id")).alias("retained_customers")
    )
    
    return result


def reus_customer_retention_monthly_new(fact_sales_order, fact_customer_visit):
    """
    Customer retention monthly analysis - new customers.
    
    Args:
        fact_sales_order: Silver layer fact_sales_order table DataFrame
        fact_customer_visit: Silver layer fact_customer_visit table DataFrame
        
    Returns:
        Snowpark DataFrame with new customer counts
    """
    fso = fact_sales_order
    fcv = fact_customer_visit
    
    # CTE: customer_orders - use explicit column names
    customer_orders = fso.select(
        col('"customer_id"').alias("co_customer_id"),
        col('"channel"').alias("co_channel"),
        to_char(col('"order_date"'), lit("YYYY-MM")).alias("co_month_year")
    )
    
    # CTE: customer_visits_device
    customer_visits_device = fcv.select(
        col('"customer_id"').alias("cvd_customer_id"),
        col('"channel"').alias("cvd_channel"),
        col('"device_type"').alias("cvd_device_type"),
        to_char(col('"visit_timestamp"'), lit("YYYY-MM")).alias("cvd_month_year")
    )
    
    # CTE: customer_month_visits
    customer_month_visits = customer_orders.join(
        customer_visits_device,
        (col("co_customer_id") == col("cvd_customer_id")) & 
        (col("co_channel") == col("cvd_channel")) & 
        (col("co_month_year") == col("cvd_month_year")),
        "left"
    ).select(
        col("co_customer_id").alias("customer_id"),
        col("co_channel").alias("channel"),
        coalesce(col("cvd_device_type"), lit("Unknown")).alias("device_type"),
        col("co_month_year").alias("month_year")
    )
    
    # Create current and previous month dataframes with explicit aliases
    curr = customer_month_visits.select(
        col("customer_id").alias("curr_customer_id"),
        col("channel").alias("curr_channel"),
        col("device_type").alias("curr_device_type"),
        col("month_year").alias("curr_month_year")
    )
    
    prev = customer_month_visits.select(
        col("customer_id").alias("prev_customer_id"),
        col("channel").alias("prev_channel"),
        col("device_type").alias("prev_device_type"),
        col("month_year").alias("prev_month_year")
    )
    
    # Find new customers (those who don't exist in previous months)
    new_customers = curr.join(
        prev,
        (col("curr_customer_id") == col("prev_customer_id")) &
        (col("curr_channel") == col("prev_channel")) &
        (col("curr_device_type") == col("prev_device_type")) &
        (col("prev_month_year") < col("curr_month_year")),
        "left"
    ).filter(
        col("prev_customer_id").isNull()
    )
    
    result = new_customers.group_by(
        col("curr_channel").alias("channel"),
        col("curr_device_type").alias("device_type"),
        col("curr_month_year").alias("month")
    ).agg(
        countDistinct(col("curr_customer_id")).alias("new_customers")
    )
    
    return result


def reus_product_return_analysis(fact_return_order, fact_sales_order, dim_channel, 
                                  dim_product_master, dim_material_category):
    """
    Product return analysis - raw columns.
    
    Args:
        fact_return_order: Silver layer fact_return_order table DataFrame
        fact_sales_order: Silver layer fact_sales_order table DataFrame
        dim_channel: Silver layer dim_channel table DataFrame
        dim_product_master: Silver layer dim_product_master table DataFrame
        dim_material_category: Silver layer dim_material_category table DataFrame
        
    Returns:
        Snowpark DataFrame with product return analysis metrics
    """
    fro = fact_return_order
    fso = fact_sales_order
    dc = dim_channel
    dpm = dim_product_master
    dmc = dim_material_category
    
    result = fro.join(fso, fro['"original_sales_order_id"'] == fso['"sales_order_id"'], "inner") \
        .join(dc, fro['"channel_id"'] == dc['"channel_id"'], "inner") \
        .join(dpm, fro['"product_id"'] == dpm['"product_id"'], "inner") \
        .join(dmc, dpm['"category_id"'] == dmc['"category_id"'], "inner")
    
    # Add columns before grouping
    result = result.with_column("product_category", dmc['"category_name"'])
    result = result.with_column("date", fro['"return_date"'])
    
    grouped = result.group_by(
        dc['"channel_name"'],
        col("product_category"),
        dpm['"product_name"'],
        col("date")
    )
    
    return grouped.agg(
        sum_(fro['"refund_amount"']).alias("total_refund_amount"),
        sum_(fso['"total_amount"']).alias("total_sales_amount"),
        countDistinct(fro['"return_id"']).alias("total_returns"),
        countDistinct(fso['"sales_order_id"']).alias("total_orders")
    )


def reus_average_order_value_analysis(fact_sales_order, dim_retail_outlet, dim_customer_master, dim_region_hierarchy):
    """
    Average order value analysis - raw columns.
    
    Args:
        fact_sales_order: Silver layer fact_sales_order table DataFrame
        dim_retail_outlet: Silver layer dim_retail_outlet table DataFrame
        dim_customer_master: Silver layer dim_customer_master table DataFrame
        dim_region_hierarchy: Silver layer dim_region_hierarchy table DataFrame
        
    Returns:
        Snowpark DataFrame with average order value metrics
    """
    fso = fact_sales_order
    dro = dim_retail_outlet
    dcm = dim_customer_master
    drh = dim_region_hierarchy
    
    result = fso.join(dro, fso['"outlet_id"'] == dro['"outlet_id"'], "inner") \
        .join(dcm, fso['"customer_id"'] == dcm['"customer_id"'], "inner") \
        .join(drh, dro['"region_id"'] == drh['"region_id"'], "inner")
    
    # Add date column before grouping
    result = result.with_column("date", fso['"order_date"'])
    
    grouped = result.group_by(
        fso['"country"'],
        drh['"region"'],
        fso['"channel"'],
        dro['"outlet_name"'],
        dcm['"customer_name"'],
        col("date")
    )
    
    return grouped.agg(
        sum_(fso['"total_amount"']).alias("total_order_amount"),
        count(fso['"sales_order_id"']).alias("total_orders")
    )


def reus_sales_per_outlet_analysis(fact_sales_order, dim_retail_outlet, dim_region_hierarchy):
    """
    Sales per outlet analysis - raw columns.
    
    Args:
        fact_sales_order: Silver layer fact_sales_order table DataFrame
        dim_retail_outlet: Silver layer dim_retail_outlet table DataFrame
        dim_region_hierarchy: Silver layer dim_region_hierarchy table DataFrame
        
    Returns:
        Snowpark DataFrame with sales per outlet metrics
    """
    fso = fact_sales_order
    dro = dim_retail_outlet
    drh = dim_region_hierarchy
    
    result = fso.join(dro, fso['"outlet_id"'] == dro['"outlet_id"'], "inner") \
        .join(drh, dro['"region_id"'] == drh['"region_id"'], "inner")
    
    # Add date column before grouping
    result = result.with_column("date", fso['"order_date"'])
    
    grouped = result.group_by(
        fso['"country"'],
        drh['"region"'],
        fso['"channel"'],
        col("date")
    )
    
    return grouped.agg(
        countDistinct(fso['"outlet_id"']).alias("total_outlets"),
        sum_(fso['"total_amount"']).alias("total_sales")
    )


# ============================================
# 22-27. CFM (Consumer & Field Marketing) FUNCTIONS
# ============================================

def cfm_conversion_rate(fact_ad_impression):
    """
    CFM Conversion rate - raw columns.
    
    Args:
        fact_ad_impression: Silver layer fact_ad_impression table DataFrame
        
    Returns:
        Snowpark DataFrame with conversion rate metrics
    """
    fai = fact_ad_impression
    
    # Add columns before grouping
    result = fai.with_column("channel", fai['"platform"'])
    result = result.with_column("date", fai['"impression_date"'])
    
    grouped = result.group_by(
        col("channel"),
        col("date")
    )
    
    return grouped.agg(
        sum_(fai['"conversions"']).alias("total_conversions"),
        sum_(fai['"impressions"']).alias("total_impressions")
    )


def cfm_cost_per_conversion_spend(fact_marketing_spend, fact_ad_impression, dim_campaign_master):
    """
    CFM Cost per conversion - campaign spend aggregated.
    
    Args:
        fact_marketing_spend: Silver layer fact_marketing_spend table DataFrame
        fact_ad_impression: Silver layer fact_ad_impression table DataFrame
        dim_campaign_master: Silver layer dim_campaign_master table DataFrame
        
    Returns:
        Snowpark DataFrame with cost per conversion spend metrics
    """
    fms = fact_marketing_spend
    fai = fact_ad_impression
    dcm = dim_campaign_master
    
    # CTE: campaign_spend with explicit alias
    campaign_spend = fms.group_by(col('"campaign_id"')).agg(
        sum_(col('"amount"')).alias("total_spend_amount")
    ).select(
        col('"campaign_id"').alias("cs_campaign_id"),
        col("total_spend_amount")
    )
    
    # CTE: campaign_impressions with explicit alias
    campaign_impressions = fai.group_by(col('"campaign_id"')).agg(
        sum_(col('"conversions"')).alias("total_conversions")
    ).select(
        col('"campaign_id"').alias("ci_campaign_id"),
        col("total_conversions")
    )
    
    # CTE: campaign_details with explicit alias
    campaign_details = dcm.select(
        col('"campaign_id"').alias("cd_campaign_id"),
        col('"campaign_name"'),
        col('"start_date"'),
        col('"end_date"')
    )
    
    # Join CTEs using explicit aliases
    result = campaign_details \
        .join(campaign_spend, col("cd_campaign_id") == col("cs_campaign_id"), "left") \
        .join(campaign_impressions, col("cd_campaign_id") == col("ci_campaign_id"), "left")
    
    return result.select(
        col('"campaign_name"').alias("campaign"),
        col('"start_date"'),
        col('"end_date"'),
        coalesce(col("total_spend_amount"), lit(0)).alias("total_spend_amount"),
        coalesce(col("total_conversions"), lit(0)).alias("total_conversions")
    )


def cfm_cost_per_conversion_engagement(fact_ad_impression, dim_campaign_master):
    """
    CFM Cost per conversion - engagement time calculation.
    
    Args:
        fact_ad_impression: Silver layer fact_ad_impression table DataFrame
        dim_campaign_master: Silver layer dim_campaign_master table DataFrame
        
    Returns:
        Snowpark DataFrame with engagement time metrics
    """
    fai = fact_ad_impression
    dcm = dim_campaign_master
    
    # CTE: campaign_impressions with explicit alias
    campaign_impressions = fai.group_by(col('"campaign_id"')).agg(
        sum_(col('"impressions"')).alias("total_impressions")
    ).select(
        col('"campaign_id"').alias("ci_campaign_id"),
        col("total_impressions")
    )
    
    # CTE: campaign_details with explicit alias
    campaign_details = dcm.select(
        col('"campaign_id"').alias("cd_campaign_id"),
        col('"campaign_name"'),
        col('"start_date"'),
        col('"end_date"'),
        datediff("day", col('"start_date"'), col('"end_date"')).alias("time_engaged_days")
    )
    
    # Join CTEs using explicit aliases
    result = campaign_details \
        .join(campaign_impressions, col("cd_campaign_id") == col("ci_campaign_id"), "left")
    
    return result.select(
        col('"campaign_name"').alias("campaign"),
        col('"start_date"'),
        col('"end_date"'),
        col("time_engaged_days"),
        coalesce(col("total_impressions"), lit(0)).alias("total_impressions")
    )


def cfm_survey_response_rate(fact_consumer_survey):
    """
    CFM Survey response rate - raw columns.
    
    Args:
        fact_consumer_survey: Silver layer fact_consumer_survey table DataFrame
        
    Returns:
        Snowpark DataFrame with survey response rate metrics
    """
    fcs = fact_consumer_survey
    
    # Add date column before grouping
    result = fcs.with_column("date", col('"survey_date"'))
    
    grouped = result.group_by(
        col('"channel"'),
        col('"region"'),
        col("date")
    )
    
    return grouped.agg(
        count(when(col('"feedback_text"').isNotNull(), lit(1))).alias("responses_with_feedback"),
        count(col('"survey_id"')).alias("total_surveys")
    )


def cfm_customer_satisfaction_score(fact_consumer_survey, dim_product_master, dim_material_category):
    """
    CFM Customer satisfaction score - raw data.
    
    Args:
        fact_consumer_survey: Silver layer fact_consumer_survey table DataFrame
        dim_product_master: Silver layer dim_product_master table DataFrame
        dim_material_category: Silver layer dim_material_category table DataFrame
        
    Returns:
        Snowpark DataFrame with customer satisfaction score metrics
    """
    cs = fact_consumer_survey
    pm = dim_product_master
    mc = dim_material_category
    
    result = cs.join(pm, cs['"product_id"'] == pm['"product_id"'], "inner") \
        .join(mc, pm['"category_id"'] == mc['"category_id"'], "inner")
    
    return result.select(
        mc['"category_name"'].alias("product_category"),
        pm['"product_name"'],
        cs['"survey_date"'].alias("date"),
        cs['"satisfaction_score"']
    )


def cfm_trade_promotion_effectiveness(fact_promotion_plan, dim_promotion_master, dim_channel, fact_trade_promotion):
    """
    CFM Trade promotion effectiveness - raw columns.
    
    Args:
        fact_promotion_plan: Silver layer fact_promotion_plan table DataFrame
        dim_promotion_master: Silver layer dim_promotion_master table DataFrame
        dim_channel: Silver layer dim_channel table DataFrame
        fact_trade_promotion: Silver layer fact_trade_promotion table DataFrame
        
    Returns:
        Snowpark DataFrame with trade promotion effectiveness metrics
    """
    pp = fact_promotion_plan
    pm = dim_promotion_master
    dc = dim_channel
    tp = fact_trade_promotion
    
    result = pp.join(pm, pp['"promotion_id"'] == pm['"promotion_id"'], "inner") \
        .join(dc, pp['"channel_id"'] == dc['"channel_id"'], "inner") \
        .join(tp, pp['"product_id"'] == tp['"product_id"'], "left")
    
    # Add date column before grouping
    result = result.with_column("date", pp['"period_start"'])
    
    grouped = result.group_by(
        pm['"promotion_name"'],
        dc['"channel_name"'],
        col("date")
    )
    
    return grouped.agg(
        sum_(coalesce(tp['"actual_lift_pct"'], lit(0))).alias("total_actual_lift_pct"),
        sum_(pp['"target_lift_pct"']).alias("total_target_lift_pct")
    )


# ============================================
# 28-30. FC (Finance & Controlling) FUNCTIONS
# ============================================

def fc_invoice_accuracy_analysis(fact_invoice, fact_payment):
    """
    Calculate accurate and total invoices by snapshot_date and payment_method.
    
    Args:
        fact_invoice: Silver layer fact_invoice table DataFrame
        fact_payment: Silver layer fact_payment table DataFrame
        
    Returns:
        Snowpark DataFrame with invoice accuracy metrics
    """
    # Join fact_invoice with fact_payment to get payment method information
    result = fact_invoice.join(
        fact_payment,
        (fact_invoice['"customer_id"'] == fact_payment['"customer_id"']) & 
        (fact_invoice['"amount_paid"'] == fact_payment['"amount"']),
        "left"
    )
    
    # Group by snapshot_date and payment_method to calculate metrics
    aggregated_result = result.group_by(
        fact_invoice['"snapshot_date"'],
        fact_payment['"payment_method"']
    ).agg(
        count(
            when(
                (fact_invoice['"payment_status"'] == lit("Paid")) & 
                (fact_invoice['"difference_days"'] <= lit(0)),
                lit(1)
            )
        ).alias("Accurate_Invoices"),
        count(fact_invoice['"invoice_id"']).alias("Total_Invoices")
    )
    
    # Use quoted identifiers for final select
    return aggregated_result.select(
        col('"snapshot_date"'),
        col('"payment_method"'),
        col("Accurate_Invoices"),
        col("Total_Invoices")
    ).sort(col('"snapshot_date"'), col('"payment_method"'))


def fc_budget(dim_account_master, fact_budget, fact_general_ledger):
    """
    Calculate Actual Spend vs Budget by account.
    
    Args:
        dim_account_master: Silver layer dim_account_master table DataFrame
        fact_budget: Silver layer fact_budget table DataFrame
        fact_general_ledger: Silver layer fact_general_ledger table DataFrame
        
    Returns:
        Snowpark DataFrame with budget vs actual spend metrics
    """
    # Calculate actual spend from general ledger with explicit alias
    actual_spend = fact_general_ledger.group_by(col('"account_id"')).agg(
        (sum_(fact_general_ledger['"debit"']) - sum_(fact_general_ledger['"credit"'])).alias("actual_spend_raw")
    ).select(
        col('"account_id"').alias("as_account_id"),
        col("actual_spend_raw")
    )
    
    # Get approved budgets with explicit alias
    budget_data = fact_budget.filter(
        fact_budget['"approved_flag"'] == lit(True)
    ).group_by(col('"account_id"')).agg(
        sum_(fact_budget['"budget_amount"']).alias("Budget")
    ).select(
        col('"account_id"').alias("bd_account_id"),
        col("Budget")
    )
    
    # Join all tables together using explicit aliases
    result = dim_account_master.join(
        actual_spend, 
        dim_account_master['"account_id"'] == col("as_account_id"), 
        "left"
    ).join(
        budget_data,
        dim_account_master['"account_id"'] == col("bd_account_id"),
        "left"
    )
    
    # Calculate Actual Spend based on account type
    final_result = result.select(
        dim_account_master['"account_name"'],
        when(
            dim_account_master['"account_type"'] == lit("Expense"),
            coalesce(col("actual_spend_raw"), lit(0))
        ).when(
            dim_account_master['"account_type"'] == lit("Revenue"),
            coalesce(-col("actual_spend_raw"), lit(0))
        ).otherwise(lit(0)).alias("Actual_Spend"),
        coalesce(col("Budget"), lit(0)).alias("Budget")
    ).filter(
        dim_account_master['"active_flag"'] == lit(True)
    )
    
    return final_result.sort(col('"account_name"'))


def fc_payment_timeliness_analysis(fact_payment, fact_invoice):
    """
    Calculate On-Time Payments and Total Payments by source_type and date.
    
    Args:
        fact_payment: Silver layer fact_payment table DataFrame
        fact_invoice: Silver layer fact_invoice table DataFrame
        
    Returns:
        Snowpark DataFrame with payment timeliness metrics
    """
    # Join fact_payment with fact_invoice
    result = fact_payment.join(
        fact_invoice,
        (fact_payment['"source_type"'] == lit("Invoice")) & 
        (fact_payment['"source_id"'] == fact_invoice['"invoice_id"']) & 
        (fact_payment['"customer_id"'] == fact_invoice['"customer_id"']),
        "left"
    )
    
    # Group by source_type and payment_date to calculate metrics
    aggregated_result = result.group_by(
        fact_payment['"source_type"'],
        fact_payment['"payment_date"']
    ).agg(
        count(
            when(
                (fact_payment['"source_type"'] != lit("Invoice")) |
                ((fact_payment['"source_type"'] == lit("Invoice")) & 
                 (fact_payment['"payment_date"'] <= fact_invoice['"due_date"'])),
                lit(1)
            )
        ).alias("On_Time_Payments"),
        count(fact_payment['"payment_id"']).alias("Total_Payments")
    )
    
    # Use quoted identifiers for final select
    return aggregated_result.select(
        col('"source_type"'),
        col('"payment_date"'),
        col("On_Time_Payments"), 
        col("Total_Payments")
    ).sort(col('"payment_date"'), col('"source_type"'))


# ============================================
# 31. SESG (Sustainability & ESG) FUNCTIONS
# ============================================

def sesg_emission_production_analysis(fact_emission_record, fact_production_batch):
    """
    Calculate CO2e emissions by source type and correlate with production units.
    
    Args:
        fact_emission_record: Silver layer fact_emission_record table DataFrame
        fact_production_batch: Silver layer fact_production_batch table DataFrame
        
    Returns:
        Snowpark DataFrame with emission and production correlation metrics
    """
    # Prepare production data with date
    production_by_date = fact_production_batch.with_column(
        "production_date", 
        to_date(fact_production_batch['"start_time"'])
    ).group_by(col("production_date")).agg(
        sum_(col('"produced_qty"')).alias("daily_units_produced")
    )
    
    # Prepare emission data with explicit alias for source_type
    emission_by_date_source = fact_emission_record.group_by(
        col('"record_date"'),
        col('"source_type"')
    ).agg(
        sum_(col('"co2e_amount"')).alias("daily_co2e_amount")
    ).select(
        col('"record_date"').alias("emission_date"),
        col('"source_type"').alias("emission_source_type"),
        col("daily_co2e_amount")
    )
    
    # Join emissions with production on date
    result = emission_by_date_source.join(
        production_by_date,
        col("emission_date") == col("production_date"),
        "left"
    )
    
    # Aggregate by source_type for final output
    final_result = result.group_by(col("emission_source_type")).agg(
        sum_(col("daily_co2e_amount")).alias("CO2e_Amount"),
        sum_(col("daily_units_produced")).alias("Units_Produced")
    )
    
    return final_result.select(
        col("emission_source_type").alias("source_type"),
        coalesce(col("CO2e_Amount"), lit(0)).alias("CO2e_Amount"),
        coalesce(col("Units_Produced"), lit(0)).alias("Units_Produced")
    ).sort(col("source_type"))


# ============================================
# LIST OF ALL FUNCTIONS (for reference)
# ============================================

ALL_AGGREGATION_FUNCTIONS = [
    "dim_dates",
    "rms_fact_sustainability",
    "rms_delivery_delay",
    "rms_procurement_lead_time",
    "rms_grn_to_po",
    "pm_scrap_and_raw",
    "pm_plan_adherence",
    "pm_downtime_per_shift_aggregated",
    "pm_downtime_per_shift_oeee",
    "dsc_cogs",
    "dsc_inventory_days",
    "dsc_damaged_return",
    "dsc_transport_cost_per_unit",
    "dsc_on_time_shipment_rate",
    "dsc_inbound_delivery_accuracy",
    "reus_customer_retention_monthly_totals",
    "reus_customer_retention_monthly_retained",
    "reus_customer_retention_monthly_new",
    "reus_product_return_analysis",
    "reus_average_order_value_analysis",
    "reus_sales_per_outlet_analysis",
    "cfm_conversion_rate",
    "cfm_cost_per_conversion_spend",
    "cfm_cost_per_conversion_engagement",
    "cfm_survey_response_rate",
    "cfm_customer_satisfaction_score",
    "cfm_trade_promotion_effectiveness",
    "fc_invoice_accuracy_analysis",
    "fc_budget",
    "fc_payment_timeliness_analysis",
    "sesg_emission_production_analysis",
]
