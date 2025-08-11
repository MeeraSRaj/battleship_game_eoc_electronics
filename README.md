# Battleship - Naval Armada

An interactive two-player Battleship game developed in Python using the Pygame library, designed to run on a Raspberry Pi 5 platform. The project replicates the classic naval strategy board game with digital interaction, visual effects, and audio feedback, optimized for touchscreen kiosks or embedded systems.

---

## Abstract
This project presents the design and implementation of a two-player Battleship game running on Raspberry Pi 5. It focuses on recreating the gameplay experience with added UI/UX elements, event-driven programming, and sound integration suitable for portable or educational systems. The solution is cost-effective and can be operated on touchscreen kiosks, embedded setups, or via remote desktop access.

---

## Keywords
Raspberry Pi 5, Pygame, Battleship, Game Development, Python, Touchscreen Interface, Embedded Gaming

---

## System Design and Architecture
The game follows a modular architecture:
- **Grid Engine**: Generates 10x10 grids for each player, enabling precise ship placement and attack tracking.
- **Rendering Module**: Uses Pygame to display grids, ships, and hit/miss outcomes.
- **Sound Module**: Plays explosion and splash effects to provide immediate auditory feedback.
- **Input System**: Supports mouse and touch input; the 'R' key rotates ships during placement.
- **Game Logic**: Manages ship placement validation, turn handling, and win conditions.

---

## Software Implementation
- **Language**: Python 3
- **Library**: Pygame
- **Platform**: Raspberry Pi OS (64-bit)
- **Features**:
  - Welcome screen with Start and Instructions options
  - Player name input
  - Drag-and-drop ship placement with rotation support
  - Real-time visual and audio feedback
  - Win condition detection with restart/quit options
  - Input validation to prevent invalid moves
- **Code Structure**:
  - `Player` class for grid operations, ship deployment, and attack handling
  - Main game loop for managing gameplay flow and state transitions

---

## Hardware Implementation
- Operated primarily via **VNC Viewer** to remotely access the Raspberry Pi 5
- Supports mouse or touchscreen interaction
- Audio output through HDMI or remote desktop audio forwarding
- Can be connected to an HDMI display or touchscreen if required
- Portable and cost-effective, suitable for classroom or demonstration use

---

## Results
The game achieved:
- Consistent 60 FPS rendering with smooth animations
- Accurate handling of ship placement, attack validation, and win detection
- Enhanced user engagement through audio-visual feedback
- Stable remote operation using VNC Viewer without performance loss

---

## Future Scope
Planned improvements include:
1. **AI-Based Single Player Mode**: Incorporating algorithms for intelligent targeting (e.g., probability-based strategies, reinforcement learning).
2. **Networked Multiplayer**: Implementing local or online multiplayer via socket programming or web APIs.
3. **UI/UX Enhancements**: Additional animations, visual themes, and responsive layouts.

---

## References
1. [Raspberry Pi 5 Technical Specifications](https://www.raspberrypi.com/products/raspberry-pi-5/) – Raspberry Pi Foundation, 2023  
2. [Pygame Documentation](https://www.pygame.org/docs/) – Pygame Community, 2023  
3. [Python Language Reference](https://www.python.org/doc/) – Python Software Foundation, 2023  
4. [VNC Connect – Remote Access Solutions](https://www.realvnc.com/) – RealVNC Ltd., 2023

---

## Getting Started
### Prerequisites
- Raspberry Pi 5 with Raspberry Pi OS (64-bit)
- Python 3 installed
- Pygame library installed:
```bash
pip install pygame
