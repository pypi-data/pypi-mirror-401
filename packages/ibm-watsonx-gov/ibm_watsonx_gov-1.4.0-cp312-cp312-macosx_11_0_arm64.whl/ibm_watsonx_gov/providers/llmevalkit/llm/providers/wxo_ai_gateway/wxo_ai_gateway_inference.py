# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# Licensed Materials - Property of IBM
# 5737-H76, 5900-A3Q
# © Copyright IBM Corp. 2025  All Rights Reserved.
# US Government Users Restricted Rights - Use, duplication or disclosure restricted by
# GSA ADPSchedule Contract with IBM Corp.
# ----------------------------------------------------------------------------------------------------

import asyncio
import json
import logging
import time
import weakref
from typing import Dict

import aiohttp
import requests

logger = logging.getLogger(__name__)


class WxoAIGatewayInference():
    RETRY_AFTER_STATUS_CODES = [502, 503, 504]
    RETRY_COUNT = 3
    BACK_OFF_FACTOR = 1

    def __init__(self, api_key: str, url: str) -> None:
        self.api_key = api_key
        self.url = url
        self.session: aiohttp.ClientSession = None
        self._loop: asyncio.AbstractEventLoop = None
        weakref.finalize(self, self._finalize_cleanup, self)

    async def get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session for the current event loop."""
        try:
            current_loop = asyncio.get_running_loop()
        except Exception:
            raise logger.debug("get_session must be called from within an async context")

        # Check if session exists and is valid for current loop
        if (self.session is None or
                self.session.closed or
                self._loop is not current_loop):

            # Close old session if it exists and is from a different loop
            if self.session and not self.session.closed:
                try:
                    await self.session.close()
                except Exception as e:
                    logger.debug(f"Error closing old session: {e}")

            # Create new session for current loop
            self.session = aiohttp.ClientSession()
            self._loop = current_loop
            logger.debug(f"Created new session for event loop {id(current_loop)}")

        return self.session

    @staticmethod
    def _finalize_cleanup(self):
        """
        Called automatically when the object is garbage-collected.
        This function is synchronous, so it schedules async cleanup properly.
        """
        if self.session and not self.session.closed:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.session.close())
                else:
                    loop.run_until_complete(self.session.close())
            except Exception as e:
                logger.info(f"Error during cleanup: {e}")

    def chat(self, messages: list[Dict], **kwargs) -> dict:
        """
        Sync chat method.
        Args:
            messages (list[Dict]): List of messages to send.

        Returns:
            dict: Response from the API.
        """
        payload_data = {
            "messages": messages
        }
        response = self._post(payload_data)
        return response

    async def achat(self, messages: list[Dict], **kwargs) -> dict:
        """
        async implementation of the chat method.

        Args:
            messages (list[Dict]): List of messages to send.

        Returns:
            dict: Response from the API.
        """
        payload_data = {
            "messages": messages
        }
        response = await self._apost(payload_data)
        return response

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "accept": "application/json",
            "IAM-API_KEY": self.api_key
        }

    def _post(self, payload_data: dict) -> dict:
        """
        Make a synchronous POST request to the Wxo AI Gateway API.

        Args:
            payload_data: Dictionary containing the request payload

        Returns:
            dict: JSON response from the API

        Raises:
            requests.HTTPError: If the request fails after all retries
            json.JSONDecodeError: If response cannot be parsed as JSON
        """
        headers = self._get_headers()

        for attempt in range(self.RETRY_COUNT):
            try:
                response = requests.post(
                    url=self.url,
                    json=payload_data,
                    headers=headers,
                    timeout=30.0,
                    verify=False
                )

                response_status = response.status_code

                if response_status == 200:
                    return response.json()

                if response_status in self.RETRY_AFTER_STATUS_CODES and attempt < self.RETRY_COUNT - 1:
                    backoff_time = self.BACK_OFF_FACTOR * (2 ** attempt)
                    logger.info(
                        f"Received status {response_status}, retrying in {backoff_time}s (attempt {attempt + 1}/{self.RETRY_COUNT})...")
                    time.sleep(backoff_time)
                    continue

                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                if attempt < self.RETRY_COUNT - 1:
                    backoff_time = self.BACK_OFF_FACTOR * (2 ** attempt)
                    logger.info(
                        f"Request failed with {type(e).__name__}, retrying in {backoff_time}s (attempt {attempt + 1}/{self.RETRY_COUNT})...")
                    time.sleep(backoff_time)
                    continue
                else:
                    raise

    async def _apost(self, payload_data: dict) -> dict:
        """
        Make an asynchronous POST request to the Wxo AI Gateway API.

        Args:
            payload_data: Dictionary containing the request payload

        Returns:
            dict: JSON response from the API

        Raises:
            aiohttp.ClientError: If the request fails after all retries
            json.JSONDecodeError: If response cannot be parsed as JSON
        """
        headers = self._get_headers()
        session = await self.get_session()
        for attempt in range(self.RETRY_COUNT):
            try:
                async with session.post(
                    url=self.url,
                    json=payload_data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30.0),
                    ssl=False
                ) as response:
                    response_status = response.status

                    if response_status == 200:
                        return await response.json()

                    if response_status in self.RETRY_AFTER_STATUS_CODES and attempt < self.RETRY_COUNT - 1:
                        backoff_time = self.BACK_OFF_FACTOR * \
                            (2 ** attempt)
                        logger.info(
                            f"Received status {response_status}, retrying in {backoff_time}s (attempt {attempt + 1}/{self.RETRY_COUNT})...")
                        await asyncio.sleep(backoff_time)
                        continue

                    return await response.json()

            except aiohttp.ClientError as e:
                if attempt < self.RETRY_COUNT - 1:
                    backoff_time = self.BACK_OFF_FACTOR * (2 ** attempt)
                    logger.info(
                        f"Request failed with {type(e).__name__}, retrying in {backoff_time}s (attempt {attempt + 1}/{self.RETRY_COUNT})...")
                    await asyncio.sleep(backoff_time)
                    continue
                else:
                    raise
