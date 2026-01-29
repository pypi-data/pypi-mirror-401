from semantha_sdk.rest.rest_client import MediaType
from semantha_sdk.rest.rest_client import RestClient, RestEndpoint

class MarkdownEndpoint(RestEndpoint):
    """
    Class to access resource: "/api/domains/{domainname}/referencedocuments/{documentid}/markdown"
    author semantha, this is a generated class do not change manually! 
    
    """

    @property
    def _endpoint(self) -> str:
        return self._parent_endpoint + "/markdown"

    def __init__(
        self,
        session: RestClient,
        parent_endpoint: str,
    ) -> None:
        super().__init__(session, parent_endpoint)

    def get_as_plain_text(
        self,
    ) -> str:
        """
        Returns one reference document by ID as markdown
        Args:
            """
        q_params = {}
    
        return self._session.get(self._endpoint, q_params=q_params, headers=RestClient.to_header(MediaType.TEXT_PLAIN)).execute().as_str()

    
    
    
    