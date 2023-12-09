import os
import time
import requests
import logging
from urllib.parse import urlparse
import externalscaler_pb2_grpc
import externalscaler_pb2

# Set logging level based on LOG_LEVEL environment variable
log_level = logging.DEBUG if os.getenv('LOG_LEVEL') == 'DEBUG' else logging.INFO
logging.basicConfig(level=log_level)

class CustomScaler(externalscaler_pb2_grpc.ExternalScalerServicer):
    def fetch_metric_value(self):
        """Fetches the metric value from the scaler API endpoint."""
        scaler_api_endpoint = os.getenv('SCALER_API_EP', 'http://localhost:9090/scale')
        logging.debug(f"Fetching metric value from: {scaler_api_endpoint}")

        # Validate the URL
        if not urlparse(scaler_api_endpoint).scheme:
            logging.error(f"Invalid URL: {scaler_api_endpoint}")
            return 0

        try:
            response = requests.get(scaler_api_endpoint)
            response.raise_for_status()
            logging.debug(f"Response received: {response.text.strip()}")
            return response.text.strip()
        except requests.RequestException as e:
            logging.error(f"Error fetching metric value from {scaler_api_endpoint}: {e}")
            return 0

    def IsActive(self, request, context):
        metric_value = self.fetch_metric_value()
        is_active = metric_value != "0"
        logging.debug(f"IsActive check: {is_active}")
        return externalscaler_pb2.IsActiveResponse(result=is_active)

    def StreamIsActive(self, request, context):
        while True:
            metric_value = self.fetch_metric_value()
            is_active = metric_value != "0"
            logging.debug(f"StreamIsActive check: {is_active}")
            yield externalscaler_pb2.IsActiveResponse(result=is_active)
            time.sleep(1)

    def GetMetricSpec(self, request, context):
        target_size = self.fetch_metric_value()
        try:
            target_size = int(target_size)
        except ValueError:
            logging.error(f"Invalid target size value: {target_size}")
            target_size = 0

        metric_spec = externalscaler_pb2.MetricSpec(metricName="desired_replica_count", targetSize=target_size)
        logging.debug(f"GetMetricSpec response: {metric_spec}")
        return externalscaler_pb2.GetMetricSpecResponse(metricSpecs=[metric_spec])

    def GetMetrics(self, request, context):
        metric_value = self.fetch_metric_value()
        try:
            metric_value = int(metric_value)
        except ValueError:
            logging.error(f"Invalid metric value: {metric_value}")
            metric_value = 0

        logging.debug(f"GetMetrics response: MetricValue(metricName='desired_replica_count', metricValue={metric_value})")
        return externalscaler_pb2.GetMetricsResponse(metricValues=[externalscaler_pb2.MetricValue(metricName="desired_replica_count", metricValue=metric_value)])

# Additional server setup code goes here
