"""
LLM Service — handles all interactions with Google Gemini for chat generation.
"""
import google.generativeai as genai
from config import config


class LLMService:
    """Google Gemini LLM integration for grounded responses."""

    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=config.CHAT_MODEL,
            generation_config={
                "temperature": config.TEMPERATURE,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": config.MAX_OUTPUT_TOKENS,
            },
        )

    def build_prompt(
        self, user_message: str, document_context: str, chat_history: list[dict] = None
    ) -> str:
        """
        Build the augmented prompt with retrieved context and conversation history.

        Structure:
        1. System instructions (grounding rules)
        2. Retrieved document context
        3. Conversation history
        4. Current user question
        """
        prompt = """You are a helpful AI Support Assistant for CloudDesk platform.

## STRICT RULES (YOU MUST FOLLOW THESE):
1. You can ONLY answer questions using the provided "Product Documentation" below.
2. If the user's question is NOT covered by the documentation, you MUST respond with: "I'm sorry, I don't have information about that in our documentation. Please contact our support team for further assistance."
3. Do NOT make up, guess, or hallucinate any information.
4. Do NOT provide information from your general knowledge — ONLY use the documentation provided.
5. Be concise, friendly, and professional.
6. Use markdown formatting when it improves readability (bullet points, bold for emphasis, code blocks if needed).
7. If the user greets you (hello, hi, hey), respond warmly and ask how you can help.
8. If the user thanks you, respond politely.

## Product Documentation:
"""
        if document_context:
            prompt += document_context
        else:
            prompt += "(No relevant documentation found for this query)"

        prompt += "\n\n## Conversation History (for context):\n"

        if chat_history:
            for msg in chat_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                prompt += f"{role}: {msg['content']}\n"
        else:
            prompt += "(This is the start of the conversation)\n"

        prompt += f"""
## Current User Question:
{user_message}

## Your Response:
Remember: ONLY use the Product Documentation above. If the answer is not in the docs, say you don't have that information."""

        return prompt

    async def generate_response(
        self, user_message: str, document_context: str, chat_history: list[dict] = None
    ) -> dict:
        """
        Generate a non-streaming response.

        Returns:
            Dict with 'reply' and 'tokens_used'
        """
        try:
            prompt = self.build_prompt(user_message, document_context, chat_history)
            result = await self.model.generate_content_async(prompt)
            text = result.text
            tokens_used = getattr(result, "usage_metadata", None)
            token_count = 0
            if tokens_used:
                token_count = getattr(tokens_used, "total_token_count", 0)

            return {"reply": text, "tokens_used": token_count}
        except Exception as e:
            print(f"❌ LLM generation error: {e}")
            raise Exception("Failed to generate AI response. Please try again later.")

    async def generate_stream_response(
        self, user_message: str, document_context: str, chat_history: list[dict] = None
    ):
        """
        Generate a streaming response — yields chunks as they arrive.

        Yields:
            Dicts with type 'chunk', 'complete', or 'error'
        """
        try:
            prompt = self.build_prompt(user_message, document_context, chat_history)
            response = await self.model.generate_content_async(prompt, stream=True)

            async for chunk in response:
                text = chunk.text
                if text:
                    yield {"type": "chunk", "content": text}

            # Get final token count
            # Note: streaming doesn't always provide usage metadata
            # We estimate or get it from the aggregated response
            yield {"type": "complete", "tokens_used": 0}

        except Exception as e:
            print(f"❌ LLM streaming error: {e}")
            yield {"type": "error", "error": "Failed to generate AI response. Please try again later."}

    async def generate_title(self, user_message: str, assistant_reply: str) -> str:
        """Generate a short title for a chat session."""
        try:
            prompt = (
                "Generate a very short title (3-5 words max) for this conversation. "
                "Return ONLY the title, nothing else. No quotes, no punctuation at the end.\n\n"
                f"User: {user_message}\n"
                f"Assistant: {assistant_reply[:200]}\n\n"
                "Title:"
            )
            result = await self.model.generate_content_async(prompt)
            title = result.text.strip().strip("\"'")
            return title[:50]
        except Exception as e:
            print(f"⚠️  Title generation failed: {e}")
            return " ".join(user_message.split()[:5])


# Singleton instance
llm_service = LLMService()
