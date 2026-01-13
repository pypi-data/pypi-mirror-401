import unittest
from unittest.mock import MagicMock, patch
from io import BytesIO
from src.abnlookup import ABNLookupClient
from src.abnlookup.exceptions import ABNLookupError, APIConnectionError, APIExceptionError

class TestABNLookupClient(unittest.TestCase):
    
    def setUp(self):
        self.guid = "test-guid-123"
        self.client = ABNLookupClient(self.guid)
        print("Setting ABNLookupClient for testing...")

    @patch('abnlookup.client.urllib.request.urlopen')
    def test_search_by_abn_success(self, mock_urlopen):
        # Mock XML response for SearchByABNv202001
        xml_response = """
        <ABRPayloadSearchResults xmlns="http://abr.business.gov.au/ABRXMLSearch/">
            <response>
                <businessEntity202001>
                    <ABN>12345678901</ABN>
                    <entityStatus>
                        <entityStatusCode>Active</entityStatusCode>
                        <effectiveFrom>2020-01-01</effectiveFrom>
                    </entityStatus>
                    <legalName>
                        <organisationName>Test Company Pty Ltd</organisationName>
                        <isCurrentIndicator>Y</isCurrentIndicator>
                    </legalName>
                    <mainBusinessLocation>
                        <mainBusinessLocationState>NSW</mainBusinessLocationState>
                        <mainBusinessLocationPostcode>2000</mainBusinessLocationPostcode>
                    </mainBusinessLocation>
                </businessEntity202001>
            </response>
        </ABRPayloadSearchResults>
        """
        
        # Configure mock to behave like a file context manager
        mock_response = MagicMock()
        mock_response.read.return_value = xml_response.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        
        mock_urlopen.return_value = mock_response

        result = self.client.search_by_abn("12345678901")

        self.assertEqual(result.abn, "12345678901")
        self.assertEqual(result.legal_name.name, "Test Company Pty Ltd")
        self.assertEqual(result.main_business_location.state, "NSW")
        self.assertEqual(result.abn_status.status_code, "Active")

        print("✅ Test search_by_abn_success passed.")

    @patch('abnlookup.client.urllib.request.urlopen')
    def test_search_by_abn_exception(self, mock_urlopen):
        # Mock API Exception response
        xml_response = """
        <ABRPayloadSearchResults xmlns="http://abr.business.gov.au/ABRXMLSearch/">
            <response>
                <exception>
                    <exceptionDescription>Invalid ABN</exceptionDescription>
                </exception>
            </response>
        </ABRPayloadSearchResults>
        """
        
        mock_response = MagicMock()
        mock_response.read.return_value = xml_response.encode('utf-8')
        mock_response.__enter__.return_value = mock_response
        mock_response.__exit__.return_value = None
        
        mock_urlopen.return_value = mock_response

        with self.assertRaises(ABNLookupError) as cm:
            self.client.search_by_abn("00000000000")
        
        self.assertIn("Invalid ABN", str(cm.exception))

        print("✅ Test search_by_abn_exception passed.")
if __name__ == '__main__':
    unittest.main()