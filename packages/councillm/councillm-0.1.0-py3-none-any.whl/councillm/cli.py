# # # councillm/cli.py

# # from councillm.runtime import set_runtime
# # from councillm.tui import CouncilTUI


# # def _ask_list(prompt: str):
# #     while True:
# #         raw = input(prompt).strip()
# #         models = [m.strip() for m in raw.split(",") if m.strip()]
# #         if models:
# #             return models
# #         print("⚠️ Enter at least one model name.")


# # def interactive_setup():
# #     print("\n" + "=" * 60)
# #     print("        LLM COUNCIL — INITIAL SETUP")
# #     print("=" * 60)

# #     generators = _ask_list(
# #         "Assign GENERATOR models (comma separated): "
# #     )

# #     critics = _ask_list(
# #         "Assign CRITIC models (comma separated): "
# #     )

# #     while True:
# #         chairman = input("Assign CHAIRMAN model: ").strip()
# #         if chairman:
# #             break
# #         print("⚠️ Chairman model required.")

# #     set_runtime(
# #         generators=generators,
# #         critics=critics,
# #         chairman=chairman,
# #     )

# #     print("\n✔ Configuration complete. Launching TUI...\n")


# # def run():
# #     """
# #     Entry point expected by `councillm` console script.
# #     """
# #     interactive_setup()
# #     CouncilTUI().run()

# # councillm/cli.py

# import asyncio
# from councillm.runtime import configure_runtime
# from councillm.council import run_council


# def banner():
#     print("\n" + "=" * 70)
#     print("        LLM COUNCIL — CLI MODE (OLLAMA)")
#     print("=" * 70)
#     print("Type your question and press Enter.")
#     print("Type 'exit' to quit.\n")


# async def main():
#     banner()

#     gens = input("Assign GENERATOR models (comma separated): ").strip()
#     crits = input("Assign CRITIC models (comma separated): ").strip()
#     chair = input("Assign CHAIRMAN model: ").strip()

#     configure_runtime(
#         generators=[m.strip() for m in gens.split(",") if m.strip()],
#         critics=[m.strip() for m in crits.split(",") if m.strip()],
#         chairman=chair.strip(),
#     )

#     print("\n✔ Council configured.\n")

#     while True:
#         q = input("You: ").strip()
#         if q.lower() == "exit":
#             break

#         await run_council(q)


# def run():
#     asyncio.run(main())

# councillm/cli.py

import asyncio
from councillm.council import run_council
from councillm.config import VALID_MODES


def ask_models(role: str) -> list[str] | str:
    raw = input(f"Enter {role} model(s): ").strip()
    return [m.strip() for m in raw.split(",")] if "," in raw else raw


async def main():
    print("\nLLM COUNCIL — OLLAMA MODE\n")

    generators = ask_models("GENERATOR")
    critics = ask_models("CRITIC")
    chairman = ask_models("CHAIRMAN")

    mode = input("Mode [fast/lite/full] (default=lite): ").strip() or "lite"
    if mode not in VALID_MODES:
        mode = "lite"

    search = input("Enable web search? [y/N]: ").lower() == "y"

    print("\nCouncil ready.\n")

    while True:
        q = input("You: ").strip()
        if q.lower() == "exit":
            break

        result = await run_council(
            q,
            generators=generators,
            critics=critics,
            chairman=chairman,
            mode=mode,
            search=search,
            verbose=True
            
        )
        


        print(f"\nChairman:\n{result['final']}\n")


def run():
    asyncio.run(main())
