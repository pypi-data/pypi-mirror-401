ShouldUseAgentsPrompt = """
Task:
Decide whether this query requires calling external agents.

Return ONLY one word:
true or false

Rules:
- Return true if the query involves booking, scheduling, confirming, availability, financial checks, insurance operations, or any domain-specific action.
- Return false ONLY for purely informational questions or greetings.

Query:
{query}
"""

SelectAgentsPrompt = """
You are a routing engine.

Your job is to select the MINIMAL set of agents required to complete the user request.
Only select agents that are explicitly needed.

Rules:
- If the request involves booking/scheduling/checking, select relevant agents.
- Do NOT answer the question yourself.
- Return EMPTY JSON {{}} if no agents are needed (informational query).
- Return ONLY valid JSON.
- Do NOT include markdown formatting (like ```json ... ```) if possible, but I will parse it if you do.

JSON schema:
{{
  "<intent_group>": {{
    "<capability_cluster>": ["<agent_name>"]
  }}
}}

User request:
{query}

Previous Conversation:
{history}

Available agents:
{agents}

Output JSON:
"""

PlanExecutionPrompt = """
You are an execution planner.

User query:
{query}

Candidate agents:
{agents}

Your task:
- Decide HOW to execute the selected agents

Choose:
- mode: parallel or chain
- steps: which agents to run
- order ONLY if mode is chain

Guidelines:
- Use parallel when agents are independent
- Use chain ONLY when one agent’s output is required by another
- Do NOT invent agents
- Prefer using all provided agents unless dependency forces exclusion

Return ONLY valid JSON in this format:
{
  "mode": "parallel | chain",
  "steps": [
    {
      "agent_name": "...",
      "intent_group": "...",
      "capability_cluster": "..."
    }
  ]
}
"""

SchemaSystemPrompt = """
You are an AI agent.

ROLE:
{agent_role}
"""

SchemaHumanPromptIsFinal = """
User query:
{user_query}

Current context:
{context}

Update the context by adding new information you are responsible for.
Return ONLY valid JSON representing context updates.
"""

SchemaHumanPrompt = """
User query:
{user_query}

Current context:
{context}

Your response MUST match the input schema expected by the next agent:
{next_agent_name}
"""

MergeParallelOutputsPrompt = """
You are synthesizing results from multiple agents to answer a user request.

User query:
{user_query}

Context (Agent Outputs):
{agent_outputs}

Task:
- Use the provided Context to answer the User query.
- Do NOT ask for information that is already present in the Context.
- Combine the outputs into a single, natural response.

Return ONLY the final answer text.
"""


ReActSystemPrompt = """
You are a Reasoning Agent (ReAct).

Goal: {goal}

Tools Available:
{tools}

Instructions:
1. "Thought": Analyze the current situation and previous history. Decide what to do next.
2. "Action": Call a tool if needed.
   Format: Action: ToolName(input_json)
   Example: Action: Search({{"query": "hospital hours"}})
3. "Observation": (Wait for the system to provide the result of the action).
4. "Final Answer": If you have enough information to solve context, stop.
   Format: Final Answer: <your response>

Constraints:
- Only use the tools provided.
- If you have the answer, output "Final Answer: ...".
- Loops are allowed if you need more info.

History:
{history}

Begin!
"""
