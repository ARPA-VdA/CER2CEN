import datetime

from cer2cen.api import api

# Token expiration time set to 5 minutes. This defines how long a token is considered valid after its creation.
token_expire_min = 5

class State:
    """
    A class used to manage token states and primary key tracking for tables.
    
    Attributes:
    ----------
    token : dict
        A dictionary holding token information including creation time and JWT.
    last_pk : dict
        A dictionary tracking the last primary key for different tables.

    Methods:
    -------
    get_last_pk(tablename):
        Returns the last primary key used for a specific table.
    update_last_pk(tablename, new_pk):
        Updates the last primary key for a table if the new one is higher.
    put_token(token):
        Stores a token and the time it was created.
    need_refresh():
        Checks if the token needs to be refreshed based on expiration time.
    get_token(username, password):
        Returns a JWT token, refreshing it if expired.
    """

    def __init__(self):
        """
        Initializes the State class with an empty token and last_pk dictionaries.
        """
        self.token = {} #creation and jwt
        self.last_pk = {}

    def get_last_pk(self, tablename):
        """
        Retrieves the last primary key used for a specific table.
        
        This helps to track the last migrated value for the table to ensure no data is processed twice.

        Parameters:
        ----------
        tablename : str
            The name of the table for which the primary key is being requested.

        Returns:
        -------
        int
            The last primary key value or 0 if no key exists for the table.
        """
        ans = self.last_pk.get(tablename)
        if ans == None:
            return 0
        else:
            return ans
        
    def update_last_pk(self, tablename, new_pk):
        """
        Updates the last primary key for the given table if the new primary key is greater
        than the current one.

        This helps to track the last migrated value for the table to ensure no data is processed twice.
        
        Parameters
        ----------
        tablename : str
            The name of the table for which the primary key is being updated.
        new_pk : int
            The new primary key value that will be compared with the current value.

        Returns
        -------
        None
        """
        old = self.get_last_pk(tablename)
        if new_pk > old:
            self.last_pk[tablename] = new_pk

    def put_token(self, token):
        """
        Stores the token in the token dictionary and records the current time as the 
        token creation time.

        Parameters
        ----------
        token : dict
            A dictionary containing token information. It is expected to have a key "JWT"
            for the actual token string.

        Returns
        -------
        None
        """
        self.token["creation"] = datetime.datetime.now()
        self.token["jwt"] = token["JWT"]

    def need_refresh(self):
        """
        Determines if the token needs to be refreshed by checking if the time since 
        creation has exceeded the predefined expiration limit.

        Returns
        -------
        bool
            True if the token needs to be refreshed, False if the token is still valid.
        """
        if self.token != {}:
            current_time = datetime.datetime.now()

            token_creation = self.token["creation"]

            elapsed = current_time - token_creation
            if (elapsed.total_seconds() / 60) > token_expire_min :
                print(f"Token expired. Refreshing now. Elapsed time: {elapsed}.")
                return True
            else:
                return False
        else:
            print("No token found. Requesting a new token.")
            return True


    def get_token(self, username, password):
        """
        Retrieves the JWT token for the session. If the token has expired or does not exist, 
        it will refresh the token by requesting a new one from the API.

        Parameters
        ----------
        username : str
            The username to authenticate with the API.
        password : str
            The password to authenticate with the API.

        Returns
        -------
        str
            The JWT token string used for authentication.
        """
        if self.need_refresh(): # Check if the token needs to be refreshed
            # Call the API to get a new token and store it
            self.put_token(api.getToken(username, password))
        return self.token["jwt"]