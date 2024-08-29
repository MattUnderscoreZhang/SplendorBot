server:
    pdm run fastapi dev index.py --host 0.0.0.0 --port 8080

tailwind:
    npx tailwind -i assets/css/tailwind_imports.css -o assets/css/tailwind.css --watch
