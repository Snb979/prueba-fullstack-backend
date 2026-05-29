from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt

import time
import os


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "mysecretkey"
)

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)


class RequestLoggerMiddleware(
    BaseHTTPMiddleware
):

    async def dispatch(
        self,
        request,
        call_next
    ):

        start_time = time.time()

        user_email = "anonymous"
        role = "unknown"

        auth = request.headers.get(
            "Authorization"
        )

        if auth:

            try:

                token = auth.replace(
                    "Bearer ",
                    ""
                )

                payload = jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[ALGORITHM]
                )

                user_email = payload.get(
                    "email",
                    "unknown"
                )

                role = payload.get(
                    "role",
                    "unknown"
                )

            except:
                pass

        response = await call_next(
            request
        )

        process_time = round(
            time.time() - start_time,
            4
        )

        print(
            f"{request.method} "
            f"{request.url.path} "
            f"{response.status_code} "
            f"user={user_email} "
            f"role={role} "
            f"{process_time}s"
        )

        return response