from datetime import timedelta

#reCaptcha Google config
RECAPTCHA_PUBLIC_KEY = '6LdWmOIUAAAAALBnW-byjnxFgGTN4otXh8dAc4sI'
RECAPTCHA_PRIVATE_KEY ='6LdWmOIUAAAAAE2HuImf23hescbgdftadEv0T60P'
SECRET_KEY= 'DhI1U6g9Pv8wRCGakI3QTAlpWbG4'
TESTING = True

#configer timeout for the session
PERMANENT_SESSION_LIFETIME =  timedelta(seconds=10)

MYSQL_HOST = '104.198.153.176'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'p364352951497-hkqqm8'
MYSQL_DB = 'users'
MYSQL_CURSORCLASS = 'DictCursor'