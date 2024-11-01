from prettytable import PrettyTable

def print_table(fields, rows):
    table = PrettyTable()
    table.field_names = fields

    for row in rows:
        table.add_row(row)
    # print(len(table.rows))
    print(f"\n\n{table}")  # Print the table

    return 0