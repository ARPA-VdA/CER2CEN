from cer2cen.api import state, database, api
import pickle
import os.path
import os
import mariadb
import json
from dotenv import load_dotenv
load_dotenv()

# File to store application state
datastore = "data.pkl"

# Application credentials, loaded from environment variables
APP_PASSWORD = os.getenv("APP_PASSWORD")
APP_USERNAME = os.getenv("APP_USERNAME")
# Check if the 'SETTING_EDIT' environment variable is set (not None)
SETTING_EDIT = os.getenv("SETTING_EDIT") is not None

# Database connection credentials, loaded from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306)) # Convert DB_PORT to integer, defaulting to 3306 if not set
DB_DATABASE = os.getenv("DB_DATABASE")

# Print database connection details and whether editing is enabled
# print(f"DB_HOST: {DB_HOST}, DB_PORT: {DB_PORT}, DB_DATABASE: {DB_DATABASE}, SETTING_EDIT: {SETTING_EDIT}")

def get_state():
    """
    Loads the application state from a pickle file, if it exists. Otherwise, returns a new state object.
    
    Returns
    -------
    state.State
        The state object containing token and last primary key information.
    """
    s = state.State()
    
    if os.path.isfile(datastore):
        with open(datastore, 'rb') as file:
            s = pickle.load(file)
    return s
def save_state(s):
    """
    Saves the current application state to a pickle file.

    Parameters
    ----------
    s : state.State
        The state object to save.
    """
    with open(datastore, 'wb') as file:
        pickle.dump(s, file)

def load_tables():
    """
    Loads table mappings from a JSON file named 'tables.json'.

    Returns
    -------
    dict
        A dictionary mapping local table names to their upstream equivalents.
    """
    with open('tables.json', 'r') as file:
        return json.load(file)

def start():
    """
    Main function to begin the migration process. Connects to the database, retrieves new records, 
    and syncs them with the upstream system.
    
    Uses the current state to track the last migrated primary key for each table.
    """
    s = get_state()

    print(s.get_token(APP_USERNAME, APP_PASSWORD))
    try:
        connection = mariadb.connect(
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_DATABASE)
        
        tables = load_tables()
        # Iterate over each table and its corresponding upstream table
        for table, upstream in tables.items():
            print(table)
            last_id = s.get_last_pk(table)
            if SETTING_EDIT:
                print("Full editing enabled")
                last_id = 0
            # Fetch new records from the local database table where the primary key is greater than last_id
            res = database.get_new(connection, table, last_id)
            for x in res:
                res2 = api.add_row(s.get_token(APP_USERNAME, APP_PASSWORD), x, upstream, SETTING_EDIT)
                if res2:
                    new_pk = next(iter(x.values()))
                    s.update_last_pk(table, new_pk)
                else:
                    print("Error")
                    exit()
            print(f"Done Table {table}")

        connection.close()


    except mariadb.Error as err:
        print(f"An error occurred whilst connecting to MariaDB: {err}") 

    save_state(s)
