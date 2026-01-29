from pydantic import ConfigDict, BaseModel, Field
from enum import Enum
from typing import Dict, List, Literal, Optional, Any, Union
from humps import camelize


def to_camel(string):
    return camelize(string)


class GPTRouterMetadata(BaseModel):
    tag: Optional[str] = None
    history_id: Optional[str] = None
    created_by_user_id: Optional[str] = None
    appId: Optional[str] = None


class ThinkingType(str, Enum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class SearchContextSize(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ExtendedThinking(BaseModel):
    type: ThinkingType
    budget_tokens: Optional[int] = 1024


class UserLocationApproximate(BaseModel):
    city: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    timezone: Optional[str] = None


class UserLocation(BaseModel):
    type: Optional[str] = None
    approximate: Optional[UserLocationApproximate] = None


class WebSearchOptions(BaseModel):
    search_context_size: Optional[SearchContextSize] = None
    user_location: Optional[Union[dict, UserLocation]] = None


class GenerationParams(BaseModel):
    messages: Optional[List[Any]] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    user: Optional[str] = None
    prompt: Optional[str] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    functions: Optional[List[Any]] = None
    function_call: Optional[dict] = None
    tools: Optional[List[Any]] = None
    tool_choice: Optional[Union[str, dict]] = None
    response_format: Optional[Dict[str, Any]] = None
    parallel_tool_calls: Optional[bool] = None
    tag: Optional[str] = None
    user_id: Optional[str] = None
    history_id: Optional[str] = None
    appId: Optional[str] = None
    metadata: Optional[dict] = None
    raw_event: Optional[bool] = None
    thinking: Optional[ExtendedThinking] = None
    colasce_into_thinking_tag: Optional[bool] = None
    use_response_api: Optional[bool] = None
    web_search_options: Optional[WebSearchOptions] = None
    reasoning_effort: Optional[Literal["minimal", "low", "medium", "high"]] = None


class ModelGenerationRequest(BaseModel):
    model_name: str
    provider_name: str
    order: int = Field(int)
    prompt_params: Optional[GenerationParams] = Field(default={})
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, protected_namespaces=())


class Usage(BaseModel):
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class Choice(BaseModel):
    index: int
    text: str
    finish_reason: str
    role: Optional[str] = None
    function_call: Optional[Any] = None
    citations: Optional[List[dict | Any]] = None


class GenerationResponse(BaseModel):
    id: str
    choices: List[Choice]
    model: str
    provider_id: Optional[str] = Field(None, alias="providerId")
    model_id: Optional[str] = Field(None, alias="modelId")
    meta: Optional[Usage] = None
    citations: Optional[List[str]] = None
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True, protected_namespaces=())


class ChunkedGenerationResponse(BaseModel):
    event: str
    data: dict
    provider: Optional[str] = None


class ImageGenerationRequest(BaseModel):
    model_name: str = Field(alias="model")
    provider_name: str = Field(alias="imageVendor")
    prompt: str
    num_images: int = Field(alias="numImages", default=1)
    width: Optional[int] = Field(None, alias="width")
    height: Optional[int] = Field(None, alias="height")
    num_inference_steps: Optional[int] = Field(None, alias="numInferenceSteps")
    app_id: Optional[str] = Field(None, alias="appId")
    user_id: Optional[str] = Field(None, alias="createdByUserId")
    history_id: Optional[str] = Field(None, alias="historyId")
    feature: Optional[str] = Field(None, alias="feature")
    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    @property
    def size(self) -> Optional[str]:
        return f"{self.width}x{self.height}" if self.width and self.height else None

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        base_dict = super().model_dump(*args, **kwargs)
        if self.size is not None:
            base_dict["size"] = self.size
        return base_dict


class ImageGenerationResponse(BaseModel):
    url: str = None
    base64: str = None
    finish_reason: Optional[str] = Field(default="SUCCESS", alias="finishReason")


class ImageEditRequest(BaseModel):
    model_name: str = Field(alias="model", default="gpt-image-1")
    image: Union[str, List[str]] = Field(...)
    prompt: str = Field(...)
    mask: Optional[str] = Field(default=None)
    num_images: Optional[int] = Field(alias="n", default=1)
    quality: Optional[str] = Field(default="high")
    response_format: Optional[str] = Field(alias="responseFormat", default=None)
    size: Optional[str] = Field(default="1024x1024")
    user: Optional[str] = Field(default=None)
    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        base_dict = super().model_dump(*args, **kwargs)
        return base_dict


class ModelRouterGenerationRequest(BaseModel):
    model_name: str
    model_provider: str
    prompt_params: GenerationParams = Field(alias="promptParams")
    should_validate_token_count: Optional[bool] = Field(
        default=False, alias="shouldValidateTokenCount"
    )
    model_config = ConfigDict(populate_by_name=True, protected_namespaces=())

    def model_dump(self, *args, **kwargs):
        # Generate the standard dict first.
        kwargs.setdefault('exclude_none', True)
        kwargs.setdefault('by_alias', True)
        result = super().model_dump(*args, **kwargs)

        result["providerName"] = self.model_provider
        result["modelName"] = self.model_name

        return result


class ModelRouterEmbeddingsGenerationParams(BaseModel):
    input: List[str]


class ModelRouterEmbeddingsGenerationRequest(ModelRouterGenerationRequest):
    prompt_params: ModelRouterEmbeddingsGenerationParams = Field(alias="promptParams")


class ModelRouterGenerationResponse(BaseModel):
    id: str
    choices: List[Choice]
    model: str
    provider_id: Optional[str] = Field(None, alias="providerId")
    model_id: Optional[str] = Field(None, alias="modelId")
    meta: Optional[Usage] = None
    model_config = ConfigDict(protected_namespaces=())


class EmbeddingsChoice(BaseModel):
    embedding: List[float]


class ModelRouterEmbeddingsGenerationResponse(BaseModel):
    choices: List[EmbeddingsChoice]
