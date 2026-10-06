import pandas as pd


def analyze_dataset(dataframe, question):

    question_lower = question.lower()

    # Average / Mean
    if "average" in question_lower or "mean" in question_lower:

        for column in dataframe.select_dtypes(include="number").columns:

            if column.lower() in question_lower:

                value = dataframe[column].mean()

                return {
                    "type": "calculation",
                    "operation": "mean",
                    "column": column,
                    "value": round(float(value), 2)
                }

    # Maximum
    if (
        "maximum" in question_lower
        or "highest" in question_lower
        or "max" in question_lower
    ):

        for column in dataframe.select_dtypes(include="number").columns:

            if column.lower() in question_lower:

                value = dataframe[column].max()

                return {
                    "type": "calculation",
                    "operation": "maximum",
                    "column": column,
                    "value": round(float(value), 2)
                }

    # Minimum
    if (
        "minimum" in question_lower
        or "lowest" in question_lower
        or "min" in question_lower
    ):

        for column in dataframe.select_dtypes(include="number").columns:

            if column.lower() in question_lower:

                value = dataframe[column].min()

                return {
                    "type": "calculation",
                    "operation": "minimum",
                    "column": column,
                    "value": round(float(value), 2)
                }

    # Missing values
    if "missing" in question_lower or "null" in question_lower:

        missing_values = dataframe.isnull().sum()

        return {
            "type": "missing_values",
            "values": missing_values.to_dict()
        }

    # Faulty sensors
    if (
        "faulty" in question_lower
        or "fault" in question_lower
        or "failed" in question_lower
    ):

        fault_column = None

        for column in dataframe.columns:

            if column.lower() == "faultflag":
                fault_column = column
                break

        if fault_column:

            faulty_count = (
                dataframe[fault_column] == 1
            ).sum()

            total_count = len(dataframe)

            fault_percentage = (
                faulty_count / total_count
            ) * 100

            return {
                "type": "fault_analysis",
                "faulty_sensors": int(faulty_count),
                "total_records": int(total_count),
                "fault_percentage": round(
                    float(fault_percentage), 2
                )
            }

    # Dataset rows
    if (
        "how many rows" in question_lower
        or "number of rows" in question_lower
        or "how many records" in question_lower
        or "number of records" in question_lower
    ):

        return {
            "type": "dataset_size",
            "rows": int(len(dataframe))
        }

    # Dataset columns
    if (
        "how many columns" in question_lower
        or "number of columns" in question_lower
    ):

        return {
            "type": "dataset_size",
            "columns": int(len(dataframe.columns))
        }

    # Column names
    if (
        "what columns" in question_lower
        or "which columns" in question_lower
        or "column names" in question_lower
    ):

        return {
            "type": "column_information",
            "columns": list(dataframe.columns)
        }

    # Correlation
    if "correlation" in question_lower:

        numeric_columns = list(
            dataframe.select_dtypes(include="number").columns
        )

        found_columns = []

        for column in numeric_columns:

            if column.lower() in question_lower:
                found_columns.append(column)

        if len(found_columns) >= 2:

            column_1 = found_columns[0]
            column_2 = found_columns[1]

            correlation = dataframe[
                [column_1, column_2]
            ].corr().iloc[0, 1]

            return {
                "type": "correlation",
                "column_1": column_1,
                "column_2": column_2,
                "correlation": round(
                    float(correlation), 3
                )
            }

        # If specific columns weren't identified,
        # return the complete correlation matrix.
        correlation_matrix = dataframe[
            numeric_columns
        ].corr()

        return {
            "type": "correlation_matrix",
            "values": correlation_matrix.round(3).to_dict()
        }

    return None