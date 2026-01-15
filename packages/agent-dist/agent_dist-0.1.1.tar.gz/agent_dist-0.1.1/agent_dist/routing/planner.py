from collections import defaultdict, deque
from .models import ExecutionPlan, ExecutionStep, MultiRouteDecision


class PlannerAgent:
    def plan(self, decision: MultiRouteDecision) -> ExecutionPlan:
        if decision.mode == "react":
            return ExecutionPlan(mode="react", steps=[])

        if decision.mode != "agents":
            return ExecutionPlan(mode="llm_only", steps=[])

        agents = self._flatten(decision)
        graph, indegree = self._build_graph(agents)

        if all(d == 0 for d in indegree.values()):
            return ExecutionPlan(
                mode="parallel",
                steps=[self._to_step(a) for a in agents],
            )

        ordered = self._toposort(graph, indegree, agents)

        if not ordered:
            raise RuntimeError("Planner failed to produce execution order")

        return ExecutionPlan(
            mode="chain",
            steps=[self._to_step(a) for a in ordered],
        )

    def _build_graph(self, agents):
        graph = defaultdict(set)
        indegree = {a["agent_name"]: 0 for a in agents}
        providers = defaultdict(set)

        for a in agents:
            for p in a["provides"]:
                providers[p].add(a["agent_name"])

        for b in agents:
            for r in b["requires"]:
                for src in providers.get(r, []):
                    if src != b["agent_name"]:
                        if b["agent_name"] not in graph[src]:
                            graph[src].add(b["agent_name"])
                            indegree[b["agent_name"]] += 1

        return graph, indegree

    def _toposort(self, graph, indegree, agents):
        nodes = {a["agent_name"]: a for a in agents}
        q = deque([n for n, d in indegree.items() if d == 0])
        ordered = []

        while q:
            n = q.popleft()
            ordered.append(nodes[n])
            for m in graph.get(n, []):
                indegree[m] -= 1
                if indegree[m] == 0:
                    q.append(m)

        return ordered

    def _to_step(self, agent):
        return ExecutionStep(
            agent_name=agent["agent_name"],
            intent_group=agent["intent_group"],
            capability_cluster=agent["capability_cluster"],
        )

    def _flatten(self, decision: MultiRouteDecision):
        agents = []
        for intent, caps in decision.routes.items():
            for cap, items in caps.items():
                for a in items:
                    agents.append(
                        {
                            "agent_name": a.name,
                            "intent_group": intent,
                            "capability_cluster": cap,
                            "requires": a.capabilities.requires or [],
                            "provides": a.capabilities.provides or [],
                        }
                    )
        return agents
