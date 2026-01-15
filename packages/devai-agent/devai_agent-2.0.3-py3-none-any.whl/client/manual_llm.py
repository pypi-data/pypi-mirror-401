import json
import requests
import asyncio
from typing import Any, AsyncGenerator
from config.config import Config
from client.response import StreamEvent, StreamEventType, TextDelta, ToolCallDelta, TokenUsage, ToolCall

class ManualLLMClient:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.api_key = config.api_key
        self.base_url = config.base_url

    async def close(self):
        # Nothing to close for requests
        pass

    async def chat_completion(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> AsyncGenerator[StreamEvent, None]:
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.config.model_name,
            "messages": messages,
            "stream": True
        }
        
        if tools:
            # Wrap tools in OpenAI format: { "type": "function", "function": tool_def }
            # Check if tools are already wrapped?
            # Usually tool_schemas are just the function dict.
            # We need to check structure.
            wrapped_tools = []
            for t in tools:
                if "type" in t and "function" in t:
                     wrapped_tools.append(t)
                else:
                     wrapped_tools.append({
                         "type": "function",
                         "function": t
                     })
            data["tools"] = wrapped_tools

        def _request():
            # Use requests with stream=True
            return requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                stream=True,
                timeout=60
            )

        # Run requests.post in thread
        response = await asyncio.to_thread(_request)
        
        if response.status_code != 200:
             print(f"Error: {response.status_code} - {response.text}")
             return

        # Iterate lines
        iterator = response.iter_lines()
        
        # Tool call state tracking: index -> ToolCall
        active_tools: dict[int, ToolCall] = {}
        
        while True:
            try:
                line_bytes = await asyncio.to_thread(next, iterator)
            except StopIteration:
                break
            except Exception:
                break
                
            line = line_bytes.decode("utf-8").strip()
            if not line:
                continue
            if line == "data: [DONE]":
                break
            if line.startswith("data: "):
                json_str = line[6:]
                try:
                    chunk = json.loads(json_str)
                    if not chunk["choices"]:
                        continue
                        
                    delta = chunk["choices"][0].get("delta", {})
                    
                    # Handle Content
                    content = delta.get("content", "")
                    if content:
                        yield StreamEvent(
                            type=StreamEventType.TEXT_DELTA,
                            text_delta=TextDelta(content),
                        )
                        
                    # Handle Tool Calls
                    tool_calls = delta.get("tool_calls")
                    if tool_calls:
                        for tc in tool_calls:
                            idx = tc.get("index", 0)
                            tc_id = tc.get("id")
                            fun = tc.get("function", {})
                            name = fun.get("name")
                            args = fun.get("arguments")
                            
                            # Yield start/delta for UI
                            yield StreamEvent(
                                type=StreamEventType.TOOL_CALL_START,
                                tool_call_delta=ToolCallDelta(
                                    call_id=tc_id or "",
                                    name=name,
                                    arguments_delta=args or ""
                                ),
                            )
                            
                            # Aggregate
                            if idx not in active_tools:
                                active_tools[idx] = ToolCall(call_id=tc_id or "", name=name or "", arguments="")
                            
                            if name:
                                active_tools[idx].name = name
                            if tc_id:
                                active_tools[idx].call_id = tc_id
                            if args:
                                active_tools[idx].arguments += args

                    # Handle Usage
                    if "usage" in chunk:
                         usage_data = chunk["usage"]
                         yield StreamEvent(
                             type=StreamEventType.MESSAGE_COMPLETE,
                             usage=TokenUsage(
                                 prompt_tokens=usage_data.get("prompt_tokens", 0),
                                 completion_tokens=usage_data.get("completion_tokens", 0),
                                 total_tokens=usage_data.get("total_tokens", 0)
                             )
                         )

                except Exception as e:
                     pass

        # Emit TOOL_CALL_COMPLETE for all collected tools
        for idx, tool in active_tools.items():
            yield StreamEvent(
                type=StreamEventType.TOOL_CALL_COMPLETE,
                tool_call=tool
            )
