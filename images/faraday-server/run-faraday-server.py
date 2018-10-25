#!/usr/bin/env python2

import os
import subprocess
from argparse import ArgumentParser
from ConfigParser import ConfigParser
from ConfigParser import NoSectionError


FARADAY_ROOT_DIR = ""
FARADAY_DATA_DIR = ""


def update_database_connection_string(pg_user, pg_pass, pg_host, pg_db):
    print "[+] Updating server.ini..."
    server_ini_path = os.path.join(FARADAY_DATA_DIR, "config", "server.ini")
    server_ini = ConfigParser()
    server_ini.read(server_ini_path)
    try:
        server_ini.get("database", "connection_string")
    except NoSectionError:
        server_ini.add_section("database")
    server_ini.set(
        "database",
        "connection_string",
        "postgresql+psycopg2://%s:%s@%s/%s" % (pg_user, pg_pass, pg_host, pg_db),
    )
    with open(server_ini_path, "w") as server_ini_file:
        server_ini.write(server_ini_file)


def initialize_database():
    # TODO Deal with failures
    print "[+] Initializing database..."
    subprocess.Popen(["python", os.path.join(FARADAY_ROOT_DIR, "manage.py"), "create-tables"]).wait()


def create_superuser(email, name, password):
    # TODO Deal with failures
    print "[+] Creating superuser %s..." % (name,)
    result = subprocess.Popen(
        [
            "python",
            os.path.join(FARADAY_ROOT_DIR, "manage.py"),
            "createsuperuser",
            "--email",
            email,
            "--username",
            name,
            "--password",
            password,
        ]
    ).wait()


def launch_server():
    print "[+] Launching server..."
    subprocess.call(
        [
            "python",
            os.path.join(FARADAY_ROOT_DIR, "faraday-server.py"),
            "--bind", 
            "0.0.0.0",
            "--nodeps",
            "--no-setup",
        ]
    )


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    # Environment options
    arg_parser.add_argument("--faraday-root", type=str, required=True)
    arg_parser.add_argument("--faraday-data", type=str, required=True)
    # Postgres options
    arg_parser.add_argument("--pg-user", type=str, required=True)
    arg_parser.add_argument("--pg-pass", type=str, required=True)
    arg_parser.add_argument("--pg-db", type=str, required=True)
    arg_parser.add_argument("--pg-host", type=str, required=True)
    # Faraday options
    arg_parser.add_argument("--su-mail", type=str, required=True)
    arg_parser.add_argument("--su-name", type=str, required=True)
    arg_parser.add_argument("--su-pass", type=str, required=True)
    args = arg_parser.parse_args()
    # Set global variables
    FARADAY_ROOT_DIR = args.faraday_root
    FARADAY_DATA_DIR = args.faraday_data
    if not os.path.exists(FARADAY_ROOT_DIR) or not os.path.isdir(FARADAY_ROOT_DIR):
        raise ValueError("Faraday root dir \"%s\" does not exist or is not a directory" % (FARADAY_ROOT_DIR,))
    if not os.path.exists(FARADAY_DATA_DIR) or not os.path.isdir(FARADAY_DATA_DIR):
        raise ValueError("Faraday data dir \"%s\" does not exist or is not a directory" % (FARADAY_DATA_DIR,))
    # Update DB connection
    update_database_connection_string(args.pg_user, args.pg_pass, args.pg_host, args.pg_db)
    # Perform first-time-setup if necessary
    initialize_database()
    create_superuser(args.su_mail, args.su_name, args.su_pass)
    # Launch the server
    launch_server()
