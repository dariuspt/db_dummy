import os  # Import the os module to access environment variables

# Load environment variables or use default values if they are not set.
# The os.getenv() function is used to retrieve the value of an environment variable.

# Database username. Default is 'postgres' if the DB_USER environment variable is not set.
DB_USER = os.getenv("DB_USER", "u7paluhujo6p51")

# Database password. Default is 'Noch%40nge12' if the DB_PASS environment variable is not set.
# The password is URL-encoded (%40 represents '@').
DB_PASS = os.getenv("DB_PASS", "p1af0cc57920fcbf1b38a54f2f9404d5c8fe1269cf1e38e7b39a5b09c4876352a")

# Database host. Default is 'localhost' if the DB_HOST environment variable is not set.
DB_HOST = os.getenv("DB_HOST", "cf980tnnkgv1bp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com")

# Database name. Default is 'products_db' if the DB_NAME environment variable is not set.
DB_NAME = os.getenv("DB_NAME", "d9t3vfbpdctolc")

# Database port. Default is 5432 (the default port for PostgreSQL) if the DB_PORT environment variable is not set.
DB_PORT = os.getenv("DB_PORT", 5432)

# Construct the database URL in the format required by most database clients.
# This URL includes the database type (postgresql), user, password, host, port, and database name.
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Print a confirmation message to indicate that the database URL has been configured successfully.
print("Database URL configured successfully.")
