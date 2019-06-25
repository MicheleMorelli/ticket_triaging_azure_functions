import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('It looks like that I received some tickets!')
    content = req.get_json()
    num = content["tickets_count"]

    return func.HttpResponse(
         f"\n\nI found {num} new tickets\n\n",
         status_code=200
    )
