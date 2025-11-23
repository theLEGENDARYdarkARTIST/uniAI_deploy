# import os
# from fastapi import FastAPI, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment vars
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Models
# CHAT_MODEL = "models/gemini-2.0-flash"
# IMAGE_MODEL = "models/gemini-2.5-flash-image"

# app = FastAPI(title="UniAI — Gemini Backend")

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # -------- CHAT --------
# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat")
# async def chat(req: ChatRequest):
#     model = genai.GenerativeModel(CHAT_MODEL)
#     response = model.generate_content(req.message)
#     return {"reply": response.text}


# # -------- SUMMARY --------
# @app.post("/summarize")
# async def summarize(file: UploadFile = File(...)):
#     text = (await file.read()).decode("utf-8", errors="ignore")

#     model = genai.GenerativeModel(CHAT_MODEL)
#     response = model.generate_content(f"Summarize this:\n{text}")
#     return {"summary": response.text}


# # -------- IMAGE GENERATION --------
# class ImageRequest(BaseModel):
#     prompt: str

# @app.post("/image")
# async def image(req: ImageRequest):
#     model = genai.GenerativeModel(IMAGE_MODEL)
#     response = model.generate_content(req.prompt)

#     # Gemini image output is base64
#     if hasattr(response, "generated_images"):
#         img_base64 = response.generated_images[0]
#         return {"base64": img_base64}

#     return {"error": "Image generation failed."}



import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Models
CHAT_MODEL = "models/gemini-2.0-flash"
IMAGE_MODEL = "models/gemini-2.5-flash-image"

app = FastAPI(title="UniAI — Gemini Backend")

@app.get("/")
def home():
    return {"status": "UniAI backend is running"}

# ----- CORS -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],          
)

# -------- CHAT --------
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    model = genai.GenerativeModel(CHAT_MODEL)
    response = model.generate_content(req.message)
    return {"reply": response.text}


# -------- SUMMARY --------
@app.post("/summarize")
async def summarize(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8", errors="ignore")
    model = genai.GenerativeModel(CHAT_MODEL)
    response = model.generate_content(f"Summarize this:\n{text}")
    return {"summary": response.text}


# -------- IMAGE GENERATION (BASE64) --------
class ImageRequest(BaseModel):
    prompt: str

@app.post("/image")
async def image(req: ImageRequest):
    try:
        model = genai.GenerativeModel(IMAGE_MODEL)
        response = model.generate_content(req.prompt)

        # Gemini returns base64
        if hasattr(response, "generated_images") and response.generated_images:
            img_base64 = response.generated_images[0]
            return {"base64": img_base64}

        return {"error": "No image returned. Possibly quota exceeded."}

    except Exception as e:
        return {"error": str(e)}