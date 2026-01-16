# Standard library imports
import logging
import uuid
from typing import Optional
from urllib.parse import urljoin

# Third party imports
from pydantic import BaseModel

# Project imports
from mindgard.api.recon.recon_prompt_events import ReconPromptEventsClient
from mindgard.api.recon.types import GetReconRequest, StartReconRequest, StartReconResponse

from ..exceptions import ClientException


class ReconResult(BaseModel):
    total: int
    total_detected: int
    results: dict[str, int]


class SystemPromptExtractResult(BaseModel):
    id: uuid.UUID
    state: str
    result: Optional[ReconResult] = None
    reason: Optional[str] = None
    recommendation: Optional[str] = None
    project_id: str


class ReconSystemPromptExtractionClient(ReconPromptEventsClient):
    def __init__(self, base_url: str, access_token: str, project_id: str):
        super().__init__(base_url, access_token, project_id)
        self._recon_system_prompt_extraction_url = urljoin(base_url + "/", "recon/system_prompt_extraction")
        self._project_id = project_id

    def start_system_prompt_extraction(self, request: StartReconRequest) -> StartReconResponse:
        """
        Start a system prompt extraction reconnaissance process with the Mindgard service

        Args:
            request (StartReconRequest): Info (project ID) connecting this operation to a target name

        Raises:
            ClientException: Raised if the Mindgard service returns an error

        Returns:
            StartReconResponse: Mindgard service response from the start request
        """
        response = self._session.post(
            self._recon_system_prompt_extraction_url,
            params={"project_id": self._project_id},
            data=request.model_dump_json(),
        )

        if response.status_code != 201:
            logging.debug(f"Failed to start recon: {response.json()} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)
        try:
            return StartReconResponse.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing StartReconResponse", response.status_code) from e

    def get_system_prompt_extraction_result(self, request: GetReconRequest) -> Optional[SystemPromptExtractResult]:
        """
        Get the system prompt extraction reconnaissance result from the Mindgard service

        Args:
            request (GetReconRequest): Info connecting this operation to a reconnaissance session
        Raises:
            ClientException: Raised if the Mindgard service returns an error
        Returns:
            Optional[SystemPromptExtractResult]: Mindgard service response from the get request
        """
        response = self._session.get(
            self._recon_system_prompt_extraction_url,
            params={"recon_id": str(request.recon_id), "project_id": self._project_id},
        )

        if response.status_code == 404:
            logging.debug(f"No reconnaissance found for recon_id={request.recon_id}: {response.text}")
            return None

        if response.status_code != 200:
            logging.debug(f"Failed to get recon result: {response.text} - {response.status_code}")
            raise ClientException(response.json(), response.status_code)

        try:
            return SystemPromptExtractResult.model_validate(response.json())
        except Exception as e:
            raise ClientException("Problem parsing SystemPromptExtractResult", response.status_code) from e
