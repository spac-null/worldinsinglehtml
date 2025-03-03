# CLAUDE.md - Repository Guidelines

## Build/Lint/Test Commands
- No specific build system detected
- View HTML files directly in browser
- Use `python -m http.server` to serve locally (if needed)

## Code Style Guidelines

### HTML Structure
- Use HTML5 doctype and semantic tags
- Include proper viewport meta tags
- Include appropriate meta tags for mobile compatibility

### CSS Guidelines
- Use CSS variables for colors and theming
- Follow BEM naming convention for classes
- Mobile-first responsive design with media queries

### JavaScript Guidelines
- Organize code into functions with clear responsibilities
- Use const/let instead of var
- Prefix private functions with underscore
- Use camelCase for variables and functions
- Use event delegation when possible
- Prefer ES6+ syntax (arrow functions, template literals, etc.)

### THREE.js Guidelines
- Initialize scene, camera, renderer in separate functions
- Group related 3D objects under parent objects
- Implement proper lighting and shadows
- Use object.userData for storing custom data