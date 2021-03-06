import slack

sc = None


def get_sc(config):
    global sc
    if sc is None:
        sc = slack.WebClient(token=config["SLACK"]["token"])
    return sc


def post_message(config, msg):
    get_sc(config).chat_postMessage(
      channel=config["SLACK"]["channel"],
      text=msg
    )



