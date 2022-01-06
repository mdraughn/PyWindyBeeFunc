import logging
from functools import lru_cache

import azure.functions as func

from SpellingBeePlus import SpellingBeePlus

_context = None

def main(req: func.HttpRequest) -> func.HttpResponse:
    global _context
    logging.info('Python HTTP trigger function processed a request.')

    pattern = req.route_params.get('pattern')
    if pattern:
        content = build_word_list(pattern)
        return func.HttpResponse(content, headers={})
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

@lru_cache(maxsize=10)
def build_word_list(pattern):
    global _context
    if _context is None:
        _context = SpellingBeePlus()
    words = [w + '\n' for w in _context.get_words(pattern)]
    content = ''.join(words)
    return content