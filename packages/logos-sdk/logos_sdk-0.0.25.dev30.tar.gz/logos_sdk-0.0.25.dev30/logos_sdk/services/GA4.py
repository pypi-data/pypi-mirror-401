from requests.exceptions import Timeout
from typing import List, Union, Dict
from logos_sdk.services import get_headers, get_retry_session
from http import HTTPStatus
from dotenv import load_dotenv
import os
import time
import random


class GA4ServiceException(Exception):
    pass


class GA4Service:
    def __init__(self, url=None):
        load_dotenv()
        self.session = get_retry_session()
        self._URL = url or os.environ.get("GA4_SERVICE_PATH")
        self._RUN_REPORT = self._URL + "/run-report"
        self._GET_ACCESSIBLE_ACCOUNTS = self._URL + "/accessible-accounts"
        self._GET_ACCOUNT_ACCESSIBILITY = self._URL + "/get-account-accessibility"

    def get_accessible_accounts(
            self,
            secret_id: str,
    ) -> List[Dict]:
        body = {
            "secret_id": secret_id,
        }

        header = get_headers(self._GET_ACCESSIBLE_ACCOUNTS)
        response = self.session.request(
            "post", url=self._GET_ACCESSIBLE_ACCOUNTS, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise GA4ServiceException(response.content)

    def get_account_accessibility(self, secret_id: str, account_id: str) -> bool:
        """
        Gets account accessibility
        :param secret_id: The ID of the secret in secret manager
        :param account_id: The ID of the account.
        :return: True if account has access
        """
        body = {"secret_id": secret_id, "account_id": account_id}
        header = get_headers(self._GET_ACCOUNT_ACCESSIBILITY)
        response = self.session.request(
            "post", url=self._GET_ACCOUNT_ACCESSIBILITY, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise GA4ServiceException(response.content)

    def run_report(self, account_id, secret_id, start_date, end_date, dimensions, metrics, filters=None,
                   order_by_metric=None):
        """
        Runs report
        :param account_id: The ID of the account,
        :param secret_id: The ID of the secret in secret manager
        :param start_date: report start date in format "YYYY-MM-DD"
        :param end_date: report end date in format "YYYY-MM-DD"
        :param dimensions: The dimesions for the query
        :param metrics: The metrics for the query
        :param filters: The filters for the query
        :param order_by_metric: The metric to order by
        :return: report result
        """
        header = get_headers(self._RUN_REPORT)
        body = {
            "property_id": account_id,
            "secret_id": secret_id,
            "start_date": start_date,
            "end_date": end_date,
            "dimensions": dimensions,
            "metrics": metrics,
        }
        if filters is not None:
            body["filters"] = filters
        if order_by_metric is not None:
            body['order_by_metric'] = order_by_metric

        response = self.session.request(
            "post", url=self._RUN_REPORT, json=body, headers=header
        )

        if response.status_code == HTTPStatus.OK:
            service_response = response.json()
            return service_response["data"]
        else:
            raise GA4ServiceException(response.content)
