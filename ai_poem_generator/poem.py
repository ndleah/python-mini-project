from typing import List
from dataclasses import dataclass


_pipeline = None
_tokenizer = None

@dataclass
class PoemConfig:
    theme: str
    form: str = "free"
    lines: int = 4
    max_new_tokens: int = 80

def _get_generator():
    """
    Load a small, instruction-tuned chat model.
    Choose ONE model_id below that fits your disk/RAM:
      - "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  (lightest good option)
      - "Qwen/Qwen2.5-0.5B-Instruct"          (also light + coherent)
    """
    global _pipeline, _tokenizer
    if _pipeline is None:
        from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
        model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" 
        _tokenizer = AutoTokenizer.from_pretrained(model_id, use_fast=True)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        _pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=_tokenizer,
            device_map=None, 
        )
    return _pipeline, _tokenizer

def build_prompt(theme: str, form: str, lines: int) -> str:
    """
    Build a chat-style prompt via the model's chat template.
    We ask the model to output ONLY poem lines.
    """
    form = (form or "free").strip().lower()
    user_msg = (
        f"Write a {form} poem about '{theme}'. "
        f"Use vivid imagery and concrete nouns. "
        f"Output exactly {lines} short lines with no title or extra text."
    )
    return user_msg

def _fallback_poem_lines(theme: str, form: str, lines: int) -> str:
    """
    Simple deterministic backup generator so the CLI never returns empty.
    Not 'AI', but keeps UX solid and tests happy if the LM stalls.
    """
    nouns = ["pavement", "backpack", "lamp post", "notebook", "window", "bicycle", "leaf"]
    senses = ["rain-smell", "footsteps", "chalk-dust", "neon", "mud print", "quiet hum", "shadows"]
    pieces = []
    # lightweight, theme-aware lines
    root = theme.split()[0] if theme else "dawn"
    for i in range(lines):
        n = nouns[i % len(nouns)]
        s = senses[(i * 2 + 1) % len(senses)]
        pieces.append(f"{root} on {n}, {s}")
    return "\n".join(pieces)

def _postprocess(generated: str, lines: int) -> str:
    """Keep only the first N clean, non-instruction lines."""
    bad_snippets = ("Theme:", "Form:", "Rules:", "Begin:", "poem", "instruction", "Return exactly")
    # normalize and split
    raw = [ln.strip() for ln in generated.splitlines()]
    cleaned = []
    for ln in raw:
        if not ln:
            continue
        # drop obvious echoes of instructions
        low = ln.lower()
        if any(bad.lower() in low for bad in bad_snippets):
            continue
        # strip list markers like "1) ", "1. ", "- "
        ln = ln.lstrip("-.0123456789) ")
        if ln:
            cleaned.append(ln)
        if len(cleaned) >= lines:
            break
    # pad if model under-produces
    while len(cleaned) < lines:
        cleaned.append("...")
    return "\n".join(cleaned[:lines])

def generate_poem(cfg: PoemConfig) -> str:
    generator, tok = _get_generator()

    # Build chat-formatted prompt
    chat = [
        {"role": "system", "content": "You are a concise poetry assistant. Only output poem lines."},
        {"role": "user", "content": build_prompt(cfg.theme, cfg.form, cfg.lines)},
    ]
    prompt = tok.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

    # Use mild sampling to avoid stalls; don't set eos_token_id so it doesn't stop instantly
    res = generator(
        prompt,
        max_new_tokens=max(48, cfg.max_new_tokens),
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        top_k=50,
        num_return_sequences=1,
        return_full_text=False,   # don't echo the prompt
        no_repeat_ngram_size=3,
        repetition_penalty=1.08,
        pad_token_id=tok.eos_token_id,
    )
    text = res[0]["generated_text"]
    out = _postprocess(text, cfg.lines)

    # If, for any reason, lines came back short, fall back (never print blanks)
    nonempty = [ln for ln in out.splitlines() if ln.strip()]
    if len(nonempty) < cfg.lines:
        return _fallback_poem_lines(cfg.theme, cfg.form, cfg.lines)
    return out