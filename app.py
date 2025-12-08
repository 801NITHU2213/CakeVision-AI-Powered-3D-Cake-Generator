import os
import requests
import base64
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
import torch

load_dotenv()

app = Flask(__name__, static_folder='../Frontend')
CORS(app)

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
print("STABILITY_API_KEY =", STABILITY_API_KEY)
if not STABILITY_API_KEY:
    raise ValueError("Missing STABILITY_API_KEY in environment variables")

GEN_DIR = os.path.join(os.path.dirname(__file__), "../Frontend/static/generated")
os.makedirs(GEN_DIR, exist_ok=True)

try:
    print("Loading MiDaS model...")
    midas = torch.hub.load("intel-isl/MiDaS", "DPT_Hybrid")
    midas.eval()
    transform = torch.hub.load("intel-isl/MiDaS", "transforms").dpt_transform
    print("MiDaS model loaded.")
except Exception as e:
    print("MiDaS model failed to load:", e)
    exit(1)

def pick_depth_image(prompt):
    prompt = prompt.lower()
    if "3 tier" in prompt or "three tier" in prompt:
        return "/static/depth_outputs/depth_3tier.png"
    elif "2 tier" in prompt or "two tier" in prompt:
        return "/static/depth_outputs/depth_2tier.png"
    elif "1 tier" in prompt or "single tier" in prompt:
        return "/static/depth_outputs/depth_1tier.png"
    else:
        return "/static/depth_outputs/depth_base.png"

def pick_top_image(prompt):
    p = prompt.lower()
    if "chocolate" in p:
        return "/static/cake_tops/chocolate.jpg"
    elif "strawberry" in p:
        return "/static/cake_tops/strawberry.jpg"
    elif "yellow" in p:
        return "/static/cake_tops/yellow.jpg"
    else:
        return "/static/cake_tops/plain.jpg"

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    user_prompt = data.get("prompt", "")

    # Automatically optimize every prompt for seamless cake sides
    SIDE_HINTS = " seamless side view strip pattern, no background, no plate, repeating horizontally"
    final_prompt = user_prompt + SIDE_HINTS

    body = {
        "text_prompts": [{"text": final_prompt}],
        "cfg_scale": 7,
        "height": 768,
        "width": 1344,
        "samples": 1,
        "steps": 30,
    }
    try:
        response = requests.post(
            "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={
                "Authorization": f"Bearer {STABILITY_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json=body
        )
        if response.status_code == 200:
            image_data = response.json()
            image_base64 = image_data["artifacts"][0]["base64"]
            image_bytes = base64.b64decode(image_base64)
            filename = f"cake_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

            filepath = os.path.join(GEN_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)

            artificial_output_url = pick_depth_image(user_prompt)
            image_url = f"/static/generated/{filename}"
            top_image_url = pick_top_image(user_prompt)

            resp = {
                "image_url": image_url,
                "artificial_output_url": artificial_output_url,
                "top_image_url": top_image_url,
                "texture": image_url,
                "depthmap": artificial_output_url,
                "message": "Image and depth map ready"
            }
            return jsonify(resp)
        else:
            print("Stability error:", response.text)
            return jsonify({"error": f"Stability API error: {response.text}"}), 500
    except Exception as e:
        print("Exception:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)