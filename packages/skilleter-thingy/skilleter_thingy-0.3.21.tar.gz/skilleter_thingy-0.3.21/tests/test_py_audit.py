import io
import unittest
from unittest import mock

import skilleter_thingy.py_audit as py_audit


class TestPyAudit(unittest.TestCase):
    def test_audit_uses_timeout_and_reports(self):
        fake_response = mock.Mock()
        fake_response.json.return_value = {}

        with mock.patch('skilleter_thingy.py_audit.requests.post', return_value=fake_response) as post, \
                mock.patch('sys.stdout', new_callable=io.StringIO) as stdout:
            py_audit.audit('example', '1.0.0')

        post.assert_called_once()
        _, kwargs = post.call_args
        self.assertIn('timeout', kwargs)
        self.assertEqual(kwargs['timeout'], 10)

        output = stdout.getvalue()
        self.assertIn('Package: example 1.0.0', output)


if __name__ == '__main__':
    unittest.main()
