COMMON_RULES = """
Avoid repetition.
If the field is a table, identify the headers and the rows.
If the field is found in multiple places with different values, the value should be a list under the same field name.
Avoid creating tables with only one column/header - that's a list data type, not a table.
Respect the action options available to you and their description under <actions>.
Also include a confidence score for each field, from 0 to 1.
You should return a list of FieldResponse objects.
"""

EXTRACTION_RULES = (
    """
The field names MUST be unique so we can properly identify the fields and avoid repetition. 
The field names should be human readable and descriptive, so don't use software notation like "contract_number" or "ContractNumber" but rather "Contract Number".
"""
    + COMMON_RULES
)

STRICT_EXTRACTION_RULES = (
    """
The field names MUST be unique so we can properly identify the fields and avoid repetition.
You MUST use the exact field names provided in the <requested_fields>. Do not rename them or make them "human readable".
You MUST NOT extract any fields that are not explicitly listed in <requested_fields>.
You MUST NOT create any new entities that are not found in <requested_fields>.
"""
    + COMMON_RULES
)

FIND_FIELDS_SYSTEM_PROMPT = (
    """
Identify the relevant fields and it's values from the <content>.
"""
    + EXTRACTION_RULES
)

FIND_AND_USE_REQUESTED_FIELDS_SYSTEM_PROMPT = (
    """
Identify the relevant fields and it's values from the <content>.
Use the requested fields under <requested_fields> but also identify any additional fields that are not in the <requested_fields>.
"""
    + EXTRACTION_RULES
)

STRICT_FIELDS_SYSTEM_PROMPT = (
    """
Extract the field values from the <content>, given the set of requested fields under <requested_fields>. 
Do not find any additional fields that are not in the <requested_fields>.
"""
    + STRICT_EXTRACTION_RULES
)

USER_PROMPT_TEMPLATE = """
<actions>You have a few "action" options to choose from: {actions}</actions>
<extracted_fields>{extracted_fields}</extracted_fields>
<content>{text}</content>
"""

USER_PROMPT_WITH_REQUESTED_FIELDS_TEMPLATE = (
    """
<fields_to_extract>{requested_fields}</fields_to_extract>
"""
    + USER_PROMPT_TEMPLATE
)

FIELD_TO_EXTRACT_TEMPLATE = """
<field_to_extract name="{name}" entity="{entity}" data_type="{data_type}" description="{description}" example="{example}" />
"""

EXTRACTED_FIELD_TEMPLATE = """
<extracted_field name="{name}" data_type="{data_type}" description="{description}">{value}</extracted_field>
"""
