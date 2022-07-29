from typing import Optional, Tuple

import numpy as np
import pandas as pd
from marshmallow import Schema, ValidationError, fields


def validate_inputs(
    input_data: pd.DataFrame,
) -> Tuple[pd.DataFrame, Optional[dict]]:
    """
    Validate data input.

    Args:
        input_data: pandas DataFrame with data input.
    Returns:
        validated_data: pandas DataFrame with validated data input.
        errors: dict with schema errors.
    """
    validated_data = input_data.copy()

    schema = CustomerInputSchema(many=True)
    errors = None
    try:
        schema.load(validated_data.replace({np.nan: None}).to_dict(orient="records"))
    except ValidationError as error:
        errors = error.messages

    return validated_data, errors


class CustomerInputSchema(Schema):
    """Data input schema"""

    CLIENTNUM = fields.Integer()
    Attrition_Flag = fields.Str()
    Customer_Age = fields.Integer()
    Gender = fields.Str()
    Dependent_count = fields.Integer()
    Education_Level = fields.Str()
    Marital_Status = fields.Str()
    Income_Category = fields.Str()
    Card_Category = fields.Str()
    Months_on_book = fields.Integer()
    Total_Relationship_Count = fields.Integer()
    Months_Inactive_12_mon = fields.Integer()
    Contacts_Count_12_mon = fields.Integer()
    Credit_Limit = fields.Float()
    Total_Revolving_Bal = fields.Integer()
    Avg_Open_To_Buy = fields.Float()
    Total_Amt_Chng_Q4_Q1 = fields.Float()
    Total_Trans_Amt = fields.Integer()
    Total_Trans_Ct = fields.Integer()
    Total_Ct_Chng_Q4_Q1 = fields.Float()
    Avg_Utilization_Ratio = fields.Float()
