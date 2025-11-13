import argparse
from poem import PoemConfig, generate_poem

def parse_args():
    p = argparse.ArgumentParser(
        description="Generate a short AI poem in the terminal."
    )
    p.add_argument("theme", help="Theme/topic of the poem, e.g., 'first rain on campus'")
    p.add_argument("--form", default="free", help="Style hint: free | haiku | sonnet | limerick")
    p.add_argument("--lines", type=int, default=4, help="Number of lines to return")
    p.add_argument("--max-new-tokens", type=int, default=80, help="Upper bound on model generation length")
    return p.parse_args()

def main():
    args = parse_args()
    poem = generate_poem(PoemConfig(
        theme=args.theme,
        form=args.form,
        lines=args.lines,
        max_new_tokens=args.max_new_tokens,
    ))
    print(poem)

if __name__ == "__main__":
    main()
