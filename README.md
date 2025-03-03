# Virtual Park Experience

A collection of interactive web-based 3D experiences using Three.js, inspired by The Legend of Zelda: Ocarina of Time N64 visuals.

## Setup

This project uses a conda environment for easy setup.

### Requirements
- Miniconda or Anaconda installed on your system
- A modern web browser

### Installation

1. Clone this repository
2. Run the start script:
   ```
   ./start.sh
   ```
   This will:
   - Activate the conda environment
   - Install required packages if needed
   - Start the server on http://localhost:8000

3. Open your browser and navigate to http://localhost:8000

### Manual Setup

If you prefer to set up manually:

1. Create and activate the conda environment:
   ```
   conda create -y -n virtualpark python=3.10
   conda activate virtualpark
   ```

2. Install dependencies:
   ```
   pip install flask
   ```

3. Run the server:
   ```
   python server.py
   ```

## Experiences

### virtualPark.html
A Zelda N64-inspired virtual park where you control a blocky bird flying through different zones. Collect coins, explore, and enjoy the low-poly aesthetics.

### parkVR.html
A simpler bird's eye view virtual park experience with tap-to-fly controls.

### worldmemory.html
A 3D file system explorer rendered as a memory palace.

## Controls

### virtualPark.html
- Arrow keys / WASD: Move the bird
- Spacebar: Jump/fly higher
- Click: Interact with objects

### parkVR.html
- Tap: Fly to location

## Development

- Built with Three.js
- Mobile-optimized for touch interfaces
- Low-poly aesthetic inspired by N64 era games