from semantha_sdk.model.document_class_node import DocumentClassNode
from semantha_sdk.model.document_class_node import DocumentClassNodeSchema
from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint
from typing import List

class TreeEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/domains/{domainname}/documentclasses/tree"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/tree"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def get(
        self,
        fields: str = None,
    ) -> List[DocumentClassNode]:
        """
        
        Args:
        fields str: 
        """
        q_params = {}
        if fields is not None:
            q_params["fields"] = fields
    
        return self._session.get(self._endpoint, q_params=q_params, headers=RestClient.to_header(MediaType.JSON)).execute().to(DocumentClassNodeSchema)

    
    
    
    