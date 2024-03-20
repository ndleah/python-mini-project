from datetime import datetime
from os import getcwd
from typing import Union

import pexpect


def dumper(db_host: str, db_port: Union[str, int], db_user: str, db_name: str, db_password: Union[str, int]):
    dump_name = f'{db_name}_{datetime.now().strftime("%Y%m%d")}.sql'

    child = pexpect.spawn(f"pg_dump -U {db_user} -h {db_host} -p {db_port} -d {db_name} -f {getcwd()}/{dump_name}")
    expected_text = "Password: "
    child.expect(expected_text)
    child.sendline(str(db_password))
    child.interact()


# Just an example
# dumper(db_host='localhost', db_port=5432, db_user='postgres', db_name='database', db_password=12345678)
