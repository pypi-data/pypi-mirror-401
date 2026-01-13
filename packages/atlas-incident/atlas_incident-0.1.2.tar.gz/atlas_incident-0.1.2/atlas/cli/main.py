import sys
from atlas.orchestrator.pipeline import run_pipeline
from atlas.io.json_io import to_json
from atlas.schemas.incident import Incident
from atlas_v2.integration.controller import AtlasV2Controller
from atlas_v2.integration.wiring import WORKFLOWS
from atlas_v2.rules.definitions import RULES


def analyze(log_file, service, environment):
    with open(log_file) as f:
        raw_logs = f.read()
    result = run_pipeline(raw_logs=raw_logs, service=service, environment=environment)
    print(to_json(result))
    return result


def respond(log_file, service, environment):
    result = analyze(log_file, service, environment)
    incident = Incident(
        service=result["service"],
        environment=result["environment"],
        severity=result["severity"],
        category=result.get("category"),
        summary=result.get("root_cause", "No summary"),
    )
    controller = AtlasV2Controller(rules=RULES, workflows=WORKFLOWS)
    out = controller.handle_incident(incident)
    print("\n=== ATLAS v2 RESULT ===")
    print("Priority:", out["priority"].priority)
    print("Actions:", out["actions"])


def main():
    if len(sys.argv) != 5:
        print("Usage: atlas <analyze|respond> <log> <service> <env>")
        return
    cmd, log, service, env = sys.argv[1:]
    if cmd == "analyze":
        analyze(log, service, env)
    elif cmd == "respond":
        respond(log, service, env)
    else:
        print("Unknown command")
