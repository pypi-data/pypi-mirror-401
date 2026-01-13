from typing import Any, Dict, List
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, List
from langchain_core.embeddings import Embeddings
from langchain_community.llms import VLLM
# Example of initializing the VLLM model and getting the client to pass VLLMEmbeddings
# params= {
#         "trust_remote_code": True,
#         "max_new_tokens": 8192,
#         "top_k": 1,
#         "top_p": 0.95,
#         "temperature": 0,
#         "tensor_parallel_size": 1,
#         "vllm_kwargs": {
#           "gpu_memory_utilization": 0.8,
#           "task": "embed"
#         }
# }

# llm = VLLM(model = "meta-llama/Meta-Llama-3-8B-Instruct", **params)
# client = llm.client
# embeddings = VLLMEmbeddings(client=client)

