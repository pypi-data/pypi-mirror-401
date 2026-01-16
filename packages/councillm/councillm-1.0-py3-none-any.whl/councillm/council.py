# councillm/council.py

from councillm.runtime import get_runtime
from councillm.ollama_clnt import query_model, query_models_parallel
from councillm.search_tool import web_search


async def run_council(
    question: str,
    *,
    mode: str = "lite",
    search: bool = False,
):
    runtime = get_runtime()

    generators = runtime["generators"]
    critics = runtime["critics"]
    chairman = runtime["chairman"]

    evidence = ""
    if search:
        evidence = web_search(question)

    # ---------------- FAST ----------------
    if mode == "fast":
        prompt = f"""
Question:
{question}

Evidence:
{evidence}

Answer accurately and concisely.
"""
        final = await query_model(chairman, prompt)
        return {"final": final}

    # ---------------- LITE ----------------
    if mode == "lite":
        draft = await query_model(generators[0], question)

        synth_prompt = f"""
Draft:
{draft}

Evidence:
{evidence}

Improve correctness and completeness.
"""
        final = await query_model(chairman, synth_prompt)
        return {"draft": draft, "final": final}

    # ---------------- FULL ----------------
    stage1 = await query_models_parallel(generators, question)

    critique_prompt = f"""
Question:
{question}

Evidence:
{evidence}

Drafts:
{stage1}

Critique and rank the drafts.
"""
    stage2 = {}
    if critics:
        stage2 = await query_models_parallel(critics, critique_prompt)

    synth_prompt = f"""
Question:
{question}

Evidence:
{evidence}

Drafts:
{stage1}

Critiques:
{stage2}

Produce a single verified final answer.
"""
    final = await query_model(chairman, synth_prompt)

    return {
        "stage1": stage1,
        "stage2": stage2,
        "final": final,
    }




# # # # # # # # # from .ollama_clnt import query_model, query_models_parallel
# # # # # # # # # from .config import COUNCIL_MODES
# # # # # # # # # from .search_tool import web_search


# # # # # # # # # async def run_council(question: str, mode: str = "fast", search: bool = False):
# # # # # # # # #     """
# # # # # # # # #     Run the LLM Council in fast / lite / full mode with optional web grounding.
# # # # # # # # #     """

# # # # # # # # #     cfg = COUNCIL_MODES.get(mode)
# # # # # # # # #     if not cfg:
# # # # # # # # #         raise ValueError(f"Invalid mode '{mode}'. Choose from {list(COUNCIL_MODES)}")

# # # # # # # # #     evidence = ""
# # # # # # # # #     if search:
# # # # # # # # #         evidence = web_search(question)

# # # # # # # # #     # ---------------- FAST MODE ----------------
# # # # # # # # #     if mode == "fast":
# # # # # # # # #         prompt = f"""
# # # # # # # # # Question:
# # # # # # # # # {question}

# # # # # # # # # External Evidence:
# # # # # # # # # {evidence}

# # # # # # # # # Answer clearly and concisely. Use evidence when helpful.
# # # # # # # # # """
# # # # # # # # #         final = await query_model(cfg["chairman"], prompt)
# # # # # # # # #         return {"final": final}

# # # # # # # # #     # ---------------- LITE MODE ----------------
# # # # # # # # #     if mode == "lite":
# # # # # # # # #         gen_model = cfg["generators"][0]

# # # # # # # # #         draft = await query_model(gen_model, question)

# # # # # # # # #         synthesis_prompt = f"""
# # # # # # # # # Draft Answer:
# # # # # # # # # {draft}

# # # # # # # # # External Evidence:
# # # # # # # # # {evidence}

# # # # # # # # # Improve the draft. Correct errors and add missing facts.
# # # # # # # # # """
# # # # # # # # #         final = await query_model(cfg["chairman"], synthesis_prompt)

# # # # # # # # #         return {"draft": draft, "final": final}

# # # # # # # # #     # ---------------- FULL MODE ----------------
# # # # # # # # #     # Stage 1 — parallel generation
# # # # # # # # #     stage1 = await query_models_parallel(cfg["generators"], question)

# # # # # # # # #     # Stage 2 — peer ranking
# # # # # # # # #     ranking_prompt = f"""
# # # # # # # # # Question:
# # # # # # # # # {question}

# # # # # # # # # External Evidence:
# # # # # # # # # {evidence}

