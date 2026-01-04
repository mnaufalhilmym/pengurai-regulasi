def pdf_to_spreadsheet(pdf_bytes: bytes):
    import io
    import pandas as pd
    from pdf_to_json import pdf_to_json

    parsed = pdf_to_json(pdf_bytes)

    df = pd.DataFrame(parsed)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)

    return output.getvalue()
