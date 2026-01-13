from atlas.schemas.incident import Incident
from atlas_v2.priority.scorer import PriorityScorer
from atlas_v2.rules.engine import RuleEngine
from atlas_v2.workflow.engine import WorkflowEngine
from atlas_v2.state.store import WorkflowState
from atlas_v2.audit.trail import AuditTrail
from atlas_v2.actions.executor import ActionExecutor


class AtlasV2Controller:
    def __init__(self, rules, workflows):
        self.scorer = PriorityScorer()
        self.rule_engine = RuleEngine(rules)
        self.workflows = workflows
        self.audit = AuditTrail()
        self.executor = ActionExecutor()
        self.workflow_engine = WorkflowEngine(self.audit)

    def handle_incident(self, incident: Incident):
        # 1. priority
        priority_decision = self.scorer.score(incident)

        # 2. rules
        fired_rules = self.rule_engine.evaluate(
            incident, priority_decision.priority
        )

        results = []

        # 3. workflows
        for rule in fired_rules:
            workflow = self.workflows.get(rule.rule_id)
            if not workflow:
                continue

            state = WorkflowState(workflow.workflow_id)
            while not state.completed:
                prev_step = state.current_step
                state = self.workflow_engine.step(workflow, state)

                if state.current_step != prev_step:
                    step_name = workflow.steps[prev_step].name
                    self.executor.execute(step_name)

            results.append(workflow.workflow_id)

        return {
            "priority": priority_decision,
            "rules": fired_rules,
            "actions": self.executor.performed,
            "audit": self.audit.events,
            "workflows": results,
        }