# # # # # # # # # Here are model answers:
# # # # # # # # # {stage1}

# # # # # # # # # Rank the answers from best to worst and justify briefly.
# # # # # # # # # """
# # # # # # # # #     stage2 = await query_models_parallel(cfg["critics"], ranking_prompt)

# # # # # # # # #     # Stage 3 — chairman synthesis
# # # # # # # # #     synthesis_prompt = f"""
# # # # # # # # # Question:
# # # # # # # # # {question}

# # # # # # # # # External Evidence:
# # # # # # # # # {evidence}

# # # # # # # # # Model Drafts:
# # # # # # # # # {stage1}

# # # # # # # # # Peer Reviews:
# # # # # # # # # {stage2}

# # # # # # # # # Synthesize the best final answer grounded in evidence.
# # # # # # # # # """
# # # # # # # # #     final = await query_model(cfg["chairman"], synthesis_prompt)

# # # # # # # # #     return {
# # # # # # # # #         "stage1": stage1,
# # # # # # # # #         "stage2": stage2,
# # # # # # # # #         "final": final,
# # # # # # # # #     }

# # # # # # # # from typing import Dict, List
# # # # # # # # from .ollama_clnt import query_model, query_models_parallel
# # # # # # # # from .config import COUNCIL_MODES
# # # # # # # # from .search_tool import web_search
# # # # # # # # from .fact_guard import validate_evidence


# # # # # # # # # ==========================================================
# # # # # # # # # CORE COUNCIL RUNNER
# # # # # # # # # ==========================================================
# # # # # # # # async def run_council(question: str, mode: str = "fast", search: bool = False) -> Dict:
# # # # # # # #     """
# # # # # # # #     Karpathy-style LLM Council using Ollama backend.
# # # # # # # #     Modes: fast, lite, full
# # # # # # # #     """

# # # # # # # #     cfg = COUNCIL_MODES.get(mode)
# # # # # # # #     if not cfg:
# # # # # # # #         raise ValueError(f"Invalid mode '{mode}'. Choose from {list(COUNCIL_MODES)}")

# # # # # # # #     evidence = ""
# # # # # # # #     if search:
# # # # # # # #         raw_evidence = web_search(question)
# # # # # # # #         evidence = validate_evidence(question, raw_evidence)

# # # # # # # #     # ------------------------------------------------------
# # # # # # # #     # FAST MODE — single chairman answer
# # # # # # # #     # ------------------------------------------------------
# # # # # # # #     if mode == "fast":
# # # # # # # #         prompt = f"""
# # # # # # # # ORIGINAL QUESTION:
# # # # # # # # {question}

# # # # # # # # EXTERNAL EVIDENCE:
# # # # # # # # {evidence}

# # # # # # # # Answer the ORIGINAL QUESTION clearly and factually.
# # # # # # # # Do not describe the process. Only give the answer.
# # # # # # # # """
# # # # # # # #         final = await query_model(cfg["chairman"], prompt)
# # # # # # # #         return {"final": final}


# # # # # # # #     # ------------------------------------------------------
# # # # # # # #     # LITE MODE — generator → chairman refinement
# # # # # # # #     # ------------------------------------------------------
# # # # # # # #     if mode == "lite":
# # # # # # # #         gen_model = cfg["generators"][0]

# # # # # # # #         draft = await query_model(gen_model, question)

# # # # # # # #         synthesis_prompt = f"""
# # # # # # # # ORIGINAL QUESTION:
# # # # # # # # {question}

# # # # # # # # DRAFT ANSWER:
# # # # # # # # {draft}

# # # # # # # # EXTERNAL EVIDENCE:
# # # # # # # # {evidence}

# # # # # # # # Improve the draft and answer the ORIGINAL QUESTION directly.
# # # # # # # # """
# # # # # # # #         final = await query_model(cfg["chairman"], synthesis_prompt)

# # # # # # # #         return {
# # # # # # # #             "draft": draft,
# # # # # # # #             "final": final
# # # # # # # #         }


# # # # # # # #     # ------------------------------------------------------
# # # # # # # #     # FULL MODE — multi-model council
# # # # # # # #     # ------------------------------------------------------

# # # # # # # #     # ---------- Stage 1 : Parallel Generation ----------
# # # # # # # #     stage1 = await query_models_parallel(cfg["generators"], question)

