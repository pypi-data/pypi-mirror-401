from jotsu.mcp.types.models import WorkflowScriptNode
from jotsu.mcp.workflow import utils
from .types import WorkflowHandlerResult


class ScriptMixin:

    # FIXME: add a time limit.
    @staticmethod
    async def handle_script(
            data: dict, *, node: WorkflowScriptNode, **_kwargs
    ):
        if node.edges:
            result = utils.script(data, expr=node.script, node=node)
            match result:
                case _ if isinstance(result, dict):
                    for edge in node.edges:
                        yield WorkflowHandlerResult(edge=edge, data=result)
                case _ if isinstance(result, list):
                    for i, edge in enumerate(node.edges):
                        if i < len(result) and result[i] is not None:
                            yield WorkflowHandlerResult(edge=edge, data=result[i])
