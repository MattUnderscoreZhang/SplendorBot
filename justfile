server:
    pdm run fastapi dev server/index.py --host 0.0.0.0 --port 8080

tailwind:
    npx tailwind -i css/input.css -o css/output.css --watch
