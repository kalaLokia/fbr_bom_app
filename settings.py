import configparser
import os
import sys


if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


EXPORT_DIR = os.path.join(BASE_DIR, "data")  # File default save location

DB_HOST = None
DB_NAME = "harpy_eagle"  # app specific database name, not interfere with other db
DB_USER = None
DB_PASS = None
DB_CONN_STR = None


# Fixing windows taskbar icon setup
try:
    from ctypes import windll  # Only exists on Windows.

    myappid = "kalalokia.fortune_br.bom_app"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

# Loading application configurations
config = configparser.ConfigParser(interpolation=None)
ok_config = config.read("config.ini")

if ok_config:
    if config.has_option("DATABASE", "DB_HOST"):
        DB_HOST = config.get("DATABASE", "DB_HOST").strip()
    if config.has_option("DATABASE", "DB_USER"):
        DB_USER = config.get("DATABASE", "DB_USER").strip()
    if config.has_option("DATABASE", "DB_PASS"):
        DB_PASS = config.get("DATABASE", "DB_PASS").strip()

    if DB_HOST and DB_NAME and DB_USER and DB_PASS:
        DB_CONN_STR = (
            r"Driver={ODBC Driver 17 for SQL Server};"
            rf"Server={DB_HOST};"
            rf"Database={DB_NAME};"
            rf"uid={DB_USER};"
            rf"pwd={DB_PASS};"
            r"Integrated Security=false;"
        )
    if config.has_option("GENERAL", "SAVE_DIR"):
        EXPORT_DIR = config.get("GENERAL", "SAVE_DIR")

    author = None
    if config.has_option("GENERAL", "DEVELOPED_BY"):
        author = config.get("GENERAL", "DEVELOPED_BY")
        if author.lower() != "kalalokia":
            author = None
    if not author:
        if not config.has_section("GENERAL"):
            config.add_section("GENERAL")
        config.set("GENERAL", "DEVELOPED_BY", "kalaLokia")
        with open("config.ini", "w+") as f:
            config.write(f)


def update_default_save_dir(new_dir: str):
    """Update default save location by the app"""
    global config
    config.set("GENERAL", "SAVE_DIR", new_dir)
    with open("config.ini", "w+") as f:
        config.write(f)


# Required path verification
os.makedirs(os.path.dirname(os.path.join(BASE_DIR, "data/test.txt")), exist_ok=True)
