from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import FastAPI, UploadFile, File, HTTPException
from dotenv import load_dotenv
from groq import Groq
import os
import base64

load_dotenv()
print("Groq Key:", os.getenv("GROQ_API_KEY"))
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Image uploaded successfully",
        "filename": file.filename,
           "path": file_path
    }
def encode_image(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
@app.get("/analyze")
def analyze(filename: str):

    image_path = f"uploads/{filename}"

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    image_data = encode_image(image_path)
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
"text": """Analyze this marine image.

Return only the following information.
Do not write any introduction or conclusion.
Do not use Markdown.
Do not use ** or #.

Species Name:
Scientific Name:
Habitat:
Diet:
Conservation Status:
Interesting Facts:
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}"
                        }
                    }
                ]
            }
        ]
    )

    return {
        "analysis": response.choices[0].message.content
}