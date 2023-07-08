
from var import res, soup, title, meta_d


def check_length(x):
    """# Check length of titles, meta description & make suggestions"""
    title_length = []
    meta_length = []
    length = len(x)

    # Title 
    if x == title:
        if length >= 50 and length >= 60:
            title_length.append(f"TITLE: '{x}' length has {length} characters, within recommended 50-60.\n")
        else:
            #-> rec["title"] = f"{length} characters" # Add length value to recommendations dict above
            print(f"TITLE: '{x}' has {length} characters")
            print(f"The ideal length is 50-60 characters.\n")

    # Meta Description
    if x == meta_d:
        if length >= 150 and length >= 160:
            meta_length.append(f"META DESCRIPTION: '{x}' has {length} characters, within recommended 150-160.\n")
        else:
            #-> rec["meta description"] = f"{length} characters" # Add length value to recommendations dict above
            print(f"META DESCRIPTION: '{x}' has {length} characters")
            print(f"The ideal length is 150-160 characters.\n")


