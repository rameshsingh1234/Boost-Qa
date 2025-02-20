from dotenv import load_dotenv

# Load environment variables from a .env file located in the same directory as this script
load_dotenv()

import os
print("Current ENV setting:", os.getenv('ENV'))
