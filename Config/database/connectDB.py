import configparser
from pymongo import MongoClient

def get_db_connection():
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read('DB_Config.ini')

    # Ensure 'DATABASE' section exists
    if 'DATABASE' not in config:
        print("Error: 'DATABASE' section not found in DB_Config.ini")
        return None

    mongo_uri = config['DATABASE'].get('MONGO_URI', '').strip()
    db_name = config['DATABASE'].get('DB_NAME', '').strip()

    if not mongo_uri or not db_name:
        print("Error: Missing MONGO_URI or DB_NAME in DB_Config.ini")
        return None

    try:
        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        print("Connected to MongoDB successfully")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None


if __name__ == "__main__":
    get_db_connection()