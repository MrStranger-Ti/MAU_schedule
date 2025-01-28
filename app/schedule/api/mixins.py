from rest_framework import status
from rest_framework.response import Response

from schedule.parser import ParserResponse


class ParserResponseViewMixin:
    def get_response(self, parser_response: ParserResponse) -> Response:
        if not parser_response.success:
            if parser_response.response is None:
                return Response(
                    data={"detail": parser_response.error},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

            return Response(
                data={"detail": parser_response.error},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(data=parser_response.data, status=status.HTTP_200_OK)