# # # # # # # #     # ---------- Stage 2 : Peer Ranking ----------
# # # # # # # #     ranking_prompt = f"""
# # # # # # # # ORIGINAL QUESTION:
# # # # # # # # {question}

# # # # # # # # EXTERNAL EVIDENCE:
# # # # # # # # {evidence}

# # # # # # # # MODEL RESPONSES:
# # # # # # # # {stage1}

# # # # # # # # Rank the answers from best to worst and briefly justify.
# # # # # # # # """
# # # # # # # #     stage2 = await query_models_parallel(cfg["critics"], ranking_prompt)

# # # # # # # #     # ---------- Stage 3 : Chairman Synthesis ----------
# # # # # # # #     synthesis_prompt = f"""
# # # # # # # # You are the Chairman of an LLM Council. And you are answering a factual question.
# # # # # # # # RULES:
# # # # # # # # - If evidence is weak or missing, answer using your internal knowledge.
# # # # # # # # - If evidence contradicts known facts, IGNORE the evidence.
# # # # # # # # - Never fabricate titles or roles.

# # # # # # # # Question:
# # # # # # # # {question}

# # # # # # # # MODEL DRAFTS:
# # # # # # # # {stage1}

# # # # # # # # PEER REVIEWS:
# # # # # # # # {stage2}

# # # # # # # # Validated Evidence:
# # # # # # # # {evidence}

# # # # # # # # Answer with only the verified fact.

# # # # # # # # TASK:
# # # # # # # # Produce one accurate final answer to the ORIGINAL QUESTION.
# # # # # # # # Do not describe the process. Do not mention "synthesis".
# # # # # # # # Only answer the question directly.
# # # # # # # # """
# # # # # # # #     final = await query_model(cfg["chairman"], synthesis_prompt)

# # # # # # # #     return {
# # # # # # # #         "stage1": stage1,
# # # # # # # #         "stage2": stage2,
# # # # # # # #         "final": final,
# # # # # # # #     }

# # # # # # # """
# # # # # # # LLM Council orchestration (Ollama-based)
# # # # # # # Factual, year-aware, evidence-grounded
# # # # # # # """

# # # # # # # from .ollama_clnt import query_model, query_models_parallel
# # # # # # # from .config import COUNCIL_MODES
# # # # # # # from .search_tool import web_search


# # # # # # # # -------------------------------------------------------------------
# # # # # # # # Utility
# # # # # # # # -------------------------------------------------------------------

# # # # # # # def build_fact_prompt(question: str, evidence: str) -> str:
# # # # # # #     return f"""
# # # # # # # QUESTION (FACTUAL — YEAR-SENSITIVE):
# # # # # # # {question}

# # # # # # # AUTHORITATIVE FACTS (FROM SEARCH — MUST BE USED):
# # # # # # # {evidence if evidence else "NO FACTS FOUND"}

# # # # # # # RULES (STRICT):
# # # # # # # - If the facts explicitly state an answer, you MUST repeat it exactly.
# # # # # # # - Do NOT infer, guess, or generalize.
# # # # # # # - If the facts contradict your prior knowledge, the facts WIN.
# # # # # # # - If the facts do NOT contain the answer, reply exactly:
# # # # # # #   "Unable to verify from available evidence."

# # # # # # # Answer in ONE concise sentence.
# # # # # # # """


# # # # # # # # -------------------------------------------------------------------
# # # # # # # # Main Council Runner
# # # # # # # # -------------------------------------------------------------------

# # # # # # # async def run_council(
# # # # # # #     question: str,
# # # # # # #     mode: str = "lite",
# # # # # # #     search: bool = False,
# # # # # # # ):
# # # # # # #     """
# # # # # # #     Run the LLM Council with strict factual grounding.

# # # # # # #     Modes:
# # # # # # #     - fast: chairman only
# # # # # # #     - lite: generator + chairman
# # # # # # #     - full: multi-generator + critics + chairman
# # # # # # #     """

# # # # # # #     cfg = COUNCIL_MODES.get(mode)
# # # # # # #     if not cfg:
# # # # # # #         raise ValueError(f"Invalid mode '{mode}'. Choose from {list(COUNCIL_MODES)}")

# # # # # # #     # ---------------------------------------------------------------
# # # # # # #     # Step 1: Evidence collection (authoritative)
# # # # # # #     # ---------------------------------------------------------------
# # # # # # #     evidence = ""
# # # # # # #     if search:
# # # # # # #         evidence = web_search(question)

