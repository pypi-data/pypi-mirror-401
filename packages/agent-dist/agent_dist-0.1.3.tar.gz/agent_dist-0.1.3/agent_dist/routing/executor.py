import asyncio
import json
import httpx
from typing import Dict, Any, List
from agent_dist.registry.client import RegistryClient
from .models import ExecutionPlan
import logging

logger = logging.getLogger("orchestrator.executor")


class Executor:
    def __init__(self, llm, registry: RegistryClient):
        self.llm = llm
        self.registry = registry

    def _normalize_agent(self, agent) -> Dict[str, Any]:
        return agent if isinstance(agent, dict) else agent.model_dump()

    async def execute(self, plan: ExecutionPlan, user_query: str, history: List[Dict] = None) -> Dict[str, Any]:
        if plan.mode == "llm_only":
            prompt = user_query
            if history:
                hist_text = json.dumps(history, indent=2)
                prompt = f"Previous conversation history:\n{hist_text}\n\nCurrent user query:\n{user_query}"
            
            result = self.llm.invoke(prompt)
            return {
                "final_answer": result.content if hasattr(result, "content") else result
            }

        context: Dict[str, Any] = {
            "ctx.user.query": user_query,
            "ctx.sys.trace": [],
        }

        if plan.mode == "chain":
            return await self._execute_chain(plan, context)

        if plan.mode == "parallel":
            return await self._execute_parallel(plan, context)


        if plan.mode == "react":
            return await self._execute_react(plan, context)

        raise ValueError(f"Unknown execution mode: {plan.mode}")

    async def _execute_react(self, plan: ExecutionPlan, context: Dict[str, Any]) -> Dict[str, Any]:
        from .prompts import ReActSystemPrompt
        
        user_query = context["ctx.user.query"]
        agents = self.registry.list_agents()
        agent_map = {a["name"]: a for a in agents}
        
        tools_desc = []
        for a in agents:
            caps = a.get("capabilities", {})
            requires = caps.get("requires", [])
            # Heuristic: args match the last part of the dot-notation in requires
            args = [r.split(".")[-1] for r in requires]
            desc = f"- {a['name']}({', '.join(args)}): {a['description']}"
            tools_desc.append(desc)
        
        tools_desc = "\n".join(tools_desc)
        history = ""
        
        max_steps = 10
        for i in range(max_steps):
            prompt = ReActSystemPrompt.format(
                goal=user_query,
                tools=tools_desc,
                history=history
            )
            
            result = self.llm.invoke(prompt)
            content = result.content if hasattr(result, "content") else str(result)
            
            logger.info(f"Step {i+1} Thought: {content[:100]}...")
            
            # Simple parsing of multiple lines
            lines = content.strip().split("\n")
            action_line = next((l for l in lines if l.startswith("Action:")), None)
            final_line = next((l for l in lines if l.startswith("Final Answer:")), None)
            
            history += f"\nStep {i+1}:\n{content}\n"
            
            if final_line:
                answer = final_line.replace("Final Answer:", "").strip()
                logger.info(f"ReAct Final Answer: {answer}")
                return {
                    "final_answer": answer,
                    "trace": context.get("ctx.sys.trace", [])
                }
            
            if action_line:
                # Parse "Action: ToolName(json)"
                # Regex or string splitting. Let's do robust string splitting
                try:
                    part = action_line.replace("Action:", "").strip()
                    logger.info(f"ReAct Action: {part}")
                    agent_name = part.split("(")[0].strip()
                    args_str = part[len(agent_name):].strip().strip("()")
                    
                    if not args_str:
                        payload = {}
                    else:
                        payload = json.loads(args_str)
                        
                    if agent_name not in agent_map:
                        obs = f"Observation: Error: Agent '{agent_name}' not found."
                        logger.warning(f"ReAct Agent Not Found: {agent_name}")
                    else:
                        agent = agent_map[agent_name]
                        async with httpx.AsyncClient(timeout=30.0) as client:
                            logger.info(f"Calling Agent: {agent['url']}")
                            resp = await client.post(agent["url"], json=payload)
                            if resp.status_code >= 400:
                                obs = f"Observation: Error {resp.status_code}: {resp.text}"
                                logger.error(f"Agent Error: {resp.status_code}")
                            else:
                                obs = f"Observation: {json.dumps(resp.json())}"
                                logger.info(f"Agent Response: {obs[:100]}...")
                                
                                # RECORD TRACE
                                context["ctx.sys.trace"].append({
                                    "agent": agent_name, 
                                    "input": payload,
                                    "output": resp.json(),
                                    "step": i+1
                                })
                                
                    history += f"\n{obs}\n"
                    
                except Exception as e:
                    history += f"\nObservation: Error parsing/executing action: {str(e)}\n"
                    logger.error(f"ReAct Action Error: {e}")
            else:
                 history += "\nObservation: No action found. Waiting for next thought.\n"
                 logger.info("No action found in step.")

        return {
            "final_answer": "Goal not reached max steps.",
            "trace": context.get("ctx.sys.trace", [])
        }

    async def _execute_chain(self, plan: ExecutionPlan, context: Dict[str, Any]) -> Dict[str, Any]:
        if not plan.steps:
            raise RuntimeError("Execution plan has no steps")

        for step in plan.steps:
            agent = self._normalize_agent(self.registry.get_agent(step.agent_name))
            caps = agent["capabilities"]
            requires = set(caps.get("requires", []))
            provides = set(caps.get("provides", []))

            missing = requires - context.keys()
            if missing:
                raise RuntimeError(
                    f"Agent '{agent['name']}' missing required context: {missing}"
                )

            output = await self._invoke_agent(agent, context)

            for key in provides:
                if key not in output:
                    raise RuntimeError(
                        f"Agent '{agent['name']}' failed to provide '{key}'"
                    )
                context[key] = output[key]

            context["ctx.sys.trace"].append(
                {"agent": agent["name"], "provides": sorted(provides)}
            )

        if "ctx.final.answer" not in context:
            logger.warning("Chain completed without ctx.final.answer. Returning context.")
            # Fallback: return what we have so far instead of crashing
            return {
                "final_answer": "Process completed (implicit).",
                "details": {k: v for k, v in context.items() if k != "ctx.sys.trace"},
                "trace": context.get("ctx.sys.trace", [])
            }

        return {
            "final_answer": context["ctx.final.answer"],
            "trace": context.get("ctx.sys.trace", [])
        }

    async def _execute_parallel(self, plan: ExecutionPlan, context: Dict[str, Any]) -> Dict[str, Any]:
        async def run(step):
            agent = self._normalize_agent(self.registry.get_agent(step.agent_name))
            caps = agent["capabilities"]
            requires = set(caps.get("requires", []))
            provides = set(caps.get("provides", []))

            missing = requires - context.keys()
            if missing:
                raise RuntimeError(
                    f"Agent '{agent['name']}' missing required context: {missing}"
                )

            output = await self._invoke_agent(agent, context)
            return agent["name"], output, provides

        results = await asyncio.gather(*[run(step) for step in plan.steps])

        for agent_name, output, provides in results:
            for k, v in output.items():
                if k in context:
                    raise RuntimeError(
                        f"Parallel context collision on key '{k}'"
                    )
                context[k] = v

            context["ctx.sys.trace"].append(
                {"agent": agent_name, "provides": sorted(provides)}
            )

        if "ctx.final.answer" in context:
            return {"final_answer": context["ctx.final.answer"]}

        from .prompts import MergeParallelOutputsPrompt

        prompt = MergeParallelOutputsPrompt.format(
            user_query=context["ctx.user.query"],
            agent_outputs=json.dumps(context, indent=2),
        )

        result = self.llm.invoke(prompt)
        return {
            "final_answer": result.content if hasattr(result, "content") else result
        }

    async def _invoke_agent(
        self,
        agent: Dict[str, Any],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:

        caps = agent["capabilities"]
        requires = caps.get("requires", [])

        payload = {}
        for r in requires:
            param = r.split(".")[-1]
            payload[param] = context[r]

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(agent["url"], json=payload)
                resp.raise_for_status()
                output = resp.json()
                
            if not isinstance(output, dict):
                raise RuntimeError(f"Agent '{agent['name']}' did not return a JSON object")
                
            return output
            
        except httpx.HTTPError as e:
            logger.error(f"Agent '{agent['name']}' failed: {e}")
            # Depending on policy, we might want to return an error context or re-raise
            # For now, Re-raise to trigger the global handler
            raise RuntimeError(f"Agent '{agent['name']}' unavailable: {str(e)}") from e
        except Exception as e:
             raise RuntimeError(f"Agent '{agent['name']}' unexpected error: {str(e)}") from e