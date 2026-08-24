import os
import sys
import subprocess
import argparse
from datetime import datetime
from typing import Union

def dumper(db_host: str = "localhost", db_port: Union[str, int] = 5432, db_user: str = "postgres", db_name: str = "postgres", db_password: str = "") -> str:
    """Export PostgreSQL database backup using pg_dump cross-platform."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_filename = f"{db_name}_{timestamp}.sql"
    dump_path = os.path.join(os.getcwd(), dump_filename)

    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = str(db_password)

    cmd = [
        "pg_dump",
        "-h", str(db_host),
        "-p", str(db_port),
        "-U", str(db_user),
        "-d", str(db_name),
        "-f", dump_path
    ]

    print(f"Executing pg_dump command: {' '.join(cmd[:6])} -f {dump_filename}")
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print(f"Database dump saved successfully to: {dump_path}")
            return dump_path
        else:
            print(f"pg_dump error (Exit Code {result.returncode}): {result.stderr.strip()}")
            return None
    except FileNotFoundError:
        print("Error: 'pg_dump' utility not found. Please ensure PostgreSQL client tools are installed and added to PATH.")
        return None

def main():
    parser = argparse.ArgumentParser(description="PostgreSQL Database Dumper Utility")
    parser.add_argument("--host", default="localhost", help="Database host (default: localhost)")
    parser.add_argument("--port", type=int, default=5432, help="Database port (default: 5432)")
    parser.add_argument("--user", default="postgres", help="Database user (default: postgres)")
    parser.add_argument("--dbname", default="postgres", help="Database name (default: postgres)")
    parser.add_argument("--password", default="", help="Database password")

    args = parser.parse_args()
    dumper(args.host, args.port, args.user, args.dbname, args.password)

if __name__ == '__main__':
    main()