# # # # # # #     fact_prompt = build_fact_prompt(question, evidence)

# # # # # # #     # ---------------------------------------------------------------
# # # # # # #     # FAST MODE
# # # # # # #     # ---------------------------------------------------------------
# # # # # # #     if mode == "fast":
# # # # # # #         final = await query_model(cfg["chairman"], fact_prompt)
# # # # # # #         return {"final": final}

# # # # # # #     # ---------------------------------------------------------------
# # # # # # #     # LITE MODE
# # # # # # #     # ---------------------------------------------------------------
# # # # # # #     if mode == "lite":
# # # # # # #         gen_model = cfg["generators"][0]

# # # # # # #         draft = await query_model(gen_model, fact_prompt)

# # # # # # #         verify_prompt = f"""
# # # # # # # You are a factual verifier.

# # # # # # # Draft Answer:
# # # # # # # {draft}

# # # # # # # AUTHORITATIVE FACTS:
# # # # # # # {evidence if evidence else "NO FACTS FOUND"}

# # # # # # # RULES:
# # # # # # # - If the draft matches the facts, return it unchanged.
# # # # # # # - If incorrect or speculative, correct it using ONLY the facts.
# # # # # # # - If unverifiable, reply exactly:
# # # # # # #   "Unable to verify from available evidence."

# # # # # # # Return ONE sentence only.
# # # # # # # """
# # # # # # #         final = await query_model(cfg["chairman"], verify_prompt)

# # # # # # #         return {
# # # # # # #             "draft": draft,
# # # # # # #             "final": final,
# # # # # # #         }

# # # # # # #     # ---------------------------------------------------------------
# # # # # # #     # FULL MODE (Karpathy-style, but factual)
# # # # # # #     # ---------------------------------------------------------------

# # # # # # #     # Stage 1 — Parallel generation (fact-constrained)
# # # # # # #     stage1 = await query_models_parallel(
# # # # # # #         cfg["generators"],
# # # # # # #         fact_prompt,
# # # # # # #     )

# # # # # # #     # Stage 2 — Critics check correctness (not style)
# # # # # # #     critic_prompt = f"""
# # # # # # # You are a factual reviewer.

# # # # # # # QUESTION:
# # # # # # # {question}

# # # # # # # AUTHORITATIVE FACTS:
# # # # # # # {evidence if evidence else "NO FACTS FOUND"}

# # # # # # # MODEL ANSWERS:
# # # # # # # {stage1}

# # # # # # # TASK:
# # # # # # # - Identify which answers are factually correct.
# # # # # # # - Ignore writing quality.
# # # # # # # - List ONLY answers that strictly match the facts.
# # # # # # # """

# # # # # # #     stage2 = await query_models_parallel(
# # # # # # #         cfg["critics"],
# # # # # # #         critic_prompt,
# # # # # # #     )

# # # # # # #     # Stage 3 — Chairman verification (hard gate)
# # # # # # #     chairman_prompt = f"""
# # # # # # # You are the FINAL FACT VERIFIER.

# # # # # # # QUESTION:
# # # # # # # {question}

# # # # # # # AUTHORITATIVE FACTS:
# # # # # # # {evidence if evidence else "NO FACTS FOUND"}

# # # # # # # MODEL ANSWERS:
# # # # # # # {stage1}

# # # # # # # CRITIC FEEDBACK:
# # # # # # # {stage2}

# # # # # # # RULES (NON-NEGOTIABLE):
# # # # # # # - Use ONLY the authoritative facts.
# # # # # # # - If a correct answer exists, return it verbatim.
# # # # # # # - If facts are missing or conflicting, reply exactly:
# # # # # # #   "Unable to verify from available evidence."

# # # # # # # Return ONE sentence only.
# # # # # # # """

# # # # # # #     final = await query_model(cfg["chairman"], chairman_prompt)

# # # # # # #     return {
# # # # # # #         "stage1": stage1,
# # # # # # #         "stage2": stage2,
# # # # # # #         "final": final,
# # # # # # #     }

# # # # # # # councillm/council.py

# # # # # # from typing import Dict, Any
# # # # # # from .ollama_clnt import query_model, query_models_parallel
# # # # # # from .config import COUNCIL_MODES
# # # # # # from .search_tool import web_search


# # # # # # async def run_council(
# # # # # #     question: str,
# # # # # #     mode: str = "lite",
# # # # # #     search: bool = False,
# # # # # # ) -> Dict[str, Any]:
# # # # # #     """
# # # # # #     Run the LLM Council using Ollama.

# # # # # #     Modes:
# # # # # #       - fast : single chairman
# # # # # #       - lite : 1 generator + chairman
# # # # # #       - full : multiple generators + critics + chairman
# # # # # #     """

# # # # # #     if mode not in COUNCIL_MODES:
# # # # # #         raise ValueError(f"Invalid mode '{mode}'. Choose from {list(COUNCIL_MODES)}")

# # # # # #     cfg = COUNCIL_MODES[mode]

# # # # # #     # --------------------------------------------------
# # # # # #     # Optional web grounding
# # # # # #     # --------------------------------------------------
# # # # # #     evidence = ""
# # # # # #     if search:
# # # # # #         try:
# # # # # #             evidence = web_search(question)
# # # # # #         except Exception:
# # # # # #             evidence = ""

# # # # # #     # --------------------------------------------------
# # # # # #     # FAST MODE
# # # # # #     # --------------------------------------------------
# # # # # #     if mode == "fast":
# # # # # #         prompt = f"""
# # # # # # Answer the question FACTUALLY.

# # # # # # Question:
# # # # # # {question}

# # # # # # External Evidence (if any):
# # # # # # {evidence}

# # # # # # Rules:
# # # # # # - If unsure, say "I don't know"
# # # # # # - Prefer evidence over assumptions
# # # # # # """
# # # # # #         final = await query_model(cfg["chairman"], prompt)

# # # # # #         return {
# # # # # #             "final": final.strip(),
# # # # # #         }

# # # # # #     # --------------------------------------------------
# # # # # #     # LITE MODE
# # # # # #     # --------------------------------------------------
# # # # # #     if mode == "lite":
# # # # # #         gen_model = cfg["generators"][0]

# # # # # #         draft = await query_model(
# # # # # #             gen_model,
# # # # # #             f"Answer factually:\n{question}",
# # # # # #         )

# # # # # #         synthesis_prompt = f"""
# # # # # # You are the chairman.

# # # # # # Draft Answer:
# # # # # # {draft}

# # # # # # External Evidence:
# # # # # # {evidence}

# # # # # # Rules:
# # # # # # - Correct factual errors
# # # # # # - Prefer evidence
# # # # # # - If uncertain, say "I don't know"

# # # # # # Produce final answer:
# # # # # # """

# # # # # #         final = await query_model(cfg["chairman"], synthesis_prompt)

# # # # # #         return {
# # # # # #             "draft": draft.strip(),
# # # # # #             "final": final.strip(),
# # # # # #         }

# # # # # #     # --------------------------------------------------
# # # # # #     # FULL MODE (Karpathy-style)
# # # # # #     # --------------------------------------------------

# # # # # #     # Stage 1 — parallel generation
# # # # # #     stage1 = await query_models_parallel(
# # # # # #         cfg["generators"],
# # # # # #         f"Answer factually:\n{question}",
# # # # # #     )

# # # # # #     # Stage 2 — critique / ranking
# # # # # #     critique_prompt = f"""
# # # # # # Question:
# # # # # # {question}

# # # # # # Evidence:
# # # # # # {evidence}

# # # # # # Model Answers:
# # # # # # {stage1}

# # # # # # Critique answers.
# # # # # # Point out factual errors.
# # # # # # """

# # # # # #     stage2 = await query_models_parallel(cfg["critics"], critique_prompt)

# # # # # #     # Stage 3 — chairman synthesis
# # # # # #     synthesis_prompt = f"""
# # # # # # You are the chairman.

# # # # # # Question:
# # # # # # {question}

# # # # # # Evidence:
# # # # # # {evidence}

# # # # # # Draft Answers:
# # # # # # {stage1}

# # # # # # Critiques:
# # # # # # {stage2}

# # # # # # Rules:
# # # # # # - Prefer consensus
# # # # # # - Reject incorrect answers
# # # # # # - If evidence conflicts, say "I don't know"

# # # # # # Produce final verified answer:
# # # # # # """

# # # # # #     final = await query_model(cfg["chairman"], synthesis_prompt)

# # # # # #     return {
# # # # # #         "stage1": stage1,
# # # # # #         "stage2": stage2,
# # # # # #         "final": final.strip(),
# # # # # #     }


# # # # # #-----------------------------------------------------------------------

# # # # # from typing import Dict, List
# # # # # from .ollama_clnt import query_model, query_models_parallel
# # # # # from .search_tool import web_search
# # # # # from councillm.runtime import get_runtime_roles

# # # # # # ============================================================
# # # # # # Core Council Runner
# # # # # # ============================================================

# # # # # async def run_council(
# # # # #     question: str,
# # # # #     mode: str = "lite",
# # # # #     search: bool = False,
# # # # # ) -> Dict:
# # # # #     """
# # # # #     Run LLM Council using Ollama.

# # # # #     Modes:
# # # # #     - fast : Chairman only
# # # # #     - lite : Generator → Chairman
# # # # #     - full : Multi-generator → Critic → Chairman

# # # # #     Returns dict with at least:
# # # # #         { "final": str }
# # # # #     """

# # # # #     roles = get_runtime_roles()

# # # # #     generators = roles["generators"]
# # # # #     critics = roles["critics"]
# # # # #     chairman = roles["chairman"]


# # # # #     if not chairman:
# # # # #         raise RuntimeError("Chairman model not configured")

# # # # #     evidence = ""
# # # # #     if search:
# # # # #         evidence = web_search(question)

# # # # #     # ========================================================
# # # # #     # FAST MODE — chairman only
# # # # #     # ========================================================
# # # # #     if mode == "fast":
# # # # #         prompt = _chairman_prompt(
# # # # #             question=question,
# # # # #             drafts=None,
# # # # #             reviews=None,
# # # # #             evidence=evidence,
# # # # #         )
# # # # #         final = await query_model(chairman, prompt)
# # # # #         return {"final": final}

# # # # #     # ========================================================
# # # # #     # LITE MODE — single generator + chairman
# # # # #     # ========================================================
# # # # #     if mode == "lite":
# # # # #         if not generators:
# # # # #             raise RuntimeError("No generator models configured")

# # # # #         draft = await query_model(generators[0], question)

# # # # #         prompt = _chairman_prompt(
# # # # #             question=question,
# # # # #             drafts={"draft": draft},
# # # # #             reviews=None,
# # # # #             evidence=evidence,
# # # # #         )

# # # # #         final = await query_model(chairman, prompt)

# # # # #         return {
# # # # #             "draft": draft,
# # # # #             "final": final,
# # # # #         }

# # # # #     # ========================================================
# # # # #     # FULL MODE — Karpathy-style council
# # # # #     # ========================================================
# # # # #     if mode == "full":
# # # # #         if not generators:
# # # # #             raise RuntimeError("No generator models configured")

# # # # #         # ---------- Stage 1: Parallel generation ----------
# # # # #         stage1 = await query_models_parallel(generators, question)

# # # # #         # ---------- Stage 2: Critic review ----------
# # # # #         stage2 = {}
# # # # #         if critics:
# # # # #             review_prompt = _critic_prompt(
# # # # #                 question=question,
# # # # #                 drafts=stage1,
# # # # #                 evidence=evidence,
# # # # #             )
# # # # #             stage2 = await query_models_parallel(critics, review_prompt)

# # # # #         # ---------- Stage 3: Chairman synthesis ----------
# # # # #         final_prompt = _chairman_prompt(
# # # # #             question=question,
# # # # #             drafts=stage1,
# # # # #             reviews=stage2,
# # # # #             evidence=evidence,
# # # # #         )

# # # # #         final = await query_model(chairman, final_prompt)

# # # # #         return {
# # # # #             "stage1": stage1,
# # # # #             "stage2": stage2,
# # # # #             "final": final,
# # # # #         }

# # # # #     raise ValueError(f"Invalid mode: {mode}")


# # # # # # ============================================================
# # # # # # Prompt Builders (hallucination-resistant)
# # # # # # ============================================================

# # # # # def _critic_prompt(question: str, drafts: Dict, evidence: str) -> str:
# # # # #     return f"""
# # # # # You are a factual reviewer.

# # # # # QUESTION:
# # # # # {question}

# # # # # DRAFT ANSWERS:
# # # # # {_format_block(drafts)}

# # # # # EXTERNAL EVIDENCE:
# # # # # {evidence if evidence else "None"}

# # # # # TASK:
# # # # # - Identify factual errors
# # # # # - Flag hallucinations
# # # # # - Prefer evidence over model memory
# # # # # - Be concise and precise
# # # # # """


# # # # # def _chairman_prompt(
# # # # #     question: str,
# # # # #     drafts: Dict | None,
# # # # #     reviews: Dict | None,
# # # # #     evidence: str,
# # # # # ) -> str:
# # # # #     return f"""
# # # # # You are the Chairman of an LLM Council.

# # # # # QUESTION:
# # # # # {question}

# # # # # DRAFT ANSWERS:
# # # # # {_format_block(drafts) if drafts else "None"}

# # # # # CRITIC REVIEWS:
# # # # # {_format_block(reviews) if reviews else "None"}

# # # # # EXTERNAL EVIDENCE (AUTHORITATIVE):
# # # # # {evidence if evidence else "None"}

# # # # # RULES:
# # # # # - Evidence overrides model memory
# # # # # - If unsure, say "I don't know"
# # # # # - Do NOT hallucinate
# # # # # - Answer clearly and directly

# # # # # FINAL ANSWER:
# # # # # """


# # # # # # ============================================================
# # # # # # Utilities
# # # # # # ============================================================

# # # # # def _format_block(data: Dict | None) -> str:
# # # # #     if not data:
# # # # #         return "None"

# # # # #     return "\n\n".join(
# # # # #         f"[{model}]\n{text}"
# # # # #         for model, text in data.items()
# # # # #         if text
# # # # #     )

# # # # # councillm/council.py

# # # # from .ollama_clnt import query_model, query_models_parallel
# # # # from .search_tool import web_search


# # # # async def run_council(
# # # #     question: str,
# # # #     *,
# # # #     generators: list[str],
# # # #     critics: list[str],
# # # #     chairman: str,
# # # #     mode: str = "lite",
# # # #     search: bool = False,
# # # # ):
# # # #     evidence = web_search(question) if search else ""

# # # #     # ---------- FAST ----------
# # # #     if mode == "fast":
# # # #         prompt = f"""
# # # # Question:
# # # # {question}

# # # # Evidence:
# # # # {evidence}

# # # # Answer factually. If unsure, say so.
# # # # """
# # # #         final = await query_model(chairman, prompt)
# # # #         return {"final": final}

# # # #     # ---------- LITE ----------
# # # #     if mode == "lite":
# # # #         draft = await query_model(generators[0], question)

# # # #         prompt = f"""
# # # # Draft:
# # # # {draft}

# # # # Evidence:
# # # # {evidence}

# # # # Fix errors. Add missing facts. Remove speculation.
# # # # """
# # # #         final = await query_model(chairman, prompt)
# # # #         return {"draft": draft, "final": final}

# # # #     # ---------- FULL ----------
# # # #     stage1 = await query_models_parallel(generators, question)

# # # #     ranking_prompt = f"""
# # # # Question:
# # # # {question}

# # # # Evidence:
# # # # {evidence}

# # # # Answers:
# # # # {stage1}

# # # # Rank answers best → worst and explain briefly.
# # # # """
# # # #     stage2 = await query_models_parallel(critics, ranking_prompt)

# # # #     synthesis_prompt = f"""
# # # # Question:
# # # # {question}

# # # # Evidence:
# # # # {evidence}

# # # # Answers:
# # # # {stage1}

# # # # Critiques:
# # # # {stage2}

# # # # Produce the most accurate final answer.
# # # # """
# # # #     final = await query_model(chairman, synthesis_prompt)

# # # #     return {
# # # #         "stage1": stage1,
# # # #         "stage2": stage2,
# # # #         "final": final,
# # # #     }

# # # from councillm.runtime import get_runtime
# # # from councillm.ollama_clnt import query_model, query_models_parallel

# # # async def run_council(question: str):
# # #     cfg = get_runtime()

# # #     # Stage 1
# # #     drafts = await query_models_parallel(
# # #         cfg["generators"],
# # #         f"Answer factually:\n{question}"
# # #     )

# # #     # Stage 2
# # #     critiques = await query_models_parallel(
# # #         cfg["critics"],
# # #         f"Question:\n{question}\nDrafts:\n{drafts}\nCritique them."
# # #     )

# # #     # Stage 3
# # #     final = await query_model(
# # #         cfg["chairman"],
# # #         f"""
# # # Question:
# # # {question}

# # # Drafts:
# # # {drafts}

# # # Critiques:
# # # {critiques}

# # # Produce the most accurate final answer.
# # # """
# # #     )

# # #     return final

# # # councillm/council.py

# # # councillm/council.py

# # from .ollama_clnt import query_model, query_models_parallel
# # from .search_tool import web_search


# # async def run_council(
# #     question: str,
# #     *,
# #     generators: list[str],
# #     critics: list[str],
# #     chairman: str,
# #     mode: str = "lite",
# #     search: bool = False,
# # ):
# #     evidence = web_search(question) if search else ""

# #     # ---------- FAST ----------
# #     if mode == "fast":
# #         prompt = f"""
# # Question:
# # {question}

# # Evidence:
# # {evidence}

# # Answer factually. If unsure, say so.
# # """
# #         final = await query_model(chairman, prompt)
# #         return {"final": final}

# #     # ---------- LITE ----------
# #     if mode == "lite":
# #         draft = await query_model(generators[0], question)

# #         prompt = f"""
# # Draft:
# # {draft}

# # Evidence:
# # {evidence}

# # Fix errors. Add missing facts. Remove speculation.
# # """
# #         final = await query_model(chairman, prompt)
# #         return {"draft": draft, "final": final}

# #     # ---------- FULL ----------
# #     stage1 = await query_models_parallel(generators, question)

# #     ranking_prompt = f"""
# # Question:
# # {question}

# # Evidence:
# # {evidence}

# # Answers:
# # {stage1}

# # Rank answers best → worst and explain briefly.
# # """
# #     stage2 = await query_models_parallel(critics, ranking_prompt)

# #     synthesis_prompt = f"""
# # Question:
# # {question}

# # Evidence:
# # {evidence}

# # Answers:
# # {stage1}

# # Critiques:
# # {stage2}

# # Produce the most accurate final answer.
# # """
# #     final = await query_model(chairman, synthesis_prompt)

# #     return {
# #         "stage1": stage1,
# #         "stage2": stage2,
# #         "final": final,
# #     }

# # councillm/council.py

# from .ollama_clnt import query_model, query_models_parallel
# from .search_tool import web_search
# from .utils import log


# async def run_council(
#     question: str,
#     *,
#     generators: list[str],
#     critics: list[str],
#     chairman: str,
#     mode: str = "lite",
#     search: bool = False,
#     verbose: bool = True,
# ):
#     def v(msg):
#         if verbose:
#             log(msg)

#     evidence = ""
#     if search:
#         v("[Search] Gathering external evidence")
#         evidence = web_search(question)

#     # ---------- FAST ----------
#     if mode == "fast":
#         v("[Stage] Chairman answering directly")
#         final = await query_model(
#             chairman,
#             f"Question:\n{question}\n\nEvidence:\n{evidence}",
#         )
#         return {"final": final}

#     # ---------- LITE ----------
#     if mode == "lite":
#         v("[Stage 1] Generator drafting")
#         draft = await query_model(generators[0], question)
#         v(f"  • {generators[0]} ✓")

#         v("[Stage 2] Chairman refining")
#         final = await query_model(
#             chairman,
#             f"Draft:\n{draft}\n\nEvidence:\n{evidence}",
#         )
#         v(f"  • {chairman} ✓")

#         return {"draft": draft, "final": final}

#     # ---------- FULL ----------
#     v("[Stage 1] Generating responses")
#     stage1 = {}
#     for m in generators:
#         stage1[m] = await query_model(m, question)
#         v(f"  • {m} ✓")

#     v("[Stage 2] Peer review")
#     stage2 = {}
#     critique_prompt = f"""
# Question:
# {question}

# Evidence:
# {evidence}

# Answers:
# {stage1}

# Critique and rank the answers.
# """
#     for m in critics:
#         stage2[m] = await query_model(m, critique_prompt)
#         v(f"  • {m} ✓")

#     v("[Stage 3] Chairman synthesis")
#     final = await query_model(
#         chairman,
#         f"""
# Question:
# {question}

# Evidence:
# {evidence}

# Answers:
# {stage1}

# Critiques:
# {stage2}

# Produce the best final answer.
# """,
#     )
#     v(f"  • {chairman} ✓")

#     return {
#         "stage1": stage1,
#         "stage2": stage2,
#         "final": final,
#     }
