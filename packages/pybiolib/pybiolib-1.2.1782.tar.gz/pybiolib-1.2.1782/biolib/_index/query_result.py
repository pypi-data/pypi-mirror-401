import json
from typing import Any, Dict, Iterator, List, Optional, Union
from urllib.parse import urlencode

from biolib import api
from biolib._internal.http_client import HttpResponse
from biolib.biolib_errors import BioLibError


class IndexQueryResult:
    """Result wrapper for index query responses."""

    def __init__(self, response: HttpResponse, data_format: str):
        self._response = response
        self._data_format = data_format
        self._json_data: Optional[Dict[str, Any]] = None
        if data_format == 'json':
            self._json_data = self._response.json()

    def iter_rows(self) -> Iterator[Dict[str, Any]]:
        """Return an iterator over the rows in the query result.

        Returns:
            Iterator[Dict[str, Any]]: An iterator yielding each row as a dictionary.
        """
        if self._json_data is None:
            raise BioLibError('iter_rows() is only available when data_format is "json"')
        return iter(self._json_data['data'])


def query_index(
    query: str,
    data: Optional[Union[List[Dict[str, Any]], bytes]] = None,
    data_format: str = 'json',
) -> IndexQueryResult:
    """Query the BioLib index with a SQL-like query.

    Args:
        query: The SQL query string to execute.
        data: Optional input data. If data_format is "json", this should be a list of
            dictionaries that will be JSON encoded. Otherwise, pass raw bytes.
        data_format: The format for the query. Defaults to "json".

    Returns:
        IndexQueryResult: A result object wrapping the query response.

    Raises:
        BioLibError: If the query fails or returns a non-successful HTTP status code.
    """
    data_format = data_format.lower()

    query_params: Dict[str, str] = {'default_format': data_format}
    if data is not None:
        query_params['query'] = query

    path = 'proxy/index/?' + urlencode(query_params)

    if data is not None:
        if data_format == 'json':
            body: bytes = '\n'.join(json.dumps(item, ensure_ascii=False) for item in data).encode('utf-8')
        else:
            body = data  # type: ignore[assignment]
    else:
        body = query.encode('utf-8')

    response = api.client.post(
        path=path,
        data=body,
        headers={'Content-Type': 'text/plain; charset=utf-8'},
    )

    if response.status_code < 200 or response.status_code >= 300:
        raise BioLibError(f'Index query failed with status code {response.status_code}: {response.text}')

    return IndexQueryResult(response, data_format)
