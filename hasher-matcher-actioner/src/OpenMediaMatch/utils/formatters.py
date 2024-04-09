from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Outputs logs in a JSON format. This is useful because it makes logs easily parse-able by Datadog.
    """

    def add_fields(self, log_record, record, message_dict):
        log_record["level"] = record.__dict__.get("levelname")
        log_record["timestamp"] = self.formatTime(record)
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)


class GunicornAccessFormatter(CustomJsonFormatter):
    """
    Outputs logs in a JSON format. This is useful because it makes logs easily parse-able by Datadog.
    """

    def add_fields(self, log_record, record, message_dict):
        url = record.args["U"]
        if record.args["q"]:
            url += f"?{record.args['q']}"
        log_record["remote_ip"] = record.args["h"]
        log_record["method"] = record.args["m"]
        log_record["path"] = url
        log_record["status"] = str(record.args["s"])
        log_record["user_agent"] = record.args["a"]
        log_record["referer"] = record.args["f"]
        log_record["duration_in_ms"] = record.args["M"]
        log_record["pid"] = record.args["p"]
        super(GunicornAccessFormatter, self).add_fields(log_record, record, message_dict)

