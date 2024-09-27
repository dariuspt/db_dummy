import os  # Import the os module to access environment variables
import cloudinary
from dotenv import load_dotenv

load_dotenv()

# Load environment variables or use default values if they are not set.
# The os.getenv() function is used to retrieve the value of an environment variable.

# Database configuration
DB_USER = os.getenv("DB_USER", "u7paluhujo6p51")
DB_PASS = os.getenv("DB_PASS", "p1af0cc57920fcbf1b38a54f2f9404d5c8fe1269cf1e38e7b39a5b09c4876352a")
DB_HOST = os.getenv("DB_HOST", "cf980tnnkgv1bp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com")
DB_NAME = os.getenv("DB_NAME", "d9t3vfbpdctolc")
DB_PORT = os.getenv("DB_PORT", 5432)

# Construct the database URL in the format required by most database clients.
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Print a confirmation message to indicate that the database URL has been configured successfully.
print("Database URL configured successfully.")

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "di74te31t"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "257749951329451"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "nHQ8-0JoCuCo3dmw2ChclzEcMXQ")
)

# Print confirmation for Cloudinary configuration
print("Cloudinary configured successfully.")
