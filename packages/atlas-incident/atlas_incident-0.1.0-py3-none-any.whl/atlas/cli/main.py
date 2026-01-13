import sys
from atlas.orchestrator.pipeline import run_pipeline
from atlas.io.json_io import to_json




def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: atlas <log_file> <service> <environment>")
        sys.exit(1)

    log_file, service, environment = sys.argv[1:]

    with open(log_file, "r") as f:
        raw_logs = f.read()

    result = run_pipeline(
        raw_logs=raw_logs,
        service=service,
        environment=environment,
    )

    print(to_json(result))
