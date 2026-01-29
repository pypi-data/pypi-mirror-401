from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport

class SecParseClient:
   def __init__(self, api_key: str, url: str = "https://secparse.com/api/graphql", ws_url: str = "wss://secparse.com/api/graphql/ws") -> None:
      self.api_key = api_key
      self.url = url
      self.ws_url = ws_url
      
      self.http_transport = AIOHTTPTransport(url=self.url, headers={"X-Api-Key": self.api_key})
      self.ws_transport = WebsocketsTransport(url=self.ws_url, headers={"X-Api-Key": self.api_key})

      self.http_client = Client(transport=self.http_transport)
      self.ws_client = Client(transport=self.ws_transport)

   async def query(self, query: str, variables: dict | None = None):
      async with self.http_client as session:
         result = await session.execute(gql(query), variable_values=variables)
         return result
   
   async def subscribe(self, query: str, variables: dict | None = None):
      async with self.ws_client as session:
         async for result in session.subscribe(gql(query), variable_values=variables):
            yield result