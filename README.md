🏠 SmartHome-App - README 📋
✨ A Python GUI smart home manager with multi-property support (Tkinter + CSV persistence) ✨

🌟 Features
🔧 Core Components
File	           Description
backend.py 🖥️	  All device & home logic (SmartPlug, SmartTV, SmartSpeaker, SmartHome)
frontend.py 🎨	Tkinter GUI for single-home control
challenge.py 🚀	Extended multi-home manager with CSV saving/loading

Key Functionality:

🔌 SmartPlug: Adjust wattage (0-150W)

📺 SmartTV: Change channels (1-734)

🔊 SmartSpeaker: Switch services (Amazon/Apple/Spotify)

➕ Add/remove devices dynamically

💾 Auto-save homes to homes.csv

🚀 Quick Start
Clone & run:

bash
Copy
git clone https://github.com/Achilleas05/SmartHome-App.git
cd SmartHome-App
python frontend.py  # Single-home mode
python challenge.py # Multi-home mode
Requirements:

Python 3.x

Tkinter (usually pre-installed)

🖥️ GUI Preview
Single-Home Mode (frontend.py)

Copy
[Turn All On] [Turn All Off]  
📺 TV: On (Channel 42) [Toggle] [Edit] [Delete]  
🔊 Speaker: Off (Spotify) [Toggle] [Edit] [Delete]  
🔌 Plug: Off (75W) [Toggle] [Edit] [Delete]  
[Add New Device]  
Multi-Home Mode (challenge.py)

Copy
🏠 Home 1 (3 devices, 2 active) [Manage]  
🏠 Home 2 (1 device, 0 active) [Manage]  
[Add New Home] [Save & Exit]  
📂 File Structure
Copy
SmartHome-App/
├── backend.py       # Device classes + SmartHome logic
├── frontend.py      # Single-home GUI  
├── challenge.py     # Multi-home manager + CSV persistence  
├── homes.csv        # Auto-generated config storage  
└── README.md
🛠 Development Notes
🔍 Code Highlights
Backend: Strict input validation (e.g., TV channels 1-734 only)

Frontend: Grid layout adapts to device count

Challenge: CSV maintains state between sessions

🧪 Testing
Run manual tests via GUI or:

python
Copy
# Example test in backend.py
tv = SmartTV()  
tv.set_channel(500)  # Valid  
tv.set_channel(1000) # Raises error  
📜 Academic Declaration
⚠️ This is my original work for University of Portsmouth coursework (M30299).

👨‍💻 100% self-written code

📚 Referenced only Python docs & lecture materials

🤖 No AI code generators used

📬 Contact
📧 Email: achilleasachilleos0@gmail.com
