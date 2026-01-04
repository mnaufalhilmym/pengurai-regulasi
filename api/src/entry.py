from workers import Response, WorkerEntrypoint


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        from urllib.parse import urlparse

        # Parse the incoming request URL
        url = urlparse(request.url)
        url_path = url.path.rstrip("/")

        # Parse multipart/form-data
        try:
            form = await request.form_data()
        except Exception:
            return Response(
                "Invalid multipart/form-data",
                status=400,
            )

        # Expect file field named "doc"
        file = form.get("doc")
        if file is None or file.size == 0:
            return Response("Missing or invalid PDF file field 'doc'", status=400)

        # Read uploaded file bytes
        pdf_bytes = await file.bytes()

        if url_path == "/to_json":
            import json
            from pdf_to_json import pdf_to_json

            parsed = pdf_to_json(pdf_bytes)
            return Response(
                json.dumps(parsed), headers={"Content-Type": "application/json"}
            )

        if url_path == "/to_spreadsheet":
            from pdf_to_spreadsheet import pdf_to_spreadsheet

            output = pdf_to_spreadsheet(pdf_bytes)
            return Response(
                output,
                headers={
                    "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "Content-Disposition": 'attachment; filename="output.xlsx"',
                },
            )

        return Response(
            "Invalid path. Valid path are /to_json and /to_spreadsheet\n\n"
            + "This API is a parser to automatically extract the structure and content of Indonesian regulation from PDF file into JSON or spreadsheet",
            status=404,
        )
