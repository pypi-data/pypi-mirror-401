import argparse
from .core import html_file_to_pdf

def main():
    parser = argparse.ArgumentParser(description="Convert HTML to PDF")
    parser.add_argument("input", help="Input HTML file")
    parser.add_argument("output", help="Output PDF file")
    args = parser.parse_args()

    html_file_to_pdf(args.input, args.output)
    print(f"✅ PDF generated: {args.output}")

# Optional: allow running directly
if __name__ == "__main__":
    main()
