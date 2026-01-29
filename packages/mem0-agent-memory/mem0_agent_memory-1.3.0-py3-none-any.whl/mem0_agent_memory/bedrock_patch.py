"""
Monkey patch for mem0's AWS Bedrock LLM to fix compatibility issues.

Fixes:
1. Claude Haiku 4.5: Doesn't allow both temperature and top_p together
2. Amazon Nova: Requires message content in list format [{"text": "..."}] not plain strings
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def patched_format_messages_amazon(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Format messages for Amazon models using Converse API format.
    Amazon Nova requires content as list of content blocks, not plain strings.
    """
    formatted_messages = []
    for message in messages:
        role = message["role"]
        content = message["content"]
        
        # Amazon Converse API requires content as list of content blocks
        if role == "system":
            # System messages go in a separate parameter, not in messages array
            continue
        elif role == "user":
            formatted_messages.append({
                "role": "user",
                "content": [{"text": content}]  # List format required
            })
        elif role == "assistant":
            formatted_messages.append({
                "role": "assistant", 
                "content": [{"text": content}]  # List format required
            })
    
    return formatted_messages


def patched_generate_with_tools(self, messages: List[Dict[str, str]], tools: List[Dict], stream: bool = False) -> Dict[str, Any]:
    """Patched version that handles Claude 4.5 parameter restrictions."""
    # Format messages for tool-enabled models
    system_message = None
    if self.provider == "anthropic":
        formatted_messages, system_message = self._format_messages_anthropic(messages)
    elif self.provider == "amazon":
        formatted_messages = patched_format_messages_amazon(self, messages)
        # Extract system message if present
        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content")
                break
    else:
        formatted_messages = [{"role": "user", "content": [{"text": messages[-1]["content"]}]}]

    # Prepare tool configuration in Converse API format
    tool_config = None
    if tools:
        converse_tools = self._convert_tools_to_converse_format(tools)
        if converse_tools:
            tool_config = {"tools": converse_tools}

    # Prepare inference config - handle Claude 4.5 restrictions
    inference_config = {
        "maxTokens": self.model_config.get("max_tokens", 2000),
    }
    
    # Claude 4.5 models don't allow both temperature and top_p
    if "claude-4" in self.config.model.lower() or "haiku-4" in self.config.model.lower() or "sonnet-4" in self.config.model.lower() or "opus-4" in self.config.model.lower():
        # Only use temperature for Claude 4.x models
        inference_config["temperature"] = self.model_config.get("temperature", 0.1)
    else:
        # Use both for older models
        inference_config["temperature"] = self.model_config.get("temperature", 0.1)
        inference_config["topP"] = self.model_config.get("top_p", 0.9)

    # Prepare converse parameters
    converse_params = {
        "modelId": self.config.model,
        "messages": formatted_messages,
        "inferenceConfig": inference_config
    }

    # Add system message if present (for Anthropic)
    if system_message:
        converse_params["system"] = [{"text": system_message}]

    # Add tool config if present
    if tool_config:
        converse_params["toolConfig"] = tool_config

    # Make API call
    response = self.client.converse(**converse_params)

    return self._parse_response(response, tools)


def patched_generate_standard(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
    """Patched version that handles Claude 4.5 parameter restrictions."""
    # For Anthropic models, always use Converse API
    if self.provider == "anthropic":
        formatted_messages, system_message = self._format_messages_anthropic(messages)

        # Prepare inference config - handle Claude 4.5 restrictions
        inference_config = {
            "maxTokens": self.model_config.get("max_tokens", 2000),
        }
        
        # Claude 4.5 models don't allow both temperature and top_p
        if "claude-4" in self.config.model.lower() or "haiku-4" in self.config.model.lower() or "sonnet-4" in self.config.model.lower() or "opus-4" in self.config.model.lower():
            # Only use temperature for Claude 4.x models
            inference_config["temperature"] = self.model_config.get("temperature", 0.1)
        else:
            # Use both for older models
            inference_config["temperature"] = self.model_config.get("temperature", 0.1)
            inference_config["topP"] = self.model_config.get("top_p", 0.9)

        # Prepare converse parameters
        converse_params = {
            "modelId": self.config.model,
            "messages": formatted_messages,
            "inferenceConfig": inference_config
        }

        # Add system message if present
        if system_message:
            converse_params["system"] = [{"text": system_message}]

        # Use converse API for Anthropic models
        response = self.client.converse(**converse_params)

        # Parse Converse API response
        if hasattr(response, 'output') and hasattr(response.output, 'message'):
            return response.output.message.content[0].text
        elif 'output' in response and 'message' in response['output']:
            return response['output']['message']['content'][0]['text']
        else:
            return str(response)

    elif self.provider == "amazon" and "nova" in self.config.model.lower():
        # Nova models use converse API even without tools
        formatted_messages = patched_format_messages_amazon(self, messages)
        
        # Extract system message if present
        system_message = None
        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content")
                break
        
        # Prepare inference config
        inference_config = {
            "maxTokens": self.model_config.get("max_tokens", 5000),
            "temperature": self.model_config.get("temperature", 0.1),
            "topP": self.model_config.get("top_p", 0.9),
        }
        
        # Prepare converse parameters
        converse_params = {
            "modelId": self.config.model,
            "messages": formatted_messages,
            "inferenceConfig": inference_config
        }
        
        # Add system message if present
        if system_message:
            converse_params["system"] = [{"text": system_message}]
        
        # Use converse API for Nova models
        response = self.client.converse(**converse_params)
        
        # Parse Converse API response for Nova
        if hasattr(response, 'output') and hasattr(response.output, 'message'):
            return response.output.message.content[0].text
        elif 'output' in response and 'message' in response['output']:
            return response['output']['message']['content'][0]['text']
        else:
            return str(response)
    else:
        # For other providers and legacy Amazon models (like Titan)
        if self.provider == "amazon":
            # Legacy Amazon models need string formatting, not array formatting
            prompt = self._format_messages_generic(messages)
        else:
            prompt = self._format_messages(messages)
        input_body = self._prepare_input(prompt)

        # Convert to JSON
        import json
        body = json.dumps(input_body)

        # Make API call
        response = self.client.invoke_model(
            body=body,
            modelId=self.config.model,
            accept="application/json",
            contentType="application/json",
        )

        return self._parse_response(response)


def apply_bedrock_patch():
    """Apply the monkey patch to mem0's AWSBedrockLLM class."""
    try:
        from mem0.llms.aws_bedrock import AWSBedrockLLM
        
        # Replace the methods
        AWSBedrockLLM._format_messages_amazon = patched_format_messages_amazon
        AWSBedrockLLM._generate_with_tools = patched_generate_with_tools
        AWSBedrockLLM._generate_standard = patched_generate_standard
        
        logger.info("Applied Bedrock patch for Claude 4.5 and Amazon Nova compatibility")
        return True
    except Exception as e:
        logger.warning(f"Failed to apply Bedrock patch: {e}")
        return False
