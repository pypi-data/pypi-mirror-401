from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, field_validator, ValidationError

from chainalysis._constants import BASE_URL
from chainalysis._exceptions import (
    DataSolutionsSDKException,
    UnhandledException,
)
from chainalysis.util_functions.requests import issue_request

class AddressNode(BaseModel):
    address: str = Field(description="Blockchain address")
    chain_name: str = Field(description="Chain identifier (e.g., 'ethereum', 'tron')")
    step: Optional[int] = Field(None, description="The iteration number")
    is_target: Optional[bool] = Field(None, description="Whether this address should be explored")
    address_type: Optional[str] = Field(None, description="Type of address")
    protocol_name: Optional[str] = Field(None, description="Human-readable name for the address")
    protocol_category: Optional[str] = Field(None, description="Category of the address")
    nonce: Optional[int] = Field(None, description="Address nonce")
    cluster_id: Optional[str] = Field(None, description="Cluster identifier")
    cluster_name: Optional[str] = Field(None, description="Human-readable name for the cluster")
    cluster_category: Optional[str] = Field(None, description="Category of the cluster")
    category: Optional[str] = Field(None, description="Combine protocol and cluster data to get the high-level category")
    is_classified: Optional[bool] = Field(None, description="Internal flag to track if address has been classified via APIs")
    chain_caip2: Optional[str] = Field(None, description="Chain identifier in CAIP-2 format")
    color: Optional[str] = Field(None, description="Color for visualization purposes")

    @field_validator('address_type')
    @classmethod
    def validate_address_type(cls, v):
        if v and v not in ["contract", "wallet"]:
            raise ValueError("address_type must be either 'contract' or 'wallet'")
        return v

class TransactionEdge(BaseModel):
    transaction_hash: Optional[str] = Field(None, description="Transaction identifier")
    timestamp: Optional[str] = Field(None, description="ISO 8601 timestamp")
    chain_name: str = Field(description="Chain identifier")
    step: int = Field(description="The iteration number")
    sender_address: str = Field(description="Source address")
    receiver_address: str = Field(description="Destination address")
    category: Optional[str] = Field(None, description="Transaction category")
    subcategory: Optional[str] = Field(None, description="Additional classification")
    protocol_name: Optional[str] = Field(None, description="Protocol used")
    token_address: Optional[str] = Field(None, description="Address of transferred token")
    symbol: Optional[str] = Field(None, description="Symbol of transferred token")
    amount: Optional[int] = Field(None, description="Amount of tokens transferred")
    amount_usd: Optional[float] = Field(None, description="USD value of transfer")
    is_matched: Optional[bool] = Field(None, description="Whether transaction is matched")
    to_transaction_hash: Optional[str] = Field(None, description="Hash of matching transaction")
    to_timestamp: Optional[str] = Field(None, description="Timestamp of matching transaction")
    to_chain_name: Optional[str] = Field(None, description="Chain of matching transaction")
    to_token_address: Optional[str] = Field(None, description="Token address in matching transaction")
    to_symbol: Optional[str] = Field(None, description="Token symbol in matching transaction")
    to_amount: Optional[int] = Field(None, description="Token amount in matching transaction")
    to_amount_usd: Optional[int] = Field(None, description="USD value in matching transaction")
    bridge_metadata: Optional[Dict] = Field(None, description="Additional bridge metadata")
    is_classified: Optional[bool] = Field(None, description="Internal flag to track if transaction has been classified via APIs")
    chain_caip2: Optional[str] = Field(None, description="Chain identifier in CAIP-2 format")
    to_chain_caip2: Optional[str] = Field(None, description="")
    effective_to_chain_name: Optional[str] = Field(None, description="")

class Graph(BaseModel):
    nodes: List[AddressNode] = Field(description="List of address nodes")
    edges: List[TransactionEdge] = Field(description="List of transaction edges")

class StepRequest(BaseModel):
    graph: Graph = Field(description="Updated graph with new nodes and edges")
    metadata: Optional[Dict] = Field(None, description="Metadata for the request")
    graph_name: Optional[str] = Field(None, description="Name of the graph to create (empty if no graph wanted)")
    steps_forward: Optional[int] = Field(1, description="Number of steps to execute forward (default is 1)")

class StepResponse(BaseModel):
    status: str = Field(description="The status of the request")
    results: Optional[Dict] = Field(None, description="The results of the request")
    reactor_url: Optional[str]

