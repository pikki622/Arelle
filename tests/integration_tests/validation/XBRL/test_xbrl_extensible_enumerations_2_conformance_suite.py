import os
import pytest

from tests.integration_tests.validation.validation_util import get_test_data

# from https://specifications.xbrl.org/work-product-index-extensible-enumerations-extensible-enumerations-2.0.html
CONFORMANCE_SUITE = 'tests/resources/conformance_suites/extensible-enumerations-2.0-2020-02-12.zip/extensible-enumerations-2.0-2020-02-12'
ARGS = [
    '--file', os.path.join(CONFORMANCE_SUITE, 'enumerations-index.xml'),
    '--keepOpen',
    '--testcaseResultsCaptureWarnings',
    '--validate',
]

if os.getenv('CONFORMANCE_SUITES_TEST_MODE') == 'OFFLINE':
    ARGS.extend(['--internetConnectivity', 'offline'])

TEST_DATA = get_test_data(ARGS)


@pytest.mark.parametrize("result", TEST_DATA)
def test_extensible_enumerations_2_conformance_suite(result):
    assert result['status'] == 'pass', \
        'Expected these validation suffixes: {}, but received these validations: {}'.format(
            result.get('expected'), result.get('actual')
        )
