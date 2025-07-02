import sqlparse

def format_sql(raw_sql: str) -> str:
    """
    Formats SQL with proper indentation and uppercase keywords.
    """
    return sqlparse.format(raw_sql, reindent=True, keyword_case='upper')
