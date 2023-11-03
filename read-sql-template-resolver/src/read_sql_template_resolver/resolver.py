
from jinja2 import Environment, FileSystemLoader
environment = Environment(loader=FileSystemLoader("sql/"))


def read_sql_template(filename, table_name):
    template = environment.get_template(filename)
    print(f"{filename=}")
    print(f"{table_name=}")
    return template.render(table_name = table_name)