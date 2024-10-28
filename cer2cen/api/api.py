import requests
import json
#id_utente = 02 (VALLE D'AOSTA)
BASE_URL = "https://agentifisici.isprambiente.it/cen_uni/api/"
ID_UTENTE = 2

def is_success(res):
    """
    Checks if the response from the API is successful by evaluating the status code
    and the 'success' field in the JSON response.

    Parameters
    ----------
    res : Response
        The HTTP response object received from the API.

    Returns
    -------
    bool
        True if the response status is 200 and the 'success' field is True, False otherwise.
    """
    if(res.status_code == 200):
        print(res.text)
        parsed_response = json.loads(res.text)
        print(parsed_response)
        if parsed_response["success"] == True:
            return True
    return False

def get_row(token, upstream_table, row):
    """
    Fetches a specific row from the upstream table based on the primary key value.

    This function constructs a GET request to retrieve a record from the specified table 
    using the primary key extracted from the row dictionary.

    Parameters
    ----------
    token : str
        The JWT token used for authorization in the API request.
    upstream_table : str
        The name of the table from which the row is being requested.
    row : dict
        A dictionary containing the row data. The primary key value is extracted from this dictionary.

    Returns
    -------
    Response
        The response object returned from the API.
    """
    match upstream_table:
        # Special handling for the "elf_tbl_sost_aerei" table, using FK_SOSTEGNO as primary key
        case "elf_tbl_sost_aerei":
            pk_name = "FK_SOSTEGNO"
            pk_value = row["FK_SOSTEGNO"]
        # Default case for other tables, extracting the first key-value pair as primary key
        case _:
            local_pk = next(iter(row.items()))
            pk_name, pk_value = local_pk

    request_string = f"?action=view&object={upstream_table}&{pk_name}={pk_value}&id_utente={ID_UTENTE}"

    print(request_string)
    r = requests.get(BASE_URL + request_string, headers={"Authorization": f"Bearer {token}"})
    return r

def record_exists(token, upstream_table, row):
    """
    Checks if a specific record exists in the upstream table by making a GET request
    and evaluating the API response.

    Parameters
    ----------
    token : str
        The JWT token used for authorization.
    upstream_table : str
        The name of the table from which the record existence is being checked.
    row : dict
        The dictionary containing row data, from which the primary key will be extracted.

    Returns
    -------
    bool
        True if the record exists and the API response is successful, False otherwise.
    """
    res = get_row(token, upstream_table, row)
    print(res.text)
    return is_success(res)

def getToken(username, password):
    """
    Retrieves a JWT token from the API by sending a login request with the user's credentials.

    Parameters
    ----------
    username : str
        The username to authenticate with the API.
    password : str
        The password to authenticate with the API.

    Returns
    -------
    dict
        A dictionary containing the JWT token and other login details from the response.
    """
    request_data = {}
    request_data["action"] = "login"
    request_data["username"] = username
    request_data["password"] = password

    r = requests.post(BASE_URL + "index.php", data=request_data)
    return json.loads(r.text)

def add_row(token, row, upstream_table, edit):
    """
    Adds a new record to the upstream table, or edits an existing one based on the 'edit' flag.

    This function sends a POST request to add a new record, or edits an existing one if the 
    record already exists and the 'edit' flag is set to True.

    Parameters
    ----------
    token : str
        The JWT token used for authorization.
    row : dict
        The dictionary containing row data to be added or edited in the table.
    upstream_table : str
        The name of the table to which the record is being added.
    edit : bool
        A flag indicating whether to edit the record if it already exists.

    Returns
    -------
    bool
        True if the record was successfully added or edited, False otherwise.
    """
    payload = {}
    payload["action"] = "add"
    payload["object"] = upstream_table
    payload.update(cast_properties(row))
    payload["id_utente"] = ID_UTENTE

    print(payload)

    if record_exists(token, upstream_table, row):
        if edit:
            payload["action"] = "edit"
        else:
            return True
    
    match upstream_table:
        case "elf_tbl_sost_aerei":
            del payload["ID_SOST_AEREI"]

    r = requests.post(BASE_URL + "index.php", data=payload, headers={"Authorization": f"Bearer {token}"})

    return is_success(r)

def cast_properties(d):
    """
    Casts or modifies certain properties in the row dictionary according to specific rules.
    
    This function handles conversions for coordinates, orientation, and phase values, 
    ensuring they are in the correct format before being sent to the API.

    Parameters
    ----------
    d : dict
        The dictionary containing the row data that needs to be processed.

    Returns
    -------
    dict
        A new dictionary with the processed and casted properties.
    """
    new_dict = d.copy()
    for key in d.keys():
        match key:
            case 'X_CAVO' | 'Y_CAVO' | 'X_COORD' | 'Y_COORD' | 'Z_COORD':
                value = d[key]
                try:
                    new_dict[key] = value.replace('.', ',')
                    print(float(value))
                except (ValueError, TypeError):
                    print(f"Warning: Errore di conversione per la chiave {key} contenente '{value}' a float.")
            case 'ORIENTAMENTO':
                value = d[key]
                try:
                    new_dict[key] = int(float(value))
                except (ValueError, TypeError):
                    print(f"Warning: Errore di conversione per la chiave {key} contenente '{value}' a int.")
            case 'CODICELOCALE':
                #Fix different naming
                new_dict['CODICE_LOCALE'] = d[key]
            case 'FASE':
                value = d[key]
                match value:
                    case 'A':
                        new_dict[key] = 1
                    case 'B':
                        new_dict[key] = 2
                    case 'C':
                        new_dict[key] = 3

    return new_dict