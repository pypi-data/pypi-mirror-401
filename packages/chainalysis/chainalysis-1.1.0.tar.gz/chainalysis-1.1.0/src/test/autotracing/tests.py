import unittest
from unittest.mock import Mock, patch
import requests

from chainalysis.autotracing._autotracing import AutoTracing, StepRequest, StepResponse
from chainalysis._exceptions import (
    BadRequest,
    DataSolutionsAPIException,
    InternalServerException,
    UnhandledException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    RateLimitExceededException,
)

mocked_successful_response = {
    "status": "success",
    "results": {
        "graph": {
            "nodes": [],
            "edges": []
        }
    },
    "reactor_url": None
}

mocked_error_response = {
    "status": "error",
    "message": "Invalid request",
    "details": "Some error details"
}

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

class AutoTracingTests(unittest.TestCase):
    def setUp(self):
        self.autotracing = AutoTracing(api_key="test_api_key")
        self.sample_payload_with_edges = {
            "graph": {
                "nodes": [
                    {
                        "address": "TShZzD9JGGfmxNav8VYcV6vypMdosDqC2G",
                        "chain_name": "tron",
                        "step": 0
                    }
                ],
                "edges": [
                    {
                        "transaction_hash": "0x05b209ac3a8e26ef09786435ea4424130c3a37c8e3f3cec001ff6d6a4c39e3d8",
                        "timestamp": "2025-02-23T08:15:59Z",
                        "chain_name": "ethereum",
                        "step": 1,
                        "sender_address": "0xfa3fcccb897079fd83bfba690e7d47eb402d6c49",
                        "receiver_address": "0xdfa626bc29c47b08d63a247b30a2ec6edfae7d98",
                        "category": "direct",
                        "subcategory": "native",
                        "token_address": "0x0000000000000000000000000000000000000000",
                        "symbol": "native",
                        "amount": 156095525954936500000,
                        "amount_usd": 440368.8930477691,
                        "is_matched": False,
                        "to_chain_name": "ethereum",
                        "is_classified": True,
                        "chain_caip2": "eip155:1",
                        "to_chain_caip2": "eip155:1",
                        "effective_to_chain_name": "ethereum"
                    }
                ]
            },
            "metadata": {
                "start_timestamp": "2025-02-22T08:16:11Z"
            }
        }
        self.sample_payload_without_edges = {
            "graph": {
                "nodes": [
                    {
                        "address": "TShZzD9JGGfmxNav8VYcV6vypMdosDqC2G",
                        "chain_name": "tron",
                        "step": 0
                    }
                ],
                "edges": []
            },
            "metadata": {
                "start_timestamp": "2025-02-22T08:16:11Z"
            }
        }

    def test_step_request_validation(self):
        """Test that StepRequest correctly validates the input payload."""
        request = StepRequest(**self.sample_payload_with_edges)
        self.assertEqual(request.graph.nodes[0].address, "TShZzD9JGGfmxNav8VYcV6vypMdosDqC2G")
        self.assertEqual(request.graph.nodes[0].chain_name, "tron")
        self.assertEqual(request.graph.nodes[0].step, 0)
        self.assertEqual(len(request.graph.edges), 1)
        self.assertEqual(request.metadata["start_timestamp"], "2025-02-22T08:16:11Z")

    def test_step_request_validation_without_edges(self):
        """Test that StepRequest correctly validates a payload without edges."""
        request = StepRequest(**self.sample_payload_without_edges)
        self.assertEqual(request.graph.nodes[0].address, "TShZzD9JGGfmxNav8VYcV6vypMdosDqC2G")
        self.assertEqual(len(request.graph.edges), 0)

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_step_successful_response(self, mock_issue_request):
        """Test successful step execution."""
        mock_issue_request.return_value = mocked_successful_response

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertTrue(result.was_successful())
        self.assertEqual(result.status_code(), 200)
        self.assertEqual(result.json(), mocked_successful_response["results"])
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_step_error_response(self, mock_issue_request):
        """Test error handling in step execution."""
        mock_issue_request.return_value = mocked_error_response

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 0)
        mock_issue_request.assert_called_once()

    def test_address_type_validation(self):
        """Test address_type validation."""
        # Valid address type
        node = StepRequest(**{
            "graph": {
                "nodes": [{
                    "address": "0x123",
                    "chain_name": "ethereum",
                    "address_type": "contract"
                }],
                "edges": []
            }
        })
        self.assertEqual(node.graph.nodes[0].address_type, "contract")

        # Invalid address type
        with self.assertRaises(ValueError):
            StepRequest(**{
                "graph": {
                    "nodes": [{
                        "address": "0x123",
                        "chain_name": "ethereum",
                        "address_type": "invalid"
                    }],
                    "edges": []
                }
            })

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_invalid_address_type_in_step(self, mock_issue_request):
        """Test that step method properly handles invalid address_type."""
        invalid_payload = {
            "graph": {
                "nodes": [{
                    "address": "0x123",
                    "chain_name": "ethereum",
                    "address_type": "invalid"  # Invalid address type
                }],
                "edges": []
            },
            "metadata": {
                "start_timestamp": "2024-02-22T08:16:11Z"
            }
        }

        result = self.autotracing.step(invalid_payload)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 0)
        self.assertTrue("address_type must be either 'contract' or 'wallet'" in str(result.error_message))
        mock_issue_request.assert_not_called()  # Should fail validation before making API call

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_bad_request(self, mock_issue_request):
        """Test handling of bad request errors."""
        mock_issue_request.side_effect = BadRequest(message="Bad request")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 400)
        with self.assertRaises(BadRequest):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_unauthorized(self, mock_issue_request):
        """Test handling of unauthorized errors."""
        mock_issue_request.side_effect = UnauthorizedException(message="Unauthorized")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 401)
        with self.assertRaises(UnauthorizedException):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_forbidden(self, mock_issue_request):
        """Test handling of forbidden errors."""
        mock_issue_request.side_effect = ForbiddenException(message="Forbidden")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 403)
        with self.assertRaises(ForbiddenException):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_not_found(self, mock_issue_request):
        """Test handling of not found errors."""
        mock_issue_request.side_effect = NotFoundException(message="Not found")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 404)
        with self.assertRaises(NotFoundException):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_rate_limit(self, mock_issue_request):
        """Test handling of rate limit errors."""
        mock_issue_request.side_effect = RateLimitExceededException(message="Rate limit exceeded")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 429)
        with self.assertRaises(RateLimitExceededException):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_api_exception(self, mock_issue_request):
        """Test handling of general API exceptions."""
        mock_issue_request.side_effect = DataSolutionsAPIException(message="API error")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 501)
        with self.assertRaises(DataSolutionsAPIException):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_internal_server_exception(self, mock_issue_request):
        """Test handling of internal server exceptions."""
        mock_issue_request.side_effect = InternalServerException(message="Internal server error")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 500)
        with self.assertRaises(InternalServerException):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_unhandled_exception(self, mock_issue_request):
        """Test handling of unhandled exceptions."""
        mock_issue_request.side_effect = Exception("Unexpected error")

        result = self.autotracing.step(self.sample_payload_with_edges)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 500)
        with self.assertRaises(UnhandledException):
            result.json()
        mock_issue_request.assert_called_once()

    @patch('chainalysis.autotracing._autotracing.issue_request')
    def test_invalid_step_type(self, mock_issue_request):
        """Test that step method properly handles invalid step type."""
        invalid_payload = {
            "graph": {
                "nodes": [{
                    "address": "0x123",
                    "chain_name": "ethereum",
                    "step": "not_an_integer"  # Invalid step type
                }],
                "edges": []
            },
            "metadata": {
                "start_timestamp": "2024-02-22T08:16:11Z"
            }
        }

        result = self.autotracing.step(invalid_payload)
        
        self.assertFalse(result.was_successful())
        self.assertEqual(result.status_code(), 0)
        self.assertTrue("Input should be a valid integer" in str(result.error_message))
        mock_issue_request.assert_not_called()  # Should fail validation before making API call

    def test_add_node(self):
        """Test adding node to intital graph."""

        initial_graph = {
                "nodes": [],
                "edges": []
        }
        node = {
            "address": "0x234",
            "chain_name": "ethereum",
            "address_type": "contract"
        }

        result_graph = self.autotracing.add_node(initial_graph, node)
        self.assertEqual(len(result_graph["nodes"]), 1)

    def test_add_edge(self):
        """Test adding edge to intital graph."""

        initial_graph = {
                "nodes": [],
                "edges": []
        }
        edge =  {
            "transaction_hash": "0x05b209ac3a8e26ef09786435ea4424130c3a37c8e3f3cec001ff6d6a4c39e3d8",
            "timestamp": "2025-02-23T08:15:59Z",
            "chain_name": "ethereum",
            "step": 1,
            "sender_address": "0xfa3fcccb897079fd83bfba690e7d47eb402d6c49",
            "receiver_address": "0xdfa626bc29c47b08d63a247b30a2ec6edfae7d98",
            "category": "direct",
            "subcategory": "native",
            "token_address": "0x0000000000000000000000000000000000000000",
            "symbol": "native",
            "amount": 156095525954936500000,
            "amount_usd": 440368.8930477691,
            "is_matched": False,
            "to_chain_name": "ethereum",
            "is_classified": True,
            "chain_caip2": "eip155:1",
            "to_chain_caip2": "eip155:1",
            "effective_to_chain_name": "ethereum"
        }

        result_graph = self.autotracing.add_edge(initial_graph, edge)
        self.assertEqual(len(result_graph["edges"]), 1)


if __name__ == '__main__':
    unittest.main() 