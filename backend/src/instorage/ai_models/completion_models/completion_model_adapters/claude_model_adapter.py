import base64

from anthropic import AsyncAnthropic

from instorage.ai_models.completion_models import get_response_claude
from instorage.ai_models.completion_models.completion_model import (
    CompletionModel,
    Context,
    ModelKwargs,
)
from instorage.files.file_models import File
from instorage.main.config import get_settings
from instorage.main.logging import get_logger

logger = get_logger(__name__)

MAX_TOKENS = 4096


class ClaudeModelAdapter:
    def __init__(
        self,
        model: CompletionModel,
        async_client: AsyncAnthropic = AsyncAnthropic(
            api_key=get_settings().anthropic_api_key
        ),
    ):
        self.model = model
        self.async_client = async_client

    def _get_kwargs(self, kwargs: ModelKwargs | None):
        if kwargs is None:
            return {}

        # We allow input from (0, 2), however claude only takes (0, 1)
        if kwargs.temperature is not None:
            kwargs.temperature /= 2

        return kwargs.model_dump(exclude_none=True)

    def get_token_limit_of_model(self):
        return self.model.token_limit

    def _build_image_input(self, file: File):
        image_data = base64.b64encode(file.image).decode("utf-8")

        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": file.mimetype,
                "data": image_data,
            },
        }

    def _build_content(
        self,
        input: str,
        images: list[File],
    ):
        content = [
            {
                "type": "text",
                "text": input,
            }
        ]

        for image in images:
            content.append(self._build_image_input(image))

        return content

    def create_query_from_context(self, context: Context):
        previous_messages = [
            message
            for question in context.messages
            for message in [
                {
                    "role": "user",
                    "content": self._build_content(
                        input=question.question,
                        images=question.images,
                    ),
                },
                {"role": "assistant", "content": question.answer},
            ]
        ]
        question = [
            {
                "role": "user",
                "content": self._build_content(
                    input=context.input,
                    images=context.images,
                ),
            }
        ]

        return previous_messages + question

    async def get_response(
        self,
        context: Context,
        model_kwargs: ModelKwargs | None = None,
    ):
        query = self.create_query_from_context(context=context)
        return await get_response_claude.get_response(
            client=self.async_client,
            max_tokens=MAX_TOKENS,
            model_name=self.model.name,
            prompt=context.prompt,
            messages=query,
            model_kwargs=self._get_kwargs(model_kwargs),
        )

    def get_response_streaming(
        self,
        context: Context,
        model_kwargs: ModelKwargs | None = None,
    ):
        query = self.create_query_from_context(context=context)
        return get_response_claude.get_response_streaming(
            client=self.async_client,
            max_tokens=MAX_TOKENS,
            model_name=self.model.name,
            prompt=context.prompt,
            messages=query,
            model_kwargs=self._get_kwargs(model_kwargs),
        )