from gmakepdf.core import html_to_pdf, html_file_to_pdf

with open("demo.html", "r", encoding="utf-8") as f:
    html = f.read()

pdf_bytes = html_to_pdf(html)

with open("from_html_text.pdf", "wb") as f:
    f.write(pdf_bytes)

print("✅ PDF generated from demo.html text")

html_file_to_pdf('demo.html', "test_html_file_to_pdf.pdf")
