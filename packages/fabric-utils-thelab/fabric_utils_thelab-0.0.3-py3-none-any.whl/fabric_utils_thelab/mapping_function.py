import polars as pl
import datetime as dt
import json

#------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------
def build_operator(col, val, op):
    """ 
    Function to build out conditions based on provided operators
    """
    if op == 'in':  # if a column value needs to be equal to multiple values
        return pl.col(col).is_in(eval(val))
    
    elif op == '==':   # if a column value equals a single value
        if val.isdigit():
            return pl.col(col) == int(val)
        elif val == 'null':
            return pl.col(col).is_null()
        return pl.col(col) == val
    
    elif op == '!=':    # if a column value needs to be equal to multiple values
        if val.isdigit():
            return pl.col(col) != int(val)
        elif val == 'null':
            return pl.col(col).is_not_null()
        return pl.col(col) != val
    
    elif op == 'contains':
        return pl.col(col).str.contains(val)
    
    elif op == 'contains_any':
        return pl.col(col).str.contains_any(eval(val))
    
    elif op == '>':
        return pl.col(col) > int(val)
    
    elif op == '<':
        return pl.col(col) < int(val)
    
    elif op == '>=':
        return pl.col(col) >= int(val)
    
    elif op == '<=':
        return pl.col(col) <= int(val)

#------------------------------------------------------------------
# Function: parse_conditions()
#------------------------------------------------------------------
def parse_conditions(item: dict, type_map: str):
    """ 
    Take the input from json file and parse into Polar Expression to either
        1. Add indicator column
        2. Add classification column
    Input:
        column: Column name
        item: dictionary contains information needed to parse condition
    """

    expr = None
    for rule in item.get('logic'):
        
        # if type_map == 'replication':
        #     src_col = rule.get('conditions').get('src_column')
        #     return pl.col(src_col)
        
        label = rule.get('output')  # The output result for classification, return None for Indicator
        conditions = rule.get('conditions')  # Condition list
        cond_expr = [build_operator(c['column'], c['value'], c['operator']) for c in conditions]  # Loop through each condition and parse the appropriate operator
        join_op = rule.get('join')  # Get the join operator (either & or |)

        # Initialize combined condition
        init_cond = cond_expr[0]
        for join, next_cond in zip(join_op, cond_expr[1:]):

            if join != "":
                if join == '&':
                    init_cond &= next_cond 
                elif join == '|':
                    init_cond |= next_cond
            else:
                init_cond
       
        # Build condition branch base on rule type
        if type_map == 'classification':
            condition_branch = pl.when(init_cond).then(pl.lit(label))
            expr = condition_branch if expr is None else expr.when(init_cond).then(pl.lit(label))

        elif type_map == 'indicator':
            condition_branch = pl.when(init_cond).then(1)
            expr = condition_branch if expr is None else expr.when(init_cond).then(1)

    # Add fall back based on type
    if type_map == 'classification':
        expr = expr.otherwise(None)
    elif type_map == 'indicator':
        expr = expr.otherwise(0)

    return expr

#------------------------------------------------------------------
# Function: process_indicator_cols()
#------------------------------------------------------------------
def process_indicator_cols(std_data, json_mapping_file_name: str | dict, BASE_DIR='./builtin'):
    """ 
    Function to add indicator columns with parsed conditions from JSON mapping
    input: DataFrame having standardized column names
    """

    if isinstance(json_mapping_file_name, str):
        with open(f'{BASE_DIR}/put_std_mapping_here/{json_mapping_file_name}') as file:
            mapping_logic = json.load(file)
    elif isinstance(json_mapping_file_name, dict):
        mapping_logic = json_mapping_file_name

    init_data = std_data
    for column, item in mapping_logic.items():  
        type_map = item.get('type')

        # Get all columns required by this logic
        required_columns = set()
        for rule in item['logic']:
            for cond in rule['conditions']:
                required_columns.add(cond['column'])

        # Skip if any required column is missing
        missing_cols = [col for col in required_columns if col not in init_data.columns]
        if missing_cols:
            print(f"⚠️ Skipping '{column}' — missing columns: {missing_cols}")
            continue

        # Parse and apply logic
        try:
            output_expr = parse_conditions(item, type_map)
            init_data = init_data.with_columns(output_expr.alias(column))
            print(f"✅ Mapped: {column}")
        except Exception as e:
            print(f"❌ Failed on '{column}': {e}")

    return init_data