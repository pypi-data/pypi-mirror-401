"""
Executor module for running Gold Layer aggregations.

This module provides a flexible way to execute individual or multiple
aggregation functions and write results to Snowflake Gold layer tables.
"""

from typing import List, Optional, Dict, Any, Callable
from snowflake.snowpark import Session

from .aggregations import (
    write_to_gold_iceberg,
    dim_dates,
    rms_fact_sustainability,
    rms_delivery_delay,
    rms_procurement_lead_time,
    rms_grn_to_po,
    pm_scrap_and_raw,
    pm_plan_adherence,
    pm_downtime_per_shift_aggregated,
    pm_downtime_per_shift_oeee,
    dsc_cogs,
    dsc_inventory_days,
    dsc_damaged_return,
    dsc_transport_cost_per_unit,
    dsc_on_time_shipment_rate,
    dsc_inbound_delivery_accuracy,
    reus_customer_retention_monthly_totals,
    reus_customer_retention_monthly_retained,
    reus_customer_retention_monthly_new,
    reus_product_return_analysis,
    reus_average_order_value_analysis,
    reus_sales_per_outlet_analysis,
    cfm_conversion_rate,
    cfm_cost_per_conversion_spend,
    cfm_cost_per_conversion_engagement,
    cfm_survey_response_rate,
    cfm_customer_satisfaction_score,
    cfm_trade_promotion_effectiveness,
    fc_invoice_accuracy_analysis,
    fc_budget,
    fc_payment_timeliness_analysis,
    sesg_emission_production_analysis,
    ALL_AGGREGATION_FUNCTIONS,
)


class GoldLayerConfig:
    """
    Configuration class for Gold Layer aggregations.
    
    Attributes:
        gold_db: Name of the Gold layer database
        gold_schema: Name of the Gold layer schema
        silver_db: Name of the Silver layer database
        silver_schema: Name of the Silver layer schema
    """
    
    def __init__(
        self,
        gold_db: str = "GOLD_LAYER",
        gold_schema: str = "AGGREGATED_DATA",
        silver_db: str = "SILVER_LAYER",
        silver_schema: str = "MAPPED_DATA"
    ):
        """
        Initialize the configuration.
        
        Args:
            gold_db: Gold layer database name (default: "GOLD_LAYER")
            gold_schema: Gold layer schema name (default: "AGGREGATED_DATA")
            silver_db: Silver layer database name (default: "SILVER_LAYER")
            silver_schema: Silver layer schema name (default: "MAPPED_DATA")
        """
        self.gold_db = gold_db
        self.gold_schema = gold_schema
        self.silver_db = silver_db
        self.silver_schema = silver_schema


# ============================================
# AGGREGATION REGISTRY
# ============================================

# Map of function names to their configurations
AGGREGATION_REGISTRY: Dict[str, Dict[str, Any]] = {
    "dim_dates": {
        "function": dim_dates,
        "tables": ["dim_date"],
        "output_table": "dim_dates",
    },
    "rms_fact_sustainability": {
        "function": rms_fact_sustainability,
        "tables": ["dim_supplier_master"],
        "output_table": "rms_fact_sustainability",
    },
    "rms_delivery_delay": {
        "function": rms_delivery_delay,
        "tables": [
            "fact_goods_receipt",
            "fact_purchase_order_line",
            "fact_purchase_order_header",
            "dim_supplier_master",
            "dim_material_master",
            "dim_product_master",
        ],
        "output_table": "rms_delivery_delay",
    },
    "rms_procurement_lead_time": {
        "function": rms_procurement_lead_time,
        "tables": [
            "fact_goods_receipt",
            "fact_purchase_order_line",
            "fact_purchase_order_header",
            "dim_supplier_master",
            "dim_material_master",
            "dim_product_master",
        ],
        "output_table": "rms_procurement_lead_time",
    },
    "rms_grn_to_po": {
        "function": rms_grn_to_po,
        "tables": [
            "fact_goods_receipt",
            "fact_purchase_order_line",
            "fact_purchase_order_header",
            "dim_supplier_master",
            "dim_product_master",
            "dim_material_master",
        ],
        "output_table": "rms_grn_to_po",
    },
    "pm_scrap_and_raw": {
        "function": pm_scrap_and_raw,
        "tables": [
            "fact_production_batch",
            "fact_shift_log",
            "dim_production_line",
            "dim_facility_master",
        ],
        "output_table": "pm_scrap_and_raw",
    },
    "pm_plan_adherence": {
        "function": pm_plan_adherence,
        "tables": [
            "fact_production_schedule_line",
            "fact_production_schedule_header",
            "dim_production_line",
            "dim_facility_master",
        ],
        "output_table": "pm_plan_adherence",
    },
    "pm_downtime_per_shift_aggregated": {
        "function": pm_downtime_per_shift_aggregated,
        "tables": [
            "fact_line_efficiency_log",
            "fact_shift_log",
            "fact_equipment_downtime_log",
            "dim_production_line",
            "dim_facility_master",
        ],
        "output_table": "pm_downtime_per_shift_aggregated",
    },
    "pm_downtime_per_shift_oeee": {
        "function": pm_downtime_per_shift_oeee,
        "tables": [
            "fact_line_efficiency_log",
            "fact_shift_log",
            "dim_production_line",
            "dim_facility_master",
        ],
        "output_table": "pm_downtime_per_shift_oeee",
    },
    "dsc_cogs": {
        "function": dsc_cogs,
        "tables": [
            "fact_product_inventory",
            "dim_warehouse_master",
            "dim_product_master",
            "fact_sales_order_line",
        ],
        "output_table": "dsc_cogs",
    },
    "dsc_inventory_days": {
        "function": dsc_inventory_days,
        "tables": [
            "fact_product_inventory",
            "dim_warehouse_master",
            "dim_product_master",
            "fact_sales_order_line",
        ],
        "output_table": "dsc_inventory_days",
    },
    "dsc_damaged_return": {
        "function": dsc_damaged_return,
        "tables": [
            "fact_outbound_shipment",
            "dim_carrier_master",
            "fact_shipment_line",
            "fact_return_order",
            "fact_purchase_order_line",
            "fact_purchase_order_header",
            "dim_supplier_master",
        ],
        "output_table": "dsc_damaged_return",
    },
    "dsc_transport_cost_per_unit": {
        "function": dsc_transport_cost_per_unit,
        "tables": [
            "fact_transportation_cost",
            "dim_carrier_master",
            "dim_truck_route",
            "fact_outbound_shipment",
        ],
        "output_table": "dsc_transport_cost_per_unit",
    },
    "dsc_on_time_shipment_rate": {
        "function": dsc_on_time_shipment_rate,
        "tables": [
            "fact_outbound_shipment",
            "dim_carrier_master",
            "dim_distribution_center",
        ],
        "output_table": "dsc_on_time_shipment_rate",
    },
    "dsc_inbound_delivery_accuracy": {
        "function": dsc_inbound_delivery_accuracy,
        "tables": [
            "fact_inbound_shipment",
            "dim_supplier_master",
            "dim_warehouse_master",
        ],
        "output_table": "dsc_inbound_delivery_accuracy",
    },
    "reus_customer_retention_monthly_totals": {
        "function": reus_customer_retention_monthly_totals,
        "tables": [
            "fact_sales_order",
            "fact_customer_visit",
        ],
        "output_table": "reus_customer_retention_monthly_totals",
    },
    "reus_customer_retention_monthly_retained": {
        "function": reus_customer_retention_monthly_retained,
        "tables": [
            "fact_sales_order",
            "fact_customer_visit",
        ],
        "output_table": "reus_customer_retention_monthly_retained",
    },
    "reus_customer_retention_monthly_new": {
        "function": reus_customer_retention_monthly_new,
        "tables": [
            "fact_sales_order",
            "fact_customer_visit",
        ],
        "output_table": "reus_customer_retention_monthly_new",
    },
    "reus_product_return_analysis": {
        "function": reus_product_return_analysis,
        "tables": [
            "fact_return_order",
            "fact_sales_order",
            "dim_channel",
            "dim_product_master",
            "dim_material_category",
        ],
        "output_table": "reus_product_return_analysis",
    },
    "reus_average_order_value_analysis": {
        "function": reus_average_order_value_analysis,
        "tables": [
            "fact_sales_order",
            "dim_retail_outlet",
            "dim_customer_master",
            "dim_region_hierarchy",
        ],
        "output_table": "reus_average_order_value_analysis",
    },
    "reus_sales_per_outlet_analysis": {
        "function": reus_sales_per_outlet_analysis,
        "tables": [
            "fact_sales_order",
            "dim_retail_outlet",
            "dim_region_hierarchy",
        ],
        "output_table": "reus_sales_per_outlet_analysis",
    },
    "cfm_conversion_rate": {
        "function": cfm_conversion_rate,
        "tables": ["fact_ad_impression"],
        "output_table": "cfm_conversion_rate",
    },
    "cfm_cost_per_conversion_spend": {
        "function": cfm_cost_per_conversion_spend,
        "tables": [
            "fact_marketing_spend",
            "fact_ad_impression",
            "dim_campaign_master",
        ],
        "output_table": "cfm_cost_per_conversion_spend",
    },
    "cfm_cost_per_conversion_engagement": {
        "function": cfm_cost_per_conversion_engagement,
        "tables": [
            "fact_ad_impression",
            "dim_campaign_master",
        ],
        "output_table": "cfm_cost_per_conversion_engagement",
    },
    "cfm_survey_response_rate": {
        "function": cfm_survey_response_rate,
        "tables": ["fact_consumer_survey"],
        "output_table": "cfm_survey_response_rate",
    },
    "cfm_customer_satisfaction_score": {
        "function": cfm_customer_satisfaction_score,
        "tables": [
            "fact_consumer_survey",
            "dim_product_master",
            "dim_material_category",
        ],
        "output_table": "cfm_customer_satisfaction_score",
    },
    "cfm_trade_promotion_effectiveness": {
        "function": cfm_trade_promotion_effectiveness,
        "tables": [
            "fact_promotion_plan",
            "dim_promotion_master",
            "dim_channel",
            "fact_trade_promotion",
        ],
        "output_table": "cfm_trade_promotion_effectiveness",
    },
    "fc_invoice_accuracy_analysis": {
        "function": fc_invoice_accuracy_analysis,
        "tables": [
            "fact_invoice",
            "fact_payment",
        ],
        "output_table": "fc_invoice_accuracy_analysis",
    },
    "fc_budget": {
        "function": fc_budget,
        "tables": [
            "dim_account_master",
            "fact_budget",
            "fact_general_ledger",
        ],
        "output_table": "fc_budget",
    },
    "fc_payment_timeliness_analysis": {
        "function": fc_payment_timeliness_analysis,
        "tables": [
            "fact_payment",
            "fact_invoice",
        ],
        "output_table": "fc_payment_timeliness_analysis",
    },
    "sesg_emission_production_analysis": {
        "function": sesg_emission_production_analysis,
        "tables": [
            "fact_emission_record",
            "fact_production_batch",
        ],
        "output_table": "sesg_emission_production_analysis",
    },
}


