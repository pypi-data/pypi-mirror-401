# councillm/ollama_clnt.py

from ollama import AsyncClient

_client = AsyncClient()


async def query_model(model: str, prompt: str) -> str:
    response = await _client.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


async def query_models_parallel(models: list[str], prompt: str) -> dict[str, str]:
    import asyncio

    async def _run(m):
        try:
            return m, await query_model(m, prompt)
        except Exception as e:
            return m, f"ERROR: {e}"

    results = await asyncio.gather(*[_run(m) for m in models])
    return dict(results)




# # # # from ollama import AsyncClient
# # # # import asyncio

# # # # client = AsyncClient()

# # # # async def query_model(model: str, prompt: str):
# # # #     try:
# # # #         response = await client.chat(
# # # #             model=model,
# # # #             messages=[{"role": "user", "content": prompt}],
# # # #         )
# # # #         return response.message.content
# # # #     except Exception as e:
# # # #         print(f"[Ollama Error] {model}: {e}")
# # # #         return None


# # # # async def query_models_parallel(models: list[str], prompt: str):
# # # #     tasks = [query_model(model, prompt) for model in models]
# # # #     results = await asyncio.gather(*tasks)
# # # #     return dict(zip(models, results))

# # # from typing import List, Dict
# # # from ollama import AsyncClient
# # # import asyncio


# # # _client = AsyncClient()


# # # # ---------------------------------------
# # # # SINGLE MODEL QUERY
# # # # ---------------------------------------

# # # async def query_model(model: str, prompt: str) -> str:
# # #     """
# # #     Query a single Ollama model with a user prompt.
# # #     Returns plain text output.
# # #     """
# # #     response = await _client.chat(
# # #         model=model,
# # #         messages=[
# # #             {"role": "user", "content": prompt}
# # #         ]
# # #     )

# # #     return response["message"]["content"]


# # # # ---------------------------------------
# # # # PARALLEL MODEL QUERY
# # # # ---------------------------------------

# # # async def query_models_parallel(
# # #     models: List[str],
# # #     prompt: str,
# # # ) -> Dict[str, str]:
# # #     """
# # #     Query multiple Ollama models in parallel.
# # #     Returns {model_name: response_text}
# # #     """

# # #     async def _call(model: str):
# # #         try:
# # #             text = await query_model(model, prompt)
# # #             return model, text
# # #         except Exception as e:
# # #             return model, f"[ERROR] {e}"

# # #     tasks = [_call(m) for m in models]
# # #     results = await asyncio.gather(*tasks)

# # #     return {model: text for model, text in results}

# # # councillm/ollama_clnt.py

# # from ollama import AsyncClient

# # _client = AsyncClient()


# # async def query_model(model: str, prompt: str) -> str:
# #     response = await _client.chat(
# #         model=model,
# #         messages=[{"role": "user", "content": prompt}],
# #     )
# #     return response["message"]["content"]


# # async def query_models_parallel(models: list[str], prompt: str) -> dict:
# #     import asyncio

# #     async def _run(m):
# #         try:
# #             return m, await query_model(m, prompt)
# #         except Exception as e:
# #             return m, f"ERROR: {e}"

# #     results = await asyncio.gather(*[_run(m) for m in models])
# #     return dict(results)


# # councillm/ollama_client.py

# # councillm/ollama_clnt.py

# from ollama import AsyncClient

# _client = AsyncClient()


# async def query_model(model: str, prompt: str) -> str:
#     response = await _client.chat(
#         model=model,
#         messages=[{"role": "user", "content": prompt}],
#     )
#     return response["message"]["content"]


# async def query_models_parallel(models: list[str], prompt: str) -> dict:
#     import asyncio

#     async def _run(m):
#         try:
#             return m, await query_model(m, prompt)
#         except Exception as e:
#             return m, f"ERROR: {e}"

#     results = await asyncio.gather(*[_run(m) for m in models])
#     return dict(results)
