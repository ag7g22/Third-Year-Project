from typing import List, Dict, Any
from azure.cosmos import ContainerProxy

class utility():
    """
    Utility class for querying in SQL & building dictionaries.
    """

    def get_queryed_items(self, proxy: ContainerProxy, query: str):
        """
        Returns items from proxy objects' querying.
        """
        return list(proxy.query_items(query=query, enable_cross_partition_query=True))