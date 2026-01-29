# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.technology import graph_find_path_params, graph_get_overlap_params, graph_get_subgraph_params
from ...types.technology.graph_find_path_response import GraphFindPathResponse
from ...types.technology.graph_get_overlap_response import GraphGetOverlapResponse
from ...types.technology.graph_get_subgraph_response import GraphGetSubgraphResponse

__all__ = ["GraphResource", "AsyncGraphResource"]


class GraphResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> GraphResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return GraphResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> GraphResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return GraphResourceWithStreamingResponse(self)

    def find_path(
        self,
        *,
        source: str,
        target: str,
        max_depth: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GraphFindPathResponse:
        """
        Find shortest path between two technology communities using BFS.

        **Algorithm:**

        - Breadth-first search with cycle detection
        - Returns shortest path by number of hops
        - Uses recursive CTE for graph traversal

        **Query Parameters:**

        - `source`: Starting community ID (required)
        - `target`: Destination community ID (required)
        - `max_depth`: Maximum path length (default: 5, max: 10)

        **Returns:**

        - path_communities[]: Array of community IDs in path
        - path_length: Number of hops
        - total_weight: Sum of edge weights along path
        - path_details: JSONB array with community summaries and edge weights

        **Performance:**

        - Limited to max depth of 10 to prevent long-running queries
        - Query timeout: 30 seconds

        **Response Codes:**

        - 200: Success (path found)
        - 401: Unauthorized
        - 404: No path found between communities

        Args:
          source: Source community UUID

          target: Target community UUID

          max_depth: Maximum path depth

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/technology/graph/path",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "source": source,
                        "target": target,
                        "max_depth": max_depth,
                    },
                    graph_find_path_params.GraphFindPathParams,
                ),
            ),
            cast_to=GraphFindPathResponse,
        )

    def get_overlap(
        self,
        *,
        community_id1: str,
        community_id2: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GraphGetOverlapResponse:
        """
        Analyze topic overlap between two technology communities.

        **Overlap Metrics:**

        - Jaccard similarity: shared_topics / (topics1 + topics2 - shared_topics)
        - Shared topics with details (JSONB)
        - Unique topic counts for each community

        **Returns:**

        - community1_id, community2_id
        - shared_topics[]: JSONB array of shared topics
        - overlap_score: Jaccard similarity (0-1)
        - unique_topics_1, unique_topics_2: Topics unique to each community
        - shared_topics_count: Number of shared topics

        **Use Cases:**

        - Identify research overlap
        - Find potential collaboration opportunities
        - Measure community similarity

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Community not found

        Args:
          community_id1: First community UUID

          community_id2: Second community UUID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/technology/graph/overlap",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "community_id1": community_id1,
                        "community_id2": community_id2,
                    },
                    graph_get_overlap_params.GraphGetOverlapParams,
                ),
            ),
            cast_to=GraphGetOverlapResponse,
        )

    def get_subgraph(
        self,
        *,
        community_ids: SequenceNotStr[str],
        depth: int | Omit = omit,
        min_edge_strength: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GraphGetSubgraphResponse:
        """
        Extract N-hop neighborhood subgraph around specified communities.

        **Algorithm:**

        - Expands from seed communities to depth N
        - Filters edges by minimum composite score
        - Returns nodes, edges, and graph statistics

        **Request:**

        - `community_ids`: List of community IDs (seed nodes)
        - `depth`: How many hops to expand (max: 5)
        - `min_edge_strength`: Minimum composite score filter

        **Returns:**

        - nodes[]: JSONB array of community nodes
        - edges[]: JSONB array of edges with weights
        - stats: Graph statistics (node_count, edge_count, avg_connectivity)

        **Performance:**

        - Max depth limited to 5
        - Use min_edge_strength to reduce graph size

        **Response Codes:**

        - 200: Success
        - 400: Invalid parameters
        - 401: Unauthorized

        Args:
          community_ids: Community UUIDs to center subgraph around

          depth: Neighborhood depth

          min_edge_strength: Minimum edge composite score

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/technology/graph/subgraph",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "community_ids": community_ids,
                        "depth": depth,
                        "min_edge_strength": min_edge_strength,
                    },
                    graph_get_subgraph_params.GraphGetSubgraphParams,
                ),
            ),
            cast_to=GraphGetSubgraphResponse,
        )


class AsyncGraphResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncGraphResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/evrimai/evrim-python#accessing-raw-response-data-eg-headers
        """
        return AsyncGraphResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncGraphResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/evrimai/evrim-python#with_streaming_response
        """
        return AsyncGraphResourceWithStreamingResponse(self)

    async def find_path(
        self,
        *,
        source: str,
        target: str,
        max_depth: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GraphFindPathResponse:
        """
        Find shortest path between two technology communities using BFS.

        **Algorithm:**

        - Breadth-first search with cycle detection
        - Returns shortest path by number of hops
        - Uses recursive CTE for graph traversal

        **Query Parameters:**

        - `source`: Starting community ID (required)
        - `target`: Destination community ID (required)
        - `max_depth`: Maximum path length (default: 5, max: 10)

        **Returns:**

        - path_communities[]: Array of community IDs in path
        - path_length: Number of hops
        - total_weight: Sum of edge weights along path
        - path_details: JSONB array with community summaries and edge weights

        **Performance:**

        - Limited to max depth of 10 to prevent long-running queries
        - Query timeout: 30 seconds

        **Response Codes:**

        - 200: Success (path found)
        - 401: Unauthorized
        - 404: No path found between communities

        Args:
          source: Source community UUID

          target: Target community UUID

          max_depth: Maximum path depth

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/technology/graph/path",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "source": source,
                        "target": target,
                        "max_depth": max_depth,
                    },
                    graph_find_path_params.GraphFindPathParams,
                ),
            ),
            cast_to=GraphFindPathResponse,
        )

    async def get_overlap(
        self,
        *,
        community_id1: str,
        community_id2: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GraphGetOverlapResponse:
        """
        Analyze topic overlap between two technology communities.

        **Overlap Metrics:**

        - Jaccard similarity: shared_topics / (topics1 + topics2 - shared_topics)
        - Shared topics with details (JSONB)
        - Unique topic counts for each community

        **Returns:**

        - community1_id, community2_id
        - shared_topics[]: JSONB array of shared topics
        - overlap_score: Jaccard similarity (0-1)
        - unique_topics_1, unique_topics_2: Topics unique to each community
        - shared_topics_count: Number of shared topics

        **Use Cases:**

        - Identify research overlap
        - Find potential collaboration opportunities
        - Measure community similarity

        **Response Codes:**

        - 200: Success
        - 401: Unauthorized
        - 404: Community not found

        Args:
          community_id1: First community UUID

          community_id2: Second community UUID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/technology/graph/overlap",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "community_id1": community_id1,
                        "community_id2": community_id2,
                    },
                    graph_get_overlap_params.GraphGetOverlapParams,
                ),
            ),
            cast_to=GraphGetOverlapResponse,
        )

    async def get_subgraph(
        self,
        *,
        community_ids: SequenceNotStr[str],
        depth: int | Omit = omit,
        min_edge_strength: float | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> GraphGetSubgraphResponse:
        """
        Extract N-hop neighborhood subgraph around specified communities.

        **Algorithm:**

        - Expands from seed communities to depth N
        - Filters edges by minimum composite score
        - Returns nodes, edges, and graph statistics

        **Request:**

        - `community_ids`: List of community IDs (seed nodes)
        - `depth`: How many hops to expand (max: 5)
        - `min_edge_strength`: Minimum composite score filter

        **Returns:**

        - nodes[]: JSONB array of community nodes
        - edges[]: JSONB array of edges with weights
        - stats: Graph statistics (node_count, edge_count, avg_connectivity)

        **Performance:**

        - Max depth limited to 5
        - Use min_edge_strength to reduce graph size

        **Response Codes:**

        - 200: Success
        - 400: Invalid parameters
        - 401: Unauthorized

        Args:
          community_ids: Community UUIDs to center subgraph around

          depth: Neighborhood depth

          min_edge_strength: Minimum edge composite score

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/technology/graph/subgraph",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "community_ids": community_ids,
                        "depth": depth,
                        "min_edge_strength": min_edge_strength,
                    },
                    graph_get_subgraph_params.GraphGetSubgraphParams,
                ),
            ),
            cast_to=GraphGetSubgraphResponse,
        )


class GraphResourceWithRawResponse:
    def __init__(self, graph: GraphResource) -> None:
        self._graph = graph

        self.find_path = to_raw_response_wrapper(
            graph.find_path,
        )
        self.get_overlap = to_raw_response_wrapper(
            graph.get_overlap,
        )
        self.get_subgraph = to_raw_response_wrapper(
            graph.get_subgraph,
        )


class AsyncGraphResourceWithRawResponse:
    def __init__(self, graph: AsyncGraphResource) -> None:
        self._graph = graph

        self.find_path = async_to_raw_response_wrapper(
            graph.find_path,
        )
        self.get_overlap = async_to_raw_response_wrapper(
            graph.get_overlap,
        )
        self.get_subgraph = async_to_raw_response_wrapper(
            graph.get_subgraph,
        )


class GraphResourceWithStreamingResponse:
    def __init__(self, graph: GraphResource) -> None:
        self._graph = graph

        self.find_path = to_streamed_response_wrapper(
            graph.find_path,
        )
        self.get_overlap = to_streamed_response_wrapper(
            graph.get_overlap,
        )
        self.get_subgraph = to_streamed_response_wrapper(
            graph.get_subgraph,
        )


class AsyncGraphResourceWithStreamingResponse:
    def __init__(self, graph: AsyncGraphResource) -> None:
        self._graph = graph

        self.find_path = async_to_streamed_response_wrapper(
            graph.find_path,
        )
        self.get_overlap = async_to_streamed_response_wrapper(
            graph.get_overlap,
        )
        self.get_subgraph = async_to_streamed_response_wrapper(
            graph.get_subgraph,
        )
