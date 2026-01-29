"""
Snowflake Gold Layer Aggregations Package
==========================================

A Python package for creating Gold layer Iceberg tables from Silver layer data
in Snowflake using Snowpark Python.

This package contains 31 aggregation functions covering:
- Dimension Tables (1 function)
- RMS - Raw Material Sourcing (4 functions)
- PM - Production Management (4 functions)
- DSC - Distribution & Supply Chain (6 functions)
- REUS - Retail & End User Sales (6 functions)
- CFM - Consumer & Field Marketing (6 functions)
- FC - Finance & Controlling (3 functions)
- SESG - Sustainability & ESG (1 function)

Basic Usage:
-----------

    from snowflake.snowpark import Session
    from cpg_cdm_agg import GoldLayerExecutor, GoldLayerConfig

    # Create session
    session = Session.builder.configs(connection_parameters).create()

    # Create config with your database/schema names
    config = GoldLayerConfig(
        gold_db="MY_GOLD_DB",
        gold_schema="MY_GOLD_SCHEMA",
        silver_db="MY_SILVER_DB",
        silver_schema="MY_SILVER_SCHEMA"
    )

    # Create executor
    executor = GoldLayerExecutor(session, config)

    # Run all aggregations
    result = executor.run()

    # Or run specific aggregations
    result = executor.run(["dim_dates", "rms_fact_sustainability"])

    # Or run a single aggregation
    result = executor.run_single("fc_budget")

Using Individual Functions:
--------------------------

    from cpg_cdm_agg import dim_dates, rms_delivery_delay

    # Get your silver layer tables
    dim_date_df = session.table("SILVER_LAYER.MAPPED_DATA.dim_date")

    # Call the function
    result_df = dim_dates(dim_date_df)

    # Write to gold layer
    result_df.write.mode("overwrite").save_as_table("GOLD_LAYER.AGGREGATED_DATA.dim_dates")
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main classes
from .executor import (
    GoldLayerConfig,
    GoldLayerExecutor,
    run_all_aggregations,
    AGGREGATION_REGISTRY,
)

# Import all 31 aggregation functions
from .aggregations import (
    # Helper function
    write_to_gold_iceberg,
    
    # 1. Dimension Tables
    dim_dates,
    
    # 2-5. RMS (Raw Material Sourcing)
    rms_fact_sustainability,
    rms_delivery_delay,
    rms_procurement_lead_time,
    rms_grn_to_po,
    
    # 6-9. PM (Production Management)
    pm_scrap_and_raw,
    pm_plan_adherence,
    pm_downtime_per_shift_aggregated,
    pm_downtime_per_shift_oeee,
    
    # 10-15. DSC (Distribution & Supply Chain)
    dsc_cogs,
    dsc_inventory_days,
    dsc_damaged_return,
    dsc_transport_cost_per_unit,
    dsc_on_time_shipment_rate,
    dsc_inbound_delivery_accuracy,
    
    # 16-21. REUS (Retail & End User Sales)
    reus_customer_retention_monthly_totals,
    reus_customer_retention_monthly_retained,
    reus_customer_retention_monthly_new,
    reus_product_return_analysis,
    reus_average_order_value_analysis,
    reus_sales_per_outlet_analysis,
    
    # 22-27. CFM (Consumer & Field Marketing)
    cfm_conversion_rate,
    cfm_cost_per_conversion_spend,
    cfm_cost_per_conversion_engagement,
    cfm_survey_response_rate,
    cfm_customer_satisfaction_score,
    cfm_trade_promotion_effectiveness,
    
    # 28-30. FC (Finance & Controlling)
    fc_invoice_accuracy_analysis,
    fc_budget,
    fc_payment_timeliness_analysis,
    
    # 31. SESG (Sustainability & ESG)
    sesg_emission_production_analysis,
    
    # List of all function names
    ALL_AGGREGATION_FUNCTIONS,
)

# Define what's exported with "from package import *"
__all__ = [
    # Version info
    "__version__",
    
    # Main classes
    "GoldLayerConfig",
    "GoldLayerExecutor",
    "run_all_aggregations",
    "AGGREGATION_REGISTRY",
    
    # Helper function
    "write_to_gold_iceberg",
    
    # Dimension Tables (1)
    "dim_dates",
    
    # RMS functions (4)
    "rms_fact_sustainability",
    "rms_delivery_delay",
    "rms_procurement_lead_time",
    "rms_grn_to_po",
    
    # PM functions (4)
    "pm_scrap_and_raw",
    "pm_plan_adherence",
    "pm_downtime_per_shift_aggregated",
    "pm_downtime_per_shift_oeee",
    
    # DSC functions (6)
    "dsc_cogs",
    "dsc_inventory_days",
    "dsc_damaged_return",
    "dsc_transport_cost_per_unit",
    "dsc_on_time_shipment_rate",
    "dsc_inbound_delivery_accuracy",
    
    # REUS functions (6)
    "reus_customer_retention_monthly_totals",
    "reus_customer_retention_monthly_retained",
    "reus_customer_retention_monthly_new",
    "reus_product_return_analysis",
    "reus_average_order_value_analysis",
    "reus_sales_per_outlet_analysis",
    
    # CFM functions (6)
    "cfm_conversion_rate",
    "cfm_cost_per_conversion_spend",
    "cfm_cost_per_conversion_engagement",
    "cfm_survey_response_rate",
    "cfm_customer_satisfaction_score",
    "cfm_trade_promotion_effectiveness",
    
    # FC functions (3)
    "fc_invoice_accuracy_analysis",
    "fc_budget",
    "fc_payment_timeliness_analysis",
    
    # SESG functions (1)
    "sesg_emission_production_analysis",
    
    # List of all function names
    "ALL_AGGREGATION_FUNCTIONS",
]
