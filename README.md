🚀 **OVERVIEW**

This project generates cake images using a custom GenAI model and then visualizes the cake in 3D using Babylon.js.

Users simply describe their cake in natural language.
The system then:

Generates a side texture of the cake.

Generates a separate top-view texture.

Wraps both textures onto a 3D cylinder.

Allows free rotation, zoom, and pan using an interactive viewer.

It feels like holding the cake in your hand. 🍰✨

🧠 **TECH STACK**
Backend (Python + Flask)

OpenAI / Diffusion-based image generation

Custom prompt engineering

Automatic top-view + side-view segmentation

Saves and serves images via endpoints

Frontend

HTML, CSS, JavaScript

Babylon.js for 3D rendering

Texture mapping (side + top)

Interactive camera (zoom, rotate, pan)

🎯 **FEATURES**

✅ Generate cake designs from text
✅ Dual textures (top + side) for realism
✅ 3D viewer with full controls
✅ Zoom, rotate, pan
