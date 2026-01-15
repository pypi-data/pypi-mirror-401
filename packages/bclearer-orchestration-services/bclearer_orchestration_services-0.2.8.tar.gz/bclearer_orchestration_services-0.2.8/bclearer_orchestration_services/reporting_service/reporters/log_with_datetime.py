from bclearer_orchestration_services.datetime_service.time_helpers.time_getter import (
    now_time_as_string,
)
from bclearer_orchestration_services.reporting_service.reporters.log_file import (
    LogFiles,
)
from bclearer_orchestration_services.reporting_service.reporters.nf_kafka_producers import (
    NfKafkaProducers,
)


def log_message(message: str):
    date_stamped_message = (
        now_time_as_string()
        + ": "
        + message
    )

    print(date_stamped_message)

    try:
        LogFiles.write_to_log_file(
            message=date_stamped_message
            + "\n",
        )
    except Exception as log_file_exception:
        import sys

        print(
            f"ERROR: Failed to write log message to file: {log_file_exception}",
            file=sys.stderr,
        )

    try:
        NfKafkaProducers.log_to_kafka_producer(
            message=date_stamped_message,
        )
    except Exception as kafka_exception:
        import sys

        print(
            f"ERROR: Failed to write log message to Kafka: {kafka_exception}",
            file=sys.stderr,
        )
