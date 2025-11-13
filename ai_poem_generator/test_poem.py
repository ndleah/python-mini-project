import types
from poem import build_prompt, PoemConfig, generate_poem

class _FakePipe:
    def __call__(self, prompt, **kwargs):
        # Return deterministic multi-line continuation for tests
        return [{
            "generated_text": "glittering streets\nreflections ripple softly\nmidnight hum returns\nlights fade into dawn\n"
        }]

def test_build_prompt_mentions_theme_and_lines():
    prompt = build_prompt("ocean breeze", "haiku", 3)
    assert "ocean breeze" in prompt
    assert "exactly 3" in prompt

def test_generate_poem_line_count(monkeypatch):
    # Monkeypatch the loader to avoid downloading models in CI
    import poem
    def _fake_get_generator():
        def apply_chat_template(chat, tokenize=False, add_generation_prompt=True):
            # Simple mock that concatenates messages
            parts = []
            for msg in chat:
                parts.append(f"{msg['role']}: {msg['content']}")
            return "\n".join(parts)
        
        tok = types.SimpleNamespace(
            eos_token_id=50256,  # gpt2 eos
            apply_chat_template=apply_chat_template
        )
        return _FakePipe(), tok
    monkeypatch.setattr(poem, "_get_generator", _fake_get_generator)
    out = generate_poem(PoemConfig(theme="city rain", form="free", lines=4))
    lines = [ln for ln in out.splitlines() if ln.strip()]
    assert len(lines) == 4
    # Check content is non-empty and textual
    assert all(isinstance(ln, str) and len(ln) > 0 for ln in lines)
