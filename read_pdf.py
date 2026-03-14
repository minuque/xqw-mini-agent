import pdfplumber

with pdfplumber.open("references/Hello-Agents-V1.0.2-20260210.pdf") as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    # Read first 25 pages to find chapter 1.1
    for i, page in enumerate(pdf.pages[:25]):
        text = page.extract_text()
        if text:
            print(f"--- Page {i + 1} ---")
            print(text[:2000])
            print()
