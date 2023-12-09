import unittest
import requests_mock
import os
from custom_scaler import CustomScaler
import externalscaler_pb2

class TestCustomScaler(unittest.TestCase):
    def setUp(self):
        self.scaler = CustomScaler()

    @requests_mock.Mocker()
    def test_is_active_true(self, mock):
        # Mock the API endpoint with a value greater than 0
        mock.get('http://mock-api-endpoint.com', text='5')

        # Set the environment variable for the test
        os.environ['SCALER_API_EP'] = 'http://mock-api-endpoint.com'

        # Call IsActive method
        response = self.scaler.IsActive(request=None, context=None)

        # Check if the response is True
        self.assertTrue(response.result)

    @requests_mock.Mocker()
    def test_is_active_false(self, mock):
        # Mock the API endpoint with a value less than or equal to 0
        mock.get('http://mock-api-endpoint.com', text='0')

        # Set the environment variable for the test
        os.environ['SCALER_API_EP'] = 'http://mock-api-endpoint.com'

        # Call IsActive method
        response = self.scaler.IsActive(request=None, context=None)

        # Check if the response is False
        self.assertFalse(response.result)

if __name__ == '__main__':
    unittest.main()
