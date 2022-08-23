import requests
import urllib3

from roboswag.auth import TokenHandler
from roboswag.logger import Logger
from roboswag.validate import Validate

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class APIModel:
    def __init__(
        self,
        base_url,
        verify=False,
        headers=None,
        content_type="application/json",
        proxies=None,
        allow_redirects=True,
        authentication=None,
    ):
        # Set headers from init too (or reuse auth)
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = verify
        self.content_type = content_type
        if content_type is not None:
            self.session.headers = {"Content-Type": content_type}
        self.allow_redirects = allow_redirects
        if proxies is not None:  # TODO urllib have autodetect proxy - allow to use it
            self.session.proxies.update(proxies)
        self.authentication = authentication
        self.logger = Logger()
        self.validate = Validate(self.logger)
        if headers is not None:
            self.session.headers.update(headers)

    def send_request(self, method, url, status=None, headers=None, body=None, query=None, **kwargs):
        headers = self.trim_empty(headers)
        query = self.trim_empty(query)
        auth = self.authentication(**kwargs) if self.authentication is not None else None
        content_type = kwargs.get("content-type", self.content_type)
        if content_type is not None:
            headers["Content-Type"] = content_type

        resp = self.session.request(
            method,
            url=self.base_url + url,
            headers=headers,
            json=body,
            params=query,
            auth=auth,
            allow_redirects=self.allow_redirects,
        )
        # TODO quiet mode
        self.logger.log_request(resp)
        self.logger.log_response(resp)
        if status is not None:
            assert resp.status_code == status, f"Expected return status: {status} but received: {resp.status_code}"
        return resp

    def post(self, *args, **kwargs):
        # TODO handle files upload
        return self.send_request("POST", *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.send_request("GET", *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.send_request("PUT", *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.send_request("DELETE", *args, **kwargs)

    @staticmethod
    def trim_empty(dictionary):
        if dictionary is None:
            return {}
        return {key: value for key, value in dictionary.items() if value is not None}
