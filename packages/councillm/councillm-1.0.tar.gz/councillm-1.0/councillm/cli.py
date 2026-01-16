# councillm/cli.py

import asyncio
import itertools
import sys

from councillm.council import run_council
from councillm.runtime import configure_runtime, is_configured


YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

LOGO = f"""{YELLOW}
██████╗ ██████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗██╗     ██╗     ███╗   ███╗
██╔════╝██╔═══██╗██║   ██║████╗  ██║██╔════╝██║██║     ██║     ████╗ ████║
██║     ██║   ██║██║   ██║██╔██╗ ██║██║     ██║██║     ██║     ██╔████╔██║
██║     ██║   ██║██║   ██║██║╚██╗██║██║     ██║██║     ██║     ██║╚██╔╝██║
╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║╚██████╗██║███████╗███████╗██║ ╚═╝ ██║
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝╚══════╝╚══════╝╚═╝     ╚═╝
{RESET}
{CYAN}LLM Council · Ollama-powered multi-model reasoning{RESET}
"""


SPINNER = ["⊹ ࣪ ﹏𓊝﹏𓂁﹏⊹ ࣪ ˖", "𓂁﹏⊹ ࣪ ˖ ⊹ ࣪ ﹏𓊝﹏"]


async def spinner(label, stop):
    for frame in itertools.cycle(SPINNER):
        if stop.is_set():
            break
        sys.stdout.write(f"\r{CYAN}{frame}{RESET} {label}...")
        sys.stdout.flush()
        await asyncio.sleep(0.25)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()


def banner():
    print(LOGO)
    print(f"{BOLD}Type your question and press Enter.{RESET}")
    print(f"{BOLD}Type 'exit' to quit.{RESET}\n")


async def main():
    banner()

    if not is_configured():
        print("⚙️  Configure LLM Council roles\n")

        gens = input("Assign GENERATOR models (comma-separated):\n> ").strip()
        critics = input("\nAssign CRITIC models (optional):\n> ").strip()
        chairman = input("\nAssign CHAIRMAN model:\n> ").strip()

        configure_runtime(
            generators=[m.strip() for m in gens.split(",") if m.strip()],
            critics=[m.strip() for m in critics.split(",") if m.strip()],
            chairman=chairman.strip(),
        )

        print("\n✔ Council configured.\n")

    mode = input("Select mode [fast / lite / full] (default=lite): ").strip().lower()
    if mode not in {"fast", "lite", "full"}:
        mode = "lite"

    search = input("Enable web search grounding? [y/N]: ").lower() == "y"
    print(f"\nCouncil ready (mode={mode}, search={search}).\n")

    while True:
        question = input(f"{BOLD}You:{RESET} ").strip()
        if question.lower() == "exit":
            print("\nCouncil dismissed.\n")
            break

        stop = asyncio.Event()
        spin = asyncio.create_task(spinner("Council deliberating", stop))

        try:
            result = await run_council(question, mode=mode, search=search)
        except Exception as e:
            stop.set()
            await spin
            print(f"\n⚠️ Council error: {e}\n")
            continue

        stop.set()
        await spin
        print(f"{BOLD}Chairman:{RESET} {result['final']}\n")


def run():
    asyncio.run(main())














# # # # # councillm/cli.py

# # # # from councillm.runtime import set_runtime
# # # # from councillm.tui import CouncilTUI


# # # # def _ask_list(prompt: str):
# # # #     while True:
# # # #         raw = input(prompt).strip()
# # # #         models = [m.strip() for m in raw.split(",") if m.strip()]
# # # #         if models:
# # # #             return models
# # # #         print("⚠️ Enter at least one model name.")


# # # # def interactive_setup():
# # # #     print("\n" + "=" * 60)
# # # #     print("        LLM COUNCIL — INITIAL SETUP")
# # # #     print("=" * 60)

# # # #     generators = _ask_list(
# # # #         "Assign GENERATOR models (comma separated): "
# # # #     )

# # # #     critics = _ask_list(
# # # #         "Assign CRITIC models (comma separated): "
# # # #     )

# # # #     while True:
# # # #         chairman = input("Assign CHAIRMAN model: ").strip()
# # # #         if chairman:
# # # #             break
# # # #         print("⚠️ Chairman model required.")

# # # #     set_runtime(
# # # #         generators=generators,
# # # #         critics=critics,
# # # #         chairman=chairman,
# # # #     )

# # # #     print("\n✔ Configuration complete. Launching TUI...\n")


# # # # def run():
# # # #     """
# # # #     Entry point expected by `councillm` console script.
# # # #     """
# # # #     interactive_setup()
# # # #     CouncilTUI().run()

# # # # councillm/cli.py

# # # import asyncio
# # # from councillm.runtime import configure_runtime
# # # from councillm.council import run_council


# # # def banner():
# # #     print("\n" + "=" * 70)
# # #     print("        LLM COUNCIL — CLI MODE (OLLAMA)")
# # #     print("=" * 70)
# # #     print("Type your question and press Enter.")
# # #     print("Type 'exit' to quit.\n")


# # # async def main():
# # #     banner()

# # #     gens = input("Assign GENERATOR models (comma separated): ").strip()
# # #     crits = input("Assign CRITIC models (comma separated): ").strip()
# # #     chair = input("Assign CHAIRMAN model: ").strip()

