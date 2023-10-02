import faker
from random import randint

fake = faker.Faker()

# Generate SQL script for inserting categories
def generate_categories_script(num_categories):
    categories_script = []
    for _ in range(num_categories):
        name = fake.word()
        categories_script.append(f"('{name}')")
    return f"INSERT INTO categories (name) VALUES {', '.join(categories_script)};\n"

# Generate SQL script for inserting products
def generate_products_script(num_products, num_categories):
    products_script = []
    for _ in range(num_products):
        name = fake.name()
        description = fake.text()
        price = round(randint(10, 1000) + randint(0, 99) / 100, 2)
        category_id = randint(1, num_categories)
        products_script.append(f"('{name}', '{description}', {price}, {category_id})")
    return f"INSERT INTO products (name, description, price, category_id) VALUES {', '.join(products_script)};\n"

# Generate SQL script for inserting sales
def generate_sales_script(num_sales, num_products):
    sales_script = []
    for _ in range(num_sales):
        product_id = randint(1, num_products)
        sale_date = fake.date_time_between(start_date="-1y", end_date="now")
        quantity = randint(1, 100)
        sales_script.append(f"({product_id}, '{sale_date}', {quantity})")
    return f"INSERT INTO sales (product_id, sale_date, quantity) VALUES {', '.join(sales_script)};\n"

# Generate SQL script for inserting inventory
def generate_inventory_script(num_inventory, num_products):
    inventory_script = []
    for _ in range(num_inventory):
        product_id = randint(1, num_products)
        quantity = randint(1, 1000)
        low_stock_threshold = randint(1, 100)
        last_updated = fake.date_time_between(start_date="-1y", end_date="now")
        inventory_script.append(f"({product_id}, {quantity}, {low_stock_threshold}, '{last_updated}')")
    return f"INSERT INTO inventory (product_id, quantity, low_stock_threshold, last_updated) VALUES {', '.join(inventory_script)};\n"

# Generate SQL script for inserting users
def generate_users_script(num_users):
    users_script = []
    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password_hash = fake.password()
        users_script.append(f"('{username}', '{email}', '{password_hash}')")
    return f"INSERT INTO users (username, email, password_hash) VALUES {', '.join(users_script)};\n"

# Generate SQL script for inserting roles
def generate_roles_script(num_roles):
    roles_script = []
    for _ in range(num_roles):
        name = fake.word()
        roles_script.append(f"('{name}')")
    return f"INSERT INTO roles (name) VALUES {', '.join(roles_script)};\n"

if __name__ == "__main__":
    num_categories = 10  # Specify the number of categories
    num_products = 100  # Specify the number of products
    num_sales = 1000  # Specify the number of sales
    num_inventory = 500  # Specify the number of inventory records
    num_users = 50  # Specify the number of users
    num_roles = 3  # Specify the number of roles

    sql_script = ""
    sql_script += generate_categories_script(num_categories)
    sql_script += generate_products_script(num_products, num_categories)
    sql_script += generate_sales_script(num_sales, num_products)
    sql_script += generate_inventory_script(num_inventory, num_products)
    sql_script += generate_users_script(num_users)
    sql_script += generate_roles_script(num_roles)

    with open("insert_data.sql", "w") as f:
        f.write(sql_script)
