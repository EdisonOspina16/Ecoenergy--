def response_status(actor):
    return actor.recall("response").status_code


def response_json(actor):
    return actor.recall("response").get_json()