# # #     configure_runtime(
# # #         generators=[m.strip() for m in gens.split(",") if m.strip()],
# # #         critics=[m.strip() for m in crits.split(",") if m.strip()],
# # #         chairman=chair.strip(),
# # #     )

# # #     print("\n✔ Council configured.\n")

# # #     while True:
# # #         q = input("You: ").strip()
# # #         if q.lower() == "exit":
# # #             break

# # #         await run_council(q)


# # # def run():
# # #     asyncio.run(main())

# # # councillm/cli.py

# # import asyncio
# # from councillm.council import run_council
# # from councillm.config import VALID_MODES


# # def ask_models(role: str) -> list[str] | str:
# #     raw = input(f"Enter {role} model(s): ").strip()
# #     return [m.strip() for m in raw.split(",")] if "," in raw else raw


# # async def main():
# #     print("\nLLM COUNCIL — OLLAMA MODE\n")

# #     generators = ask_models("GENERATOR")
# #     critics = ask_models("CRITIC")
# #     chairman = ask_models("CHAIRMAN")

# #     mode = input("Mode [fast/lite/full] (default=lite): ").strip() or "lite"
# #     if mode not in VALID_MODES:
# #         mode = "lite"

# #     search = input("Enable web search? [y/N]: ").lower() == "y"

# #     print("\nCouncil ready.\n")

# #     while True:
# #         q = input("You: ").strip()
# #         if q.lower() == "exit":
# #             break

# #         result = await run_council(
# #             q,
# #             generators=generators,
# #             critics=critics,
# #             chairman=chairman,
# #             mode=mode,
# #             search=search,
# #             verbose=True
            
# #         )
        


# #         print(f"\nChairman:\n{result['final']}\n")


# # def run():
# #     asyncio.run(main())



# import asyncio
# import itertools
# import sys
# from typing import Optional

# from councillm.council import run_council


# # ============================================================
# # ANSI COLORS (Windows safe)
# # ============================================================

# YELLOW = "\033[93m"
# CYAN = "\033[96m"
# RESET = "\033[0m"
# BOLD = "\033[1m"


# # ============================================================
# # ASCII LOGO
# # ============================================================

# LOGO = f"""{YELLOW}
# ██████╗ ██████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗██╗     ██╗     ███╗   ███╗
# ██╔════╝██╔═══██╗██║   ██║████╗  ██║██╔════╝██║██║     ██║     ████╗ ████║
# ██║     ██║   ██║██║   ██║██╔██╗ ██║██║     ██║██║     ██║     ██╔████╔██║
# ██║     ██║   ██║██║   ██║██║╚██╗██║██║     ██║██║     ██║     ██║╚██╔╝██║
# ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║╚██████╗██║███████╗███████╗██║ ╚═╝ ██║
#  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝╚══════╝╚══════╝╚═╝     ╚═╝
# {RESET}
# {CYAN}LLM Council · Ollama-powered multi-model reasoning{RESET}
# """


# # ============================================================
# # LOADING ANIMATION
# # ============================================================

# SPINNER_FRAMES = [
#     "⊹ ࣪ ﹏𓊝﹏𓂁﹏⊹ ࣪ ˖",
#     "𓂁﹏⊹ ࣪ ˖ ⊹ ࣪ ﹏𓊝﹏",
#     "﹏𓊝﹏𓂁﹏⊹ ࣪ ˖ ⊹ ࣪",
#     "⊹ ࣪ ˖ ⊹ ࣪ ﹏𓊝﹏𓂁﹏",
# ]


# async def spinner(label: str, stop: asyncio.Event):
#     for frame in itertools.cycle(SPINNER_FRAMES):
#         if stop.is_set():
#             break
#         sys.stdout.write(f"\r{CYAN}{frame}{RESET}  {label}...")
#         sys.stdout.flush()
#         await asyncio.sleep(0.25)

#     # Clear line after completion
#     sys.stdout.write("\r" + " " * 100 + "\r")
#     sys.stdout.flush()


# # ============================================================
# # BANNER
# # ============================================================

# def banner():
#     print(LOGO)
#     print(f"{BOLD}Type your question and press Enter.{RESET}")
#     print(f"{BOLD}Type 'exit' to quit.{RESET}\n")


# # ============================================================
# # MAIN CLI LOOP
# # ============================================================

# async def main():
#     banner()

#     mode = input("Select mode [fast / lite / full] (default=lite): ").strip().lower()
#     if mode not in {"fast", "lite", "full"}:
#         mode = "lite"

#     search = input("Enable web search grounding? [y/N]: ").strip().lower() == "y"

#     print(f"\nCouncil ready (mode={mode}, search={search}).\n")

#     while True:
#         question = input(f"{BOLD}You:{RESET} ").strip()

#         if question.lower() == "exit":
#             print("\nCouncil dismissed.\n")
#             break

#         stop_event = asyncio.Event()
#         spin_task = asyncio.create_task(
#             spinner("Council deliberating", stop_event)
#         )

#         try:
#             result = await run_council(
#                 question,
#                 mode=mode,
#                 search=search,
#             )
#         except Exception as e:
#             stop_event.set()
#             await spin_task
#             print(f"\n⚠️ Council error: {e}\n")
#             continue

#         stop_event.set()
#         await spin_task

#         print(f"{BOLD}Chairman:{RESET} {result['final']}\n")


# # ============================================================
# # ENTRY POINT
# # ============================================================

# def run():
#     asyncio.run(main())

