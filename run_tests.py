"""Run the test suite and save a readable UTF-8 report."""
import io
import logging
from pathlib import Path
import sys
import unittest

logging.getLogger('streamlit.runtime.scriptrunner_utils.script_run_context').setLevel(logging.ERROR)
root = Path(__file__).resolve().parent
suite = unittest.defaultTestLoader.discover(str(root/'tests'))
report = io.StringIO()
result = unittest.TextTestRunner(stream=report,verbosity=2).run(suite)
text = report.getvalue()
(root/'test-results.txt').write_text(text,encoding='utf-8')
print(text)
sys.exit(0 if result.wasSuccessful() else 1)
