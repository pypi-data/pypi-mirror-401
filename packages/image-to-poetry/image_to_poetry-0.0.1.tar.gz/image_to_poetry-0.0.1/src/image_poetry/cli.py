import argparse
import sys
from image_poetry.generator import generate_poem

def main():
    parser = argparse.ArgumentParser(description="Generate a poem from an image.")
    parser.add_argument("image_path", help="Path to the input image file")

    args = parser.parse_args()

    print(f"Analyzing image: {args.image_path}...")
    try:
        poem = generate_poem(args.image_path)
        print("\n--- Generated Poem ---\n")
        print(poem)
        print("\n----------------------\n")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
