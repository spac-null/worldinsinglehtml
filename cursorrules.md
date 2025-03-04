
.cursorrules for HTML 3D Game Development
Overview
This .cursorrules file is designed to optimize Cursor, an AI programming assistant, for developing HTML-based 3D games using WebGL, Three.js, Cannon.js, Socket.io, Express.js, and SQLite. It provides a structured set of rules to guide Cursor in generating clean, performant, and modular code for client-server 3D games with real-time multiplayer capabilities, as inspired by the provided architecture diagram. The rules focus on best practices for WebGL rendering, physics simulation, asset management, and server-client synchronization.
Features
Project Type: HTML 3D game development for web browsers.
Primary Libraries: Three.js (3D rendering), Cannon.js (physics), Socket.io (real-time multiplayer), Express.js (server logic).
Performance Goals: Hardware acceleration, low latency, real-time multiplayer, and cross-browser compatibility.
Code Standards: JavaScript (ES6+), 2-space indentation, JSDoc comments, and modular file structures.
Testing and Optimization: Includes rules for performance profiling, asset optimization, and multiplayer testing.
Getting Started
Prerequisites
Cursor AI Assistant: Ensure you have Cursor installed and configured in your development environment.
Node.js and npm: Required for server-side components (Express.js, Socket.io) and testing tools (Jest, Playwright).
Web Browser: A modern browser (Chrome, Firefox, etc.) for client-side testing and development.
Text Editor/IDE: Any editor that supports Cursor (e.g., VS Code with Cursor integration).
Installation
Clone or Create Your Project:
Create a new directory for your HTML 3D game project or clone an existing repository.
Navigate to your project root.
Add the .cursorrules File:
Save the .cursorrules JSON content (provided earlier) as .cursorrules in your project’s root directory.
Initialize Your Project:
Run npm init -y to create a package.json file.
Install required dependencies:
bash
npm install three cannon.js socket.io express sqlite3
Configure Cursor:
Ensure Cursor is integrated with your IDE and recognizes the .cursorrules file.
Cursor will automatically apply the rules when generating or suggesting code.
Usage
Basic Workflow
Start a New 3D Game:
Use Cursor to generate an index.html file with a basic WebGL canvas, linked to main.js for Three.js initialization.
Example prompt for Cursor: "Create a basic Three.js scene with a rotating cube and a camera system."
Add Game Components:
Use Cursor to generate scripts for player.js, bot.js, weapons.js, and camera.js under the scripts/game_logic directory, following the file structure in .cursorrules.
Example prompt: "Implement a player management system using Three.js and Cannon.js physics for collision detection."
Set Up Server-Side Logic:
Use Cursor to create server.js with Express.js and Socket.io for real-time multiplayer, and database.js for SQLite integration.
Example prompt: "Set up an Express.js server with Socket.io for real-time player synchronization and SQLite for game state storage."
Optimize and Test:
Use Cursor to optimize assets (e.g., minify textures, cache 3D models) and generate tests with Jest and Playwright.
Example prompt: "Write unit tests for the player movement logic using Jest and performance tests with Lighthouse."
File Structure
Follow the recommended structure from .cursorrules:
project-root/
├── index.html
├── styles.css
├── main.js
├── server.js
├── assets/
│   ├── models/
│   ├── textures/
│   ├── sounds/
│   ├── shaders/
│   └── character_models/
├── scripts/
│   ├── client/
│   │   ├── game_logic/
│   │   │   ├── player.js
│   │   │   ├── bot.js
│   │   │   ├── weapons.js
│   │   │   └── camera.js
│   │   ├── rendering/
│   │   │   ├── renderer.js
│   │   │   └── scene.js
│   │   ├── ui/
│   │   │   ├── menu.js
│   │   │   └── hud.js
│   │   └── networking/
│   │       └── socketClient.js
│   ├── server/
│   │   ├── game_logic/
│   │   │   ├── gameState.js
│   │   │   └── roomManagement.js
│   │   ├── networking/
│   │   │   └── socketServer.js
│   │   └── database/
│   │       └── database.js
├── .cursorrules
└── package.json
Contributing
We welcome contributions to improve this .cursorrules file or the associated HTML 3D game project. Please follow these steps:
Fork the repository (if hosted on GitHub or similar).
Create a branch for your changes: git checkout -b feature/your-feature.
Make your changes and commit them with clear messages.
Submit a pull request with details of your changes.
Testing
Unit Tests: Use Jest to test game logic (e.g., player movement, bot AI).
Integration Tests: Use Playwright to test multiplayer synchronization and UI interactions.
Performance Tests: Use Lighthouse and WebGL Inspector to profile rendering and network performance.
Database Tests: Ensure SQLite operations (e.g., game state storage) are tested with SQLite-specific tools.
Optimization Tips
Minify and compress assets (textures, models) to reduce load times.
Use Web Workers for heavy computations (e.g., physics, AI pathfinding).
Optimize shaders and reduce draw calls for better WebGL performance.
Implement lazy-loading for textures and efficient server-client synchronization with Socket.io.
Troubleshooting
Cursor Not Recognizing .cursorrules: Ensure the file is in the project root and your IDE is configured to integrate with Cursor.
Performance Issues: Check for unoptimized shaders, large assets, or inefficient server-client sync; use the optimization rules in .cursorrules.
Browser Compatibility: Test across Chrome, Firefox, and Safari using Playwright or manual testing.
License
This .cursorrules file is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments
Inspired by the architecture diagram for HTML 3D game development, showcasing Three.js, Cannon.js, Socket.io, Express.js, and SQLite.
Built with guidance from web resources on HTML 3D game development and Cursor best practices.
Screenshots
(Include a screenshot or diagram of the expected architecture or game UI here, e.g., the provided diagram or a mockup of a 3D game interface.)
Documentation
For a complete guide on configuring and customizing this .cursorrules file, refer to the Official Documentation (#) (if applicable, or create a docs/ folder with detailed Markdown files).
Notes:
This README assumes the .cursorrules file is part of a GitHub repository or similar platform. Adjust the links and hosting details as needed.
You can add a screenshot or diagram (e.g., the provided architecture image) to visually represent the project structure or game UI.
The license and acknowledgments can be customized based on your project’s needs or preferences.
Let me know if you’d like to refine any section, add more details, or include specific examples or images!