"""
Django command to wait for the databse to be ready
"""
import time

from django.core.management.base import BaseCommand

from psycopg2 import OperationalError as psycopgError
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Custom commands"""

    def handle(self, *args, **options):
        """Entry point for the command"""
        self.stdout.write("Waiting for databse")
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default']) #Wait for the databse to be ready
                db_up = True
            except(OperationalError, psycopgError):
                self.stdout.write(self.style.ERROR('Databse unavailabe waiting 1 sec'))
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Databse available!'))
