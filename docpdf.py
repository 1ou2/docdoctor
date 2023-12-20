import pypdf


if __name__ == "__main__":
    from pypdf import PdfReader

    reader = PdfReader("mdp.pdf")
    nb_pages = len(reader.pages)
    print(f"nb pages {nb_pages}")
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        print(page.extract_text())