import logging
import azure.functions as func

from SpellingBeePlus import SpellingBeePlus


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    pattern = req.route_params.get('pattern')
    if pattern:
        bee = SpellingBeePlus()
        words = [w+'\n' for w in bee.get_words(pattern)]
        return func.HttpResponse(''.join(words))
    else:
        return func.HttpResponse(
            "Please pass a pattern as the next component of the path",
            status_code=400
        )


    # name = req.route_params.get('name')
    # if name:
    #     return func.HttpResponse(f"Hello {name}!")
    # else:
    #     return func.HttpResponse(
    #         "Please pass a name as the next component of the path",
    #         status_code=400
    #     )