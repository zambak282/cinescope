import json
import logging
import os
import time

from pydantic import BaseModel
from constants.logger_colors import RESET, GREEN, RED


class CustomRequester:
    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.headers = self.base_headers.copy()
        self.session.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)

    def _update_session_headers(self, headers: dict):
        self.session.headers.update(headers)

    def _reset_headers(self):
        self.session.headers = self.base_headers.copy()

    def send_request(self, method, endpoint, need_logging=True, **kwargs):
        url = f"{self.base_url}{endpoint}"

        data = kwargs.get("json")
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))
            kwargs["json"] = data

        start_time = time.time()
        response = self.session.request(method, url, **kwargs)
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        if need_logging:
            self.log_request_and_response(response, elapsed_ms)

        return response

    def log_request_and_response(self, response, elapsed_ms):
        """
        Логгирование запросов и ответов. Настройки логгирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хэдэеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        :param elapsed_ms: Время, которое занял запрос
        """
        try:
            request = response.request
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text
            if not is_success:
                self.logger.info(f"\tRESPONSE:"
                                 f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                                 f"\nELAPSED MS: {RED}{elapsed_ms}{RESET}"
                                 f"\nDATA: {RED}{response_data}{RESET}")
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")
