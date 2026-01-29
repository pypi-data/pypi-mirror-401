sqlalchemy_to_system = {
    # ---------- Integer types ----------
    "INTEGER": "integer",
    "INT": "integer",
    "SMALLINT": "integer",
    "BIGINT": "integer",

    # ---------- Floating / numeric ----------
    "FLOAT": "double",
    "REAL": "real",
    "DOUBLE": "double",
    "DOUBLE_PRECISION": "double",
    "NUMERIC": "numeric",
    "DECIMAL": "numeric",

    # ---------- String / text ----------
    "VARCHAR": "string",
    "CHAR": "string",
    "NCHAR": "string",
    "NVARCHAR": "string",
    "TEXT": "string",
    "CLOB": "string",

    # ---------- Boolean ----------
    "BOOLEAN": "boolean",

    # ---------- Temporal ----------
    "DATE": "date",
    "TIME": "timestamp",
    "DATETIME": "timestamp",
    "TIMESTAMP": "timestamp",

    # ---------- Binary ----------
    "BINARY": "binary",
    "VARBINARY": "binary",
    "BLOB": "binary",

    # ---------- JSON / semi-structured ----------
    "JSON": "json",

    # ---------- UUID ----------
    "UUID": "string",

    # ---------- Fallback ----------
    "NULLTYPE": "null",
}
