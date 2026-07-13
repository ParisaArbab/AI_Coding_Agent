from langgraph.graph import END, START, StateGraph
from app.agents.parser import parse_agent_output
from app.agents.prompts import SYSTEM_PROMPT, build_user_prompt
from app.models.responses import AgentResponse
from app.models.state import AgentState

class CodingAgent:
    def __init__(self, settings, llm, repository_service, github_service):
        self.settings = settings; self.llm = llm; self.repository_service = repository_service; self.github_service = github_service
        graph = StateGraph(AgentState)
        graph.add_node("collect_context", self._collect_context)
        graph.add_node("analyze", self._analyze)
        graph.add_node("finalize", self._finalize)
        graph.add_edge(START, "collect_context"); graph.add_edge("collect_context", "analyze"); graph.add_edge("analyze", "finalize"); graph.add_edge("finalize", END)
        self.graph = graph.compile()

    async def run(self, request):
        state = await self.graph.ainvoke({"request":request, "warnings":[], "files_considered":[], "issue_context":""})
        parsed = parse_agent_output(state.get("final_text", ""))
        return AgentResponse(task_type=request.task_type.value, summary=str(parsed["summary"]), analysis=str(parsed["analysis"]), proposed_changes=list(parsed["proposed_changes"]), patch=parsed["patch"], files_considered=state.get("files_considered", []), warnings=state.get("warnings", []))

    async def _collect_context(self, state):
        request = state["request"]; warnings = list(state.get("warnings", []))
        if request.repository_path:
            snap = self.repository_service.snapshot(request.repository_path, request.instruction)
            return {**state, "repository_context":snap.context, "files_considered":snap.files}
        owner, repo = request.github_owner or "", request.github_repo or ""
        tree = await self.github_service.get_repository_tree(owner, repo)
        paths = [x["path"] for x in tree if x.get("type")=="blob" and x.get("path","").endswith((".py",".js",".ts",".tsx",".go",".java",".md",".toml",".yml",".yaml"))][:25]
        blocks=[]; included=[]
        for path in paths:
            try:
                blocks.append(f"\n--- FILE: {path} ---\n{(await self.github_service.get_file(owner, repo, path))[:20000]}\n"); included.append(path)
            except Exception:
                warnings.append(f"Could not read remote file: {path}")
        issue_context=""
        if request.issue_number:
            issue=await self.github_service.get_issue(owner, repo, request.issue_number)
            issue_context=f"Title: {issue.get('title','')}\nBody: {issue.get('body','')}\nState: {issue.get('state','')}"
        return {**state, "repository_context":"REMOTE FILES:\n"+"\n".join(paths)+"\n"+"".join(blocks), "files_considered":included, "issue_context":issue_context, "warnings":warnings}

    async def _analyze(self, state):
        request=state["request"]
        prompt=build_user_prompt(request.task_type.value, request.instruction, state.get("repository_context",""), state.get("issue_context",""))
        return {**state, "analysis":await self.llm.complete(SYSTEM_PROMPT, prompt)}

    async def _finalize(self, state):
        warnings=list(state.get("warnings", [])); request=state["request"]
        if request.create_pull_request:
            if not self.settings.allow_pr_creation: warnings.append("Pull request creation was requested but ALLOW_PR_CREATION is false.")
            else: warnings.append("Review the patch and add a human approval node before enabling automatic writes.")
        return {**state, "final_text":state.get("analysis", ""), "warnings":warnings}
