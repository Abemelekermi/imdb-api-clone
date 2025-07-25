"""
Test custom commands
"""
from unittest.mock import patch #For mocking

from psycopg2 import OperationalError as psycopgError

from django.test import SimpleTestCase
from django.core.management import call_command
from django.db.utils import OperationalError

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""
    def test_wait_for_db_ready(self, patched_check):
        """Testing waiting for databse until it's ready """
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for databse when getting an error"""
        patched_check.side_effect = [psycopgError] * 2 +\
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])

