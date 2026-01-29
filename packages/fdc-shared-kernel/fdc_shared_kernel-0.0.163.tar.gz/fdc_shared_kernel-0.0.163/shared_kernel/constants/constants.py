def get_constant(section: str, key: str) -> str:
    if section == "mssql":
        if key == "CONNECTION_STRING":
            return "mssql+pyodbc://{}:{}@{}:{}/{}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    elif section == "postgres":
        if key == "CONNECTION_STRING":
            return "postgresql+psycopg2://{}:{}@{}:{}/{}"
    elif section == "mysql":
        if key == "CONNECTION_STRING":
            return "mysql+pymysql://{}:{}@{}:{}/{}"
    elif section == "redshift":
        if key == "OID_MAP":
            return {
                16: "BOOLEAN",
                20: "BIGINT",
                21: "SMALLINT",
                23: "INTEGER",
                25: "VARCHAR",
                700: "REAL",
                701: "DOUBLE",
                1043: "VARCHAR",
                1082: "DATE",
                1114: "TIMESTAMP",
                1184: "TIMESTAMPTZ",
                1700: "NUMERIC",
            }
    elif section == "sqlalchemy":
        if key == "DTYPE_MAP":
            return {
                0: "decimal",
                1: "integer",
                2: "integer",
                3: "integer",
                4: "double",
                5: "double",
                7: "timestamp",
                8: "integer",
                9: "integer",
                10: "date",
                11: "time",
                12: "timestamp",
                13: "year",
                15: "string",
                16: "boolean",
                246: "numeric",
                252: "string",
                253: "string",
                254: "string",
            }
    return ""