class GoldLayerExecutor:
    """
    Executor class for running Gold Layer aggregations.
    
    This class provides methods to run individual, multiple, or all
    aggregation functions and write results to Snowflake Gold layer tables.
    """
    
    def __init__(self, session: Session, config: Optional[GoldLayerConfig] = None):
        """
        Initialize the executor.
        
        Args:
            session: Snowpark Session object
            config: Optional GoldLayerConfig object. If not provided, defaults are used.
        """
        self.session = session
        self.config = config or GoldLayerConfig()
    
    def _get_table(self, table_name: str):
        """
        Get a table from the Silver layer.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Snowpark DataFrame
        """
        full_name = f"{self.config.silver_db}.{self.config.silver_schema}.{table_name}"
        return self.session.table(full_name)
    
    def _execute_aggregation(self, agg_name: str) -> Dict[str, Any]:
        """
        Execute a single aggregation function.
        
        Args:
            agg_name: Name of the aggregation function
            
        Returns:
            Dict with status, row count, and any error message
        """
        if agg_name not in AGGREGATION_REGISTRY:
            return {
                "name": agg_name,
                "status": "error",
                "message": f"Unknown aggregation: {agg_name}",
                "rows": 0,
            }
        
        registry_entry = AGGREGATION_REGISTRY[agg_name]
        func = registry_entry["function"]
        tables = registry_entry["tables"]
        output_table = registry_entry["output_table"]
        
        try:
            # Load all required tables
            table_dfs = [self._get_table(t) for t in tables]
            
            # Execute the aggregation function
            result_df = func(*table_dfs)
            
            # Write to Gold layer
            row_count = write_to_gold_iceberg(
                result_df,
                output_table,
                self.config.gold_db,
                self.config.gold_schema
            )
            
            return {
                "name": agg_name,
                "status": "success",
                "message": f"Created {output_table}",
                "rows": row_count,
            }
        except Exception as e:
            return {
                "name": agg_name,
                "status": "error",
                "message": str(e),
                "rows": 0,
            }
    
    def run(self, aggregations: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Run specified aggregations or all aggregations if none specified.
        
        Args:
            aggregations: List of aggregation function names to run.
                         If None, runs all 31 aggregations.
        
        Returns:
            Dict with summary of results including successes and errors
        
        Example:
            # Run all aggregations
            result = executor.run()
            
            # Run specific aggregations
            result = executor.run(["dim_dates", "rms_fact_sustainability"])
            
            # Run a single aggregation
            result = executor.run(["fc_budget"])
        """
        if aggregations is None:
            aggregations = ALL_AGGREGATION_FUNCTIONS
        
        results = []
        errors = []
        
        for agg_name in aggregations:
            result = self._execute_aggregation(agg_name)
            if result["status"] == "success":
                results.append(result)
            else:
                errors.append(result)
        
        return {
            "total": len(aggregations),
            "successful": len(results),
            "failed": len(errors),
            "results": results,
            "errors": errors,
        }
    
    def run_single(self, aggregation_name: str) -> Dict[str, Any]:
        """
        Run a single aggregation by name.
        
        Args:
            aggregation_name: Name of the aggregation function to run
        
        Returns:
            Dict with status, row count, and any error message
        
        Example:
            result = executor.run_single("dim_dates")
        """
        return self._execute_aggregation(aggregation_name)
    
    def get_available_aggregations(self) -> List[str]:
        """
        Get list of all available aggregation function names.
        
        Returns:
            List of aggregation function names
        """
        return ALL_AGGREGATION_FUNCTIONS.copy()
    
    def get_aggregation_info(self, aggregation_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific aggregation.
        
        Args:
            aggregation_name: Name of the aggregation function
        
        Returns:
            Dict with function info, or None if not found
        """
        if aggregation_name not in AGGREGATION_REGISTRY:
            return None
        
        entry = AGGREGATION_REGISTRY[aggregation_name]
        return {
            "name": aggregation_name,
            "required_tables": entry["tables"],
            "output_table": entry["output_table"],
        }


def run_all_aggregations(
    session: Session,
    gold_db: str = "GOLD_LAYER",
    gold_schema: str = "AGGREGATED_DATA",
    silver_db: str = "SILVER_LAYER",
    silver_schema: str = "MAPPED_DATA"
) -> str:
    """
    Convenience function to run all 31 aggregations.
    
    This function can be used directly in a Snowflake stored procedure.
    
    Args:
        session: Snowpark Session object
        gold_db: Gold layer database name
        gold_schema: Gold layer schema name
        silver_db: Silver layer database name
        silver_schema: Silver layer schema name
    
    Returns:
        Summary string of the execution results
    """
    config = GoldLayerConfig(
        gold_db=gold_db,
        gold_schema=gold_schema,
        silver_db=silver_db,
        silver_schema=silver_schema
    )
    
    executor = GoldLayerExecutor(session, config)
    results = executor.run()
    
    # Build summary string
    summary = "\n" + "=" * 70 + "\n"
    summary += "GOLD LAYER AGGREGATION SUMMARY - 31 FUNCTIONS\n"
    summary += "=" * 70 + "\n"
    summary += f"Successfully created: {results['successful']} Iceberg tables\n"
    summary += f"Errors: {results['failed']}\n\n"
    
    if results["results"]:
        summary += "SUCCESSFULLY CREATED ICEBERG TABLES:\n"
        summary += "-" * 40 + "\n"
        for r in results["results"]:
            summary += f"  ✓ {r['name']} ({r['rows']} rows)\n"
        summary += "\n"
    
    if results["errors"]:
        summary += "ERRORS:\n"
        summary += "-" * 40 + "\n"
        for e in results["errors"]:
            summary += f"  ✗ {e['name']}: {e['message']}\n"
    
    summary += "=" * 70
    
    return summary
