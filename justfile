server:
    pdm run fastapi dev server/index.py --host 0.0.0.0 --port 8080

tailwind:
    npx tailwind -i css/tailwind_imports.css -o css/tailwind.css --watch
