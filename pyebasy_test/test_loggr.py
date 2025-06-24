import sys
from unittest import TestCase

import loggr


class TestLoggr(TestCase):
    def test_logging(self):
        for verbocity in loggr.VERBOCITIES:
            loggr.set_verbocity(verbocity)

            loggr.log_technical  ("1. Technical   foo message in verbocity %s" % verbocity)
            loggr.log_detailed   ("2. Detailed    bar message in verbocity %s" % verbocity)
            loggr.log_informative("3. Informative baz message in verbocity %s" % verbocity)
            loggr.log_warning    ("4. Warning     aux message in verbocity %s" % verbocity)
            loggr.log_error      ("5. Error       qux message in verbocity %s" % verbocity)
            loggr.log_error      ("------------------------------------------------------")