class AutoTracing:
    """
    The AutoTracing class provides functionality for tracing cryptocurrency transactions
    through a graph-based approach.
    """

    def __init__(self, api_key: str, reactor_api_key: str = None):
        """
        Initialize the AutoTracing class.

        :param api_key: The API key for the Data Solutions API
        :type api_key: str
        :param api_key: The API key for the Reactor API (optional)
        :type api_key: str
        """
        self.api_key = api_key
        self.reactor_api_key = reactor_api_key
        self._status_code = 0
        self.results = {}
        self._status = "error"
        self.error_message = ""
        self.error_details = ""
        self.exception = UnhandledException()
        self.reactor_url = None

    def step(self, data: Dict[str, Any]) -> "AutoTracing":
        """
        Execute one iteration of cryptocurrency transaction tracing.

        This method uses the AutoTracer engine to analyze transaction flows by:
        1. Processing transfers for target addresses
        2. Classifying new addresses and transactions
        3. Building a transaction graph
        4. Identifying new target addresses for the next iteration

        :param data: The input data containing the graph and optional metadata
        :type data: Dict[str, Any]
        :return: An instance of the AutoTracing class with the results
        :rtype: AutoTracing
        :raises DataSolutionsAPIException: Raises an exception if the API request fails
        :raises DataSolutionsSDKException: Raises an exception if an error occurs during execution
        :raises Exception: Raises an exception if an unexpected error occurs
        """
        try:
            # Validate input data
            validated_data = StepRequest(**data).model_dump()

            step_url = f"{BASE_URL['base_url']}/autotracing/step"

            response = issue_request(
                api_key=self.api_key,
                url=step_url,
                body=validated_data,
                method="POST",
                headers={"X-REACTOR-API-KEY": self.reactor_api_key} if self.reactor_api_key else {},
            )

            # Validate response
            validated_response = StepResponse(**response)

            self._status = validated_response.status
            if self._status == "success":
                self._status_code = 200
                self.results = validated_response.results or {}
                self.reactor_url = validated_response.reactor_url if validated_response.reactor_url else None
            else:
                self._status = "error"
                self.error_message = response.get("message", "Unknown error")
                self.error_details = response.get("details", "")

        except DataSolutionsSDKException as e:
            self._status = "error"
            self.exception = e
            self._status_code = e.status_code
            self.error_message = str(e)
            self.error_details = getattr(e, 'details', '')
        except ValidationError as e:
            # Handle validation errors
            self._status = "error"
            self.exception = UnhandledException(details=e)
            self._status_code = 0
            self.error_message = str(e)
            self.error_details = str(e)
        except Exception as e:
            self._status = "error"
            self.exception = UnhandledException(details=e)
            self._status_code = 500
            self.error_message = str(e)
            self.error_details = str(e)

        return self

    def json(self) -> dict:
        """
        Return results as a JSON.

        :return: Results of the autotracing step as a JSON.
        :rtype: dict
        :raises Exception: Raises an exception if the step resulted in an error.
        """
        if self._status != "error":
            return self.results
        else:
            raise self.exception

    def status_code(self) -> int:
        """
        Get the HTTP status code of the response.

        :return: HTTP status code.
        :rtype: int
        """
        return self._status_code

    def was_successful(self) -> bool:
        """
        Determine if the step executed successfully.

        :return: True if the step was successful, False otherwise.
        :rtype: bool
        """
        if self._status != "error":
            return True
        return False

    def get_reactor_url(self) -> Optional[str]:
        """
        Get the Reactor URL if available.

        :return: Reactor URL or None if not set.
        :rtype: Optional[str]
        """
        return self.reactor_url if self.reactor_url else None
    
    def add_node(self, graph: dict, node: dict) -> dict:
        """
        Add a node to the graph.

        :param graph: The graph to which the node will be added.
        :type graph: dict
        :param node: The node to add.
        :type node: dict
        :return: The updated graph with the new node added.
        """
        validated_graph = Graph(**graph).model_dump()
        validated_node = AddressNode(**node).model_dump()

        validated_graph["nodes"].append(validated_node)

        return validated_graph
    
    def add_edge(self, graph: dict, edge: dict) -> dict:
        """
        Add a edge to the graph.

        :param graph: The graph to which the edge will be added.
        :type graph: dict
        :param edge: The edge to add.
        :type edge: dict
        :return: The updated graph with the new edge added.
        """
        validated_graph = Graph(**graph).model_dump()
        validated_edge = TransactionEdge(**edge).model_dump()

        validated_graph["edges"].append(validated_edge)

        return validated_graph

    def add_reactor_api_key(self, reactor_api_key: str) -> None:
        """
        Add the Reactor API key to the AutoTracing instance.

        :param reactor_api_key: The Reactor API key to add.
        :type reactor_api_key: str
        """
        self.reactor_api_key = reactor_api_key