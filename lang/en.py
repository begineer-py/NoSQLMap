"""English language strings"""

MESSAGES = {
    # General
    'STARTUP_BANNER': '''
    _   _      _____  _____ _      ___  ___
   | \\ | |    /  ___||  _  | |     |  \\/  |
   |  \\| | ___\\ `--. | | | | |     | .  . | __ _ _ __
   | . ` |/ _ \\`--. \\| | | | |     | |\\/| |/ _` | '_ \\
   | |\\  | (_) /\\__/ \\ \\/' / |____ | |  | | (_| | |_) |
   \\_| \\_/\\___/\\____/ \\_/\\_\\_____/ \\_|  |_/\\__,_| .__/
                                                | |
                                                |_|
    ''',
    'MAIN_MENU': '''
================================
        NoSQLMap Main Menu
================================
1. Set target host        (Current: {0})
2. Set web app port       (Current: {1})
3. Set URI path           (Current: {2})
4. Set full target URL    (Current: {3})
5. Set HTTP Authentication
6. Set HTTP method        (Current: {4})
7. Set my local IP        (Current: {5})
8. Set shell listener     (Current: {6})
9. Set platform           (Current: {7})
10. Set database port     (Current: {8})
11. Toggle HTTPS          (Current: {9})
12. Parse target from Burp logs
13. Change language       (Current: {10})
14. NoSQL database attacks
15. NoSQL web app attacks
16. Scan for anonymous access
17. Clear environment
x. Exit
''',
    'PRESS_ENTER': 'Press enter to continue...',
    'INVALID_SELECTION': 'Invalid selection.',
    'LANGUAGE_SET': 'Language set to: {lang}',

    # Main Menu (nosqlmap.py)
    'SELECT_OPTION': 'Select an option: ',
    'MAIN_MENU_TITLE': 'Main Menu',
    'MENU_SET_OPTIONS': '1-Set options',
    'MENU_DB_ACCESS_ATTACKS': '2-NoSQL Database Access Attacks',
    'MENU_WEB_APP_ATTACKS': '3-NoSQL Web App Attacks',
    'MENU_SCAN_ANON': '4-Scan for Anonymous {platform} Access',
    'MENU_CHANGE_PLATFORM': '5-Verify/Change Target Platform (Current: {platform})',
    'MENU_EXIT': 'x-Exit',
    'TARGET_NOT_SET': 'Target not set! Check options.',
    'OPTIONS_NOT_SET_WEB': 'Options not set! Check host and URI path.',

    # Platform Selection (nosqlmap.py)
    'SELECT_PLATFORM': 'Select a platform: ',
    'PLATFORM_MONGODB': '1-MongoDB',
    'PLATFORM_COUCHDB': '2-CouchDB',

    # Options Menu (nosqlmap.py)
    'OPTIONS_TITLE': 'Options',
    'OPT_SET_TARGET': '1-Set target host/IP (Current: {victim})',
    'OPT_SET_WEB_PORT': '2-Set web app port (Current: {webPort})',
    'OPT_SET_APP_PATH': '3-Set App Path (Current: {uri})',
    'OPT_TOGGLE_HTTPS': '4-Toggle HTTPS (Current: {https})',
    'OPT_SET_DB_PORT': '5-Set {platform} Port (Current : {dbPort})',
    'OPT_SET_HTTP_METHOD': '6-Set HTTP Request Method (GET/POST) (Current: {httpMethod})',
    'OPT_SET_LOCAL_IP': '7-Set my local {platform}/Shell IP (Current: {myIP})',
    'OPT_SET_SHELL_PORT': '8-Set shell listener port (Current: {myPort})',
    'OPT_TOGGLE_VERBOSE': '9-Toggle Verbose Mode: (Current: {verb})',
    'OPT_LOAD_FILE': '0-Load options file',
    'OPT_LOAD_BURP': 'a-Load options from saved Burp request',
    'OPT_SAVE_FILE': 'b-Save options file',
    'OPT_SET_HEADERS': 'h-Set headers',
    'OPT_BACK': 'x-Back to main menu',
    'ENTER_HOST_IP': 'Enter the host IP/DNS name: ',
    'INVALID_IP': 'Invalid IP address format.',
    'TARGET_SET_TO': 'Target set to {victim}',
    'ENTER_WEB_PORT': 'Enter the HTTP port for web apps: ',
    'WEB_PORT_SET_TO': 'HTTP port set to {webPort}',
    'ENTER_URI_PATH': 'Enter URI Path (Press enter for no URI): ',
    'URI_PATH_SET_TO': 'URI Path set to {uri}',
    'ENTER_DB_PORT': 'Enter target {platform} port: ',
    'DB_PORT_SET_TO': 'Target {platform} Port set to {dbPort}',
    'SELECT_HTTP_METHOD': 'Select an option: ',
    'HTTP_GET_OPTION': '1-Send request as a GET',
    'HTTP_POST_OPTION': '2-Send request as a POST',
    'GET_REQUEST_SET': 'GET request set',
    'POST_REQUEST_SET': 'POST request set',
    'ENTER_POST_DATA': 'Enter POST data in a comma separated list (i.e. param name 1,value1,param name 2,value2)',
    'ENTER_LOCAL_IP': 'Enter the host IP for my {platform}/Shells: ',
    'LOCAL_IP_SET_TO': 'Shell/DB listener set to {myIP}',
    'ENTER_SHELL_PORT': 'Enter TCP listener for shells: ',
    'SHELL_PORT_SET_TO': 'Shell TCP listener set to {myPort}',
    'VERBOSE_ON': 'Verbose mode ON',
    'VERBOSE_OFF': 'Verbose mode OFF',
    'ENTER_LOAD_FILE': 'Enter file name to load: ',
    'ERROR_READING_FILE': 'I/O error({errno}): {strerror}',
    'ERROR_READING_FILE_PROMPT': 'error reading file. Press enter to continue...',
    'ENTER_BURP_FILE': 'Enter path to Burp request file: ',
    'ENTER_SAVE_FILE': 'Enter file name to save: ',
    'FILE_SAVED_TO': 'Options saved to {savePath}',
    'ENTER_HEADERS': 'Enter HTTP Headers in comma separated list (i.e. Header1, Value1, Header2, Value2): ',
    'HEADERS_SET': 'Headers Set.',

    # nsmweb.py specific messages
    'WEB_ATTACK_GET_TITLE': 'Web App Attacks (GET)',
    'WEB_ATTACK_POST_TITLE': 'Web App Attacks (POST)',
    'WEB_ATTACK_SEPARATOR': '===============',
    'CHECKING_SITE_UP': 'Checking to see if site at {url} is up...',
    'APP_IS_UP_VERBOSE': 'App is up! Got response length of {length} and response time of {time} seconds. Starting injection test.\n',
    'APP_IS_UP': 'App is up!',
    'GOT_RESPONSE_CODE': 'Got {code} from the app, check your options.',
    'SERVER_DID_NOT_RESPOND': 'Looks like the server didn\'t respond. Check your options.',
    'BASELINE_RANDOM_SIZE_PROMPT': 'Baseline test-Enter random string size: ',
    'INVALID_INTEGER': 'Invalid! The size should be an integer.',
    'RANDOM_STRING_FORMAT_PROMPT': 'What format should the random string take?',
    'FORMAT_ALPHANUMERIC': '1-Alphanumeric',
    'FORMAT_LETTERS_ONLY': '2-Letters only',
    'FORMAT_NUMBERS_ONLY': '3-Numbers only',
    'FORMAT_EMAIL': '4-Email address',
    'USING_INJECT_STRING': 'Using {injectString} for injection testing.\n',
    'NO_URI_PARAMS_GET': 'GET request requires URI parameters.  Check options.\n',
    'CHECKING_RANDOM_INJECT_SIZE_GET': 'Checking random injected parameter HTTP response size using {uri} ...\n',
    'CHECKING_RANDOM_INJECT_SIZE_POST': 'Checking random injected parameter HTTP response size sending {postData} ...\n',
    'SENDING_RANDOM_VALUE': 'Sending random parameter value...',
    'GOT_RESPONSE_LENGTH': 'Got response length of {length}.',
    'NO_CHANGE_RESPONSE_SIZE': 'No change in response size injecting a random parameter..\n',
    'RANDOM_VALUE_VARIANCE': 'Random value variance: {delta}\n',
    'LIST_PARAMETERS': 'List of parameters:',
    'SELECT_INJECT_PARAM_POST': 'Which parameter should we inject? ',
    'SELECT_INJECT_PARAMS_GET': 'Enter parameters to inject in a comma separated list:  ',
    'INJECTING_PARAM': 'Injecting the {param} parameter...',
    'INJECTING_PARAMS': 'Injecting the following parameters:',
    'SOMETHING_WENT_WRONG': 'Something went wrong. Press enter to return to the main menu...',
    'ERROR_PARSING_URL': 'Not able to parse the URL and parameters. Check options settings.',
    'ERROR_SELECTING_PARAMS': 'Error selecting injection parameters: {e}',
    'INVALID_PARAM_INDEX': "Warning: Invalid parameter index '{index}' ignored.",
    'NO_VALID_PARAMS_SELECTED': 'Error: No valid parameters selected for injection.',
    'TEST_PHP_NE_ASSOC': 'Test 1: PHP/ExpressJS != associative array injection',
    'TEST_PHP_GT_UNDEFINED': 'Test 2: PHP/ExpressJS > Undefined Injection',
    'TEST_WHERE_STR_FIND': 'Test 3: $where injection (string escape)',
    'TEST_WHERE_INT_FIND': 'Test 4: $where injection (integer escape)',
    'TEST_WHERE_STR_FINDONE': 'Test 5: $where injection string escape (single record)',
    'TEST_WHERE_INT_FINDONE': 'Test 6: $where injection integer escape (single record)',
    'TEST_THIS_NE_STR': 'Test 7: This != injection (string escape)',
    'TEST_THIS_NE_INT': 'Test 8: This != injection (integer escape)',
    'TEST_TIME_BLIND_STR': 'Starting Javascript string escape time based injection...',
    'TEST_TIME_BLIND_INT': 'Starting Javascript integer escape time based injection...',
    'TIME_VARIANCE_SUCCESS': 'HTTP load time variance was {delta} seconds! Injection possible.',
    'TIME_VARIANCE_FAIL': 'HTTP load time variance was only {delta} seconds. Injection probably didn\'t work.',
    'MONGO_LESS_24_DETECTED': 'MongoDB < 2.4 detected. Start brute forcing database info (y/n)? ',
    'VULNERABLE_URLS': 'Vulnerable URLs:',
    'POSSIBLY_VULNERABLE_URLS': 'Possibly vulnerable URLs:',
    'EXPLOITABLE_REQUESTS': 'Exploitable requests:',
    'POSSIBLY_VULNERABLE_REQUESTS': 'Possibly vulnerable requests:',
    'TIMING_ATTACKS_RESULTS': 'Timing based attacks:',
    'TIMING_STR_SUCCESS': 'String attack-Successful',
    'TIMING_STR_FAIL': 'String attack-Unsuccessful',
    'TIMING_INT_SUCCESS': 'Integer attack-Successful',
    'TIMING_INT_FAIL': 'Integer attack-Unsuccessful',
    'SAVE_RESULTS_PROMPT': 'Save results to file (y/n)? ',
    'ENTER_OUTPUT_FILENAME': 'Enter output file name: ',
    'INJECTION_RETURNED_ERROR': 'Injection returned a MongoDB Error. Injection may be possible.',
    'INJECTION_SUCCESS_VERBOSE': 'Response varied {delta} bytes from random parameter value! Injection works!',
    'INJECTION_SUCCESS': 'Successful injection!',
    'INJECTION_POSSIBLE_VERBOSE': 'Response variance was only {delta} bytes. Injection might have worked but difference is too small to be certain. ',
    'INJECTION_POSSIBLE': 'Possible injection.',
    'INJECTION_FAILED_VERBOSE': 'Random string response size and not equals injection were the same. Injection did not work.',
    'INJECTION_FAILED': 'Injection failed.',
    'INJECTION_POSSIBLE_SMALLER_VERBOSE': 'Injected response was smaller than random response. Injection may have worked but requires verification.',
    'GETDBINFO_BASELINE_SIZE': 'Getting baseline True query return size...',
    'GETDBINFO_GOT_BASELINE_SIZE': 'Got baseline true query length of {length}',
    'GETDBINFO_CALC_DB_NAME_LEN': 'Calculating DB name length...',
    'GETDBINFO_GOT_DB_NAME_LEN': 'Got database name length of {length} characters.',
    'GETDBINFO_DB_NAME': 'Database Name: ',
    'GETDBINFO_GET_USERS_PROMPT': 'Get database users and password hashes (y/n)? ',
    'GETDBINFO_FOUND_USERS': 'Found {count} user(s).',
    'GETDBINFO_GOT_USER_HASH': 'Got user:hash {user}:{hash}',
    'GETDBINFO_CRACK_HASH_PROMPT': 'Crack recovered hashes (y/n)?:',
    'GETDBINFO_SELECT_USER_TO_CRACK': 'Select user hash to crack: ',
    'GETDBINFO_CRACK_ANOTHER_PROMPT': 'Crack another hash (y/n)?',
    'WARN_URI_NOT_GENERATED': 'Error: Test URIs for getDBInfo not generated. Run GET scan first.',
    'WARN_PAYLOAD_GENERATION_FAILED': 'Failed to generate injection payloads.',
    'WARN_SKIPPING_TEST': 'Skipping Test {testNum}: Could not generate payload.',
    'INFO_RUNNING_TEST': '--- Running Test {testNum} ---',
    'INFO_RUNNING_TIME_TEST_STR': '--- Running Test 9 (Time-based String) ---',
    'INFO_RUNNING_TIME_TEST_INT': '--- Running Test 10 (Time-based Integer) ---',
    'APP_PATH_PARAMS': 'Enter a complete URL including parameters (or press Enter to abort): ',

    # nsmcouch.py specific messages
    'COUCHDB_ATTACK_TITLE': 'DB Access attacks (CouchDB)',
    'COUCHDB_CHECK_CREDS': 'Checking to see if credentials are needed...',
    'COUCHDB_SUCCESS_NO_CREDS': 'Successful access with no credentials!',
    'COUCHDB_LOGIN_REQUIRED': 'Login required!',
    'COUCHDB_ENTER_USERNAME': 'Enter server username: ',
    'COUCHDB_ENTER_PASSWORD': 'Enter server password: ',
    'COUCHDB_AUTH_SUCCESS': 'CouchDB authenticated on {target}:{port}',
    'COUCHDB_AUTH_FAILED': 'Failed to authenticate. Press enter to continue...',
    'COUCHDB_ACCESS_CHECK_FAIL': 'Access check failure. Testing will continue but will be unreliable.',
    'COUCHDB_CONNECT_FAIL': "Couldn't connect to CouchDB server. Press enter to return to the main menu.",
    'COUCHDB_FUTON_OPEN': 'Sofa web management open at {url}. No authentication required!',
    'COUCHDB_FUTON_CLOSED': 'Sofa web management closed or requires authentication.',
    'COUCHDB_MENU_GET_INFO': '1-Get Server Version and Platform',
    'COUCHDB_MENU_ENUM_DBS': '2-Enumerate Databases/Users/Password Hashes',
    'COUCHDB_MENU_ENUM_ATT': '3-Check for Attachments (still under development)',
    'COUCHDB_MENU_CLONE_DB': '4-Clone a Database',
    'COUCHDB_MENU_RETURN': '5-Return to Main Menu',
    'COUCHDB_SELECT_ATTACK': 'Select an attack: ',
    'COUCHDB_SERVER_INFO': 'Server Info:',
    'COUCHDB_VERSION': 'CouchDB Version: {version}',
    'COUCHDB_ENUM_ATTACHMENTS': 'Enumerating all attachments...',
    'COUCHDB_LIST_DATABASES': 'List of databases:',
    'COUCHDB_ERROR_LIST_DBS': "Error: Couldn't list databases. The provided credentials may not have rights.",
    'COUCHDB_USERS_HASHES': 'Database Users and Password Hashes:',
    'COUCHDB_USERNAME': 'Username: {user}',
    'COUCHDB_HASH': 'Hash: {hash}',
    'COUCHDB_SALT': 'Salt: {salt}',
    'COUCHDB_CRACK_THIS_HASH': 'Crack this hash (y/n)? ',
    'COUCHDB_CANT_LIST_DBS_STEAL': "Can't get a list of databases to steal. The provided credentials may not have rights.",
    'COUCHDB_SELECT_DB_TO_STEAL': 'Select a database to steal:',
    'COUCHDB_DB_CLONED': 'Database cloned. Copy another (y/n)? ',
    'COUCHDB_CLONE_ERROR': 'Something went wrong. Are you sure your CouchDB is running and options are set? Press enter to return...',
    'COUCHDB_PASSCRACK_TITLE': 'Select password cracking method: ',
    'COUCHDB_PASSCRACK_DICT': '1-Dictionary Attack',
    'COUCHDB_PASSCRACK_BRUTE': '2-Brute Force',
    'COUCHDB_PASSCRACK_EXIT': '3-Exit',
    'COUCHDB_PASSCRACK_SELECTION': 'Selection: ',
    'COUCHDB_BRUTE_MAXLEN': 'Enter the maximum password length to attempt: ',
    'COUCHDB_BRUTE_CHARSET_PROMPT': 'Select character set to use:',
    'COUCHDB_BRUTE_LOWER': '1-Lower case letters',
    'COUCHDB_BRUTE_UPPER': '2-Upper case letters',
    'COUCHDB_BRUTE_ALPHA': '3-Upper + lower case letters',
    'COUCHDB_BRUTE_NUM': '4-Numbers only',
    'COUCHDB_BRUTE_ALPHANUM': '5-Alphanumeric (upper and lower case)',
    'COUCHDB_BRUTE_ALL': '6-Alphanumeric + special characters',
    'COUCHDB_BRUTE_TESTING': 'Combinations tested: {count}\r',
    'COUCHDB_DICT_ENTER_PATH': 'Enter path to password dictionary: ',
    'COUCHDB_DICT_LOAD_ERROR': " Couldn't load file.",
    'COUCHDB_DICT_RUNNING': 'Running dictionary attack...',
    'COUCHDB_PASS_CRACKED': 'Password Cracked - {password}',
    'COUCHDB_PASS_CRACKED_ALT': 'Password Cracked- {password}',

    # nsmmongo.py specific messages
    'MONGODB_ATTACK_TITLE': 'DB Access attacks (MongoDB)',
    'MONGODB_CONNECT_SUCCESS': 'Successful connection to MongoDB at {target}:{port}',
    'MONGODB_CONNECT_FAIL': 'Failed to connect to MongoDB at {target}:{port}. Check host/port.',
    'MONGODB_AUTH_SUCCESS': 'MongoDB authenticated on {target}:{port}',
    'MONGODB_AUTH_FAILED': 'Failed to authenticate to MongoDB. Check credentials.',
    'MONGODB_CHECK_CREDS': 'Checking to see if credentials are needed...',
    'MONGODB_SUCCESS_NO_CREDS': 'Successful access with no credentials!',
    'MONGODB_LOGIN_REQUIRED': 'Login required!',
    'MONGODB_ENTER_USERNAME': 'Enter server username: ',
    'MONGODB_ENTER_PASSWORD': 'Enter server password: ',
    'MONGODB_MENU_GET_INFO': '1-Get Server Info/Status',
    'MONGODB_MENU_ENUM_DBS': '2-Enumerate Databases/Collections/Users',
    'MONGODB_MENU_ENUM_DOCS': '3-Enumerate Documents',
    'MONGODB_MENU_RETURN': '4-Return to Main Menu',
    'MONGODB_SELECT_ATTACK': 'Select an attack: ',
    'MONGODB_SERVER_INFO': 'Server Info:',
    'MONGODB_SERVER_STATUS': 'Server Status:',
    'MONGODB_VERSION': 'MongoDB Version: {version}',
    'MONGODB_PLATFORM': 'Platform: {platform}',
    'MONGODB_PROCESS': 'Process: {process}',
    'MONGODB_PID': 'PID: {pid}',
    'MONGODB_UPTIME': 'Uptime: {uptime} seconds',
    'MONGODB_LIST_DATABASES': 'List of databases:',
    'MONGODB_ERROR_LIST_DBS': "Error: Couldn't list databases. Credentials may lack rights.",
    'MONGODB_LIST_COLLECTIONS': 'Collections in {db}:',
    'MONGODB_ERROR_LIST_COLLS': 'Error listing collections in {db}.',
    'MONGODB_LIST_USERS': 'Users in {db}:',
    'MONGODB_ERROR_LIST_USERS': 'Error listing users in {db}. Check privileges.',
    'MONGODB_SELECT_DB_ENUM': 'Select a database to enumerate documents from:',
    'MONGODB_SELECT_COLL_ENUM': 'Select a collection to enumerate documents from:',
    'MONGODB_ENUM_DOCUMENTS': 'Enumerating documents in {db}.{collection}:',
    'MONGODB_FOUND_DOCUMENT': 'Found document: {doc}',
    'MONGODB_ERROR_ENUM_DOCS': 'Error enumerating documents in {db}.{collection}.',
    'MONGODB_PASSCRACK_TITLE': 'Select MongoDB hash cracking method: ',
    'MONGODB_PASSCRACK_DICT': '1-Dictionary Attack',
    'MONGODB_PASSCRACK_BRUTE': '2-Brute Force',
    'MONGODB_PASSCRACK_EXIT': '3-Exit',
    'MONGODB_PASSCRACK_SELECTION': 'Selection: ',
    'MONGODB_CRACK_THIS_HASH': 'Crack this hash (y/n)? ',
    'MONGODB_USERNAME': 'Username: {user}',
    'MONGODB_HASH': 'Hash: {hash}', # Note: MongoDB hashes are usually user@db
    'MONGODB_BRUTE_MAXLEN': 'Enter the maximum password length to attempt: ',
    'MONGODB_BRUTE_CHARSET_PROMPT': 'Select character set to use:',
    'MONGODB_BRUTE_LOWER': '1-Lower case letters',
    'MONGODB_BRUTE_UPPER': '2-Upper case letters',
    'MONGODB_BRUTE_ALPHA': '3-Upper + lower case letters',
    'MONGODB_BRUTE_NUM': '4-Numbers only',
    'MONGODB_BRUTE_ALPHANUM': '5-Alphanumeric (upper and lower case)',
    'MONGODB_BRUTE_ALL': '6-Alphanumeric + special characters',
    'MONGODB_BRUTE_TESTING': 'Combinations tested: {count}\r',
    'MONGODB_DICT_ENTER_PATH': 'Enter path to password dictionary: ',
    'MONGODB_DICT_LOAD_ERROR': " Couldn't load file.",
    'MONGODB_DICT_RUNNING': 'Running dictionary attack...',
    'MONGODB_PASS_CRACKED': 'Password Cracked - {password}',

    # nsmscan.py specific messages
    'SCAN_MONGO_TITLE': 'MongoDB Default Access Scanner',
    'SCAN_COUCH_TITLE': 'CouchDB Default Access Scanner',
    'SCAN_SEPARATOR': '==============================',
    'SCAN_SUBNET_OPTION': '1-Scan a subnet for default {platform} access',
    'SCAN_LOAD_FILE_OPTION': '2-Loads IPs to scan from a file',
    'SCAN_TOGGLE_PING_OPTION': '3-Enable/disable host pings before attempting connection (Currently: {status})',
    'SCAN_RETURN_MENU_OPTION': 'x-Return to main menu',
    'SCAN_ENTER_SUBNET': 'Enter subnet to scan (i.e. 192.168.1.0/24): ',
    'SCAN_INVALID_SUBNET': 'Invalid subnet format. Please use CIDR notation (e.g., 192.168.1.0/24).',
    'SCAN_ENTER_FILENAME': 'Enter filename with IPs to scan: ',
    'SCAN_PING_ENABLED': 'Host pinging enabled.',
    'SCAN_PING_DISABLED': 'Host pinging disabled.',
    'SCAN_SCANNING_SUBNET': 'Scanning subnet {subnet} for default {platform} access...',
    'SCAN_SCANNING_FILE': 'Scanning hosts from file {filename} for default {platform} access...',
    'SCAN_HOST_FOUND_NO_AUTH': '--> Found {platform} at {ip}:{port} - NO AUTH REQUIRED!',
    'SCAN_HOST_FOUND_AUTH_REQ': '--> Found {platform} at {ip}:{port} - Authentication required.',
    'SCAN_HOST_FOUND_CONN_FAIL': '--> Found host at {ip} but connection to port {port} failed.',
    'SCAN_HOST_DOWN': '--> Host {ip} appears down or unresponsive to ping.',
    'SCAN_COMPLETE': 'Scan Complete!',
    'SCAN_FOUND_HOSTS_TITLE': 'Hosts found with NO AUTH required:',
    'SCAN_NO_HOSTS_FOUND': 'No hosts found with anonymous access.',

    # Platform Auto-Detection messages
    'AUTO_DETECT_STARTING': 'Attempting to auto-detect platform on {target}...',
    'AUTO_DETECT_MONGO_SUCCESS': '[+] MongoDB detected on port {port} (No auth required or TBD).',
    'AUTO_DETECT_MONGO_CONN_FAIL': '[-] MongoDB connection failed on port {port}.',
    'AUTO_DETECT_MONGO_AUTH_REQ': '[+] MongoDB detected on port {port} (Authentication required).',
    'AUTO_DETECT_MONGO_ERROR': '[!] Error checking MongoDB on port {port}: {error}',
    'AUTO_DETECT_COUCH_SUCCESS': '[+] CouchDB detected on port {port}.',
    'AUTO_DETECT_COUCH_CONN_FAIL': '[-] CouchDB connection failed on port {port}.',
    'AUTO_DETECT_COUCH_TIMEOUT': '[-] CouchDB connection timed out on port {port}.',
    'AUTO_DETECT_COUCH_UNEXPECTED_RESP': '[?] Connected to port {port}, but response was not typical CouchDB welcome.',
    'AUTO_DETECT_COUCH_BAD_JSON': '[?] Connected to port {port}, received non-JSON response.',
    'AUTO_DETECT_COUCH_HTTP_ERROR': '[?] Received HTTP {status} error from port {port}.',
    'AUTO_DETECT_COUCH_ERROR': '[!] Error checking CouchDB on port {port}: {error}',
    'AUTO_DETECT_FINAL': '[*] Auto-detection finished. Using platform: {platform}',
    'AUTO_DETECT_FAILED': '[-] Auto-detection failed. No known platform detected on default ports.',
    'AUTO_DETECT_FALLBACK': '[!] Auto-detection failed or target not specified. Falling back to default platform: {platform}',
    'PLATFORM_SET_CMD': '[*] Platform explicitly set via command line: {platform} (Port: {port})',

    # In-Attack Prompts
    'ENTER_TARGET_NOW': 'Target host/IP not set. Please enter target: ',
    'TARGET_INPUT_REQUIRED': '[!] Target input is required to proceed.',
    'ENTER_URI_NOW': 'Web App URI path not set. Please enter URI path (e.g., /app/user.php?id=1): ',
    'URI_INPUT_REQUIRED': '[!] URI path is required for web attacks.',
    'POST_DATA_REQUIRED_VIA_OPTIONS': '[!] POST method selected, but no POST data found. Please set POST data via Option 1 first.',
    'INFO_KEEPING_PLATFORM': '[!] Auto-detection failed. Keeping current platform setting: {platform}',
    'INFO_USING_PLATFORM': '[*] Proceeding with platform: {platform} on port {port}',
    'INFO_RUNNING_WEB_ATTACK': '[*] Running Web Attack (Method: {method}, Assumed Platform for Payloads: {platform})',
    'PLATFORM_NOT_SUPPORTED_ATTACK': '[!] Attack type not supported for platform: {platform}',
    'INVALID_PORT_RANGE': '[!] Invalid port number. Port must be between 1 and 65535.',
    'ERROR_WRITING_FILE': 'Error writing file ({errno}): {strerror}',
    'SELECT_TARGET_OR_EXIT': 'Select a target number to set it, or press x to exit: ',
    'NEW_TARGET_SET': 'New target set to: {target}',

    # URL protocol detection messages
    'URI_PROTOCOL_REMOVED': 'Detected and removed protocol from URI. Using path portion only.',
    'URI_PROTOCOL_REMOVED_SIMPLE': 'Removed http:// or https:// prefix from URI.',

    # Command line help
    'TOOL_DESC': 'NoSQLMap - MongoDB/CouchDB/Redis/Neo4j NoSQL Attack Tool',
    'URL_HELP': 'Target URL to attack',
    'MYIP_HELP': 'Local IP for reverse connections',
    'FORM_HELP': 'Attempt to parse form parameters from URL',
    'LANGUAGE_HELP': 'Set language (en/zh)',
    'CHINESE_HELP': 'Set language to Chinese',
    'ENGLISH_HELP': 'Set language to English',
    'VICTIM_HELP': 'Target server for NoSQL database',
    'PLATFORM_HELP': 'Target NoSQL platform (MongoDB, Neo4j, CouchDB)',
    'DBPORT_HELP': 'TCP port for the NoSQL database',
    'WEBPORT_HELP': 'TCP port for the web server to attack',
    'URI_HELP': 'Target URI path',
    'METHOD_HELP': 'HTTP method (GET/POST)',
    'CRAWL_HELP': 'Crawl target site with specified depth',
    'ADVANCED_OPTIONS': 'Advanced options',
    'USAGE_EXAMPLES': '''
Examples:
  python nosqlmap.py http://example.com/app -f 
  python nosqlmap.py -v example.com -u /login
  python nosqlmap.py -zh
''',
    
    # Form parsing
    'FORM_FOUND': 'Found {0} forms on the page.',
    'FORM_DETAILS': 'Form #{0} (Action: {1}, Method: {2}):',
    'FIELD_NAME': 'Field Name: {0}, Type: {1}, Default Value: {2}',
    'NO_FORMS': 'No forms found on the target page.',
    'FORM_PARSE_ERR': 'Error parsing forms: {0}',
    'FORM_SELECT': 'Select a form to test (1-{0}): ',
    'INVALID_FORM': 'Invalid form number.',
    'FORM_PARSE_SUCCESS': 'Successfully parsed form. Target configured for attack.',
    'FORM_CONFIG': 'Form configuration: Method={0}, URI={1}',
    
    # Web crawling
    'CRAWL_START': 'Starting web crawl from {0} with depth {1}',
    'CRAWL_FOUND': 'Found {0} unique URLs',
    'FORM_PAGES_FOUND': 'Found {0} pages with forms',
    'CRAWL_ERROR': 'Error during crawling: {0}'
}
