import hashlib
from typing import Dict, List
from agent_dist.registry.client import RegistryClient
from .models import MultiRouteDecision


class HierarchicalRouter:
    def __init__(self, llm, registry: RegistryClient):
        self.llm = llm
        self.registry = registry
        self._cache: Dict[str, MultiRouteDecision] = {}

    def route(self, query: str, history: List[Dict] = None) -> MultiRouteDecision:
        agents = self.registry.list_agents()
        cache_key = self._hash(query, agents) # Note: history not in cache key yet for simplicity


        if cache_key in self._cache:
            return self._cache[cache_key]

        if not self._should_use_agents(query):
            decision = MultiRouteDecision(mode="llm_only")
            self._cache[cache_key] = decision
            return decision

        routes = self._llm_select_agents(query, agents, history)

        if not routes:
            pass

        # Heuristic for ReAct: checks for loop or conditional keywords
        is_complex = any(k in query.lower() for k in ["if ", "until", "while", "loop"])
        
        if is_complex and routes:
             # Even if routes found, complex logic needs ReAct
             decision = MultiRouteDecision(mode="react")
             self._cache[cache_key] = decision
             return decision

        if not routes:
             # If "should_use_agents" was true but no routes found -> ReAct can try to figure it out
             decision = MultiRouteDecision(mode="react")
             self._cache[cache_key] = decision
             return decision

        decision = MultiRouteDecision(mode="agents", routes=routes)
        self._cache[cache_key] = decision
        return decision

    def _hash(self, query: str, agents: List[dict]) -> str:
        names = sorted(a["name"] for a in agents)
        raw = query + "|" + "|".join(names)
        return hashlib.sha256(raw.encode()).hexdigest()

    def _should_use_agents(self, query: str) -> bool:
        from .prompts import ShouldUseAgentsPrompt
        
        prompt = ShouldUseAgentsPrompt.format(query=query)
        out = self.llm.invoke(prompt)
        resp = out.content if hasattr(out, "content") else out
        return resp.strip().lower() == "true"

    def _llm_select_agents(
        self,
        query: str,
        agents: List[dict],
        history: List[Dict] = None,
    ) -> Dict[str, Dict[str, List[dict]]]:

        import json
        from .prompts import SelectAgentsPrompt

        prompt = SelectAgentsPrompt.format(
            query=query,
            agents=json.dumps(agents, indent=2),
            history=json.dumps(history or [], indent=2),
        )

        out = self.llm.invoke(prompt)
        raw = out.content if hasattr(out, "content") else out

        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        raw = raw.strip()
        
        # Heuristic: find first { and last }
        s = raw.find("{")
        e = raw.rfind("}")
        if s != -1 and e != -1:
            raw = raw[s : e + 1]

        try:
            parsed = json.loads(raw)
        except Exception:
            # Fallback: empty selection if parsing fails
            return {}

        routes: Dict[str, Dict[str, List[dict]]] = {}

        # Re-map parsed names back to full agent dicts
        agent_map = {a["name"]: a for a in agents}

        for intent, caps in parsed.items():
            for cap, names in caps.items():
                for name in names:
                    if name in agent_map:
                        routes.setdefault(intent, {}).setdefault(cap, []).append(
                            agent_map[name]
                        )
                    else:
                        print(f"Warning: LLM selected unknown agent '{name}'")

        return routes
