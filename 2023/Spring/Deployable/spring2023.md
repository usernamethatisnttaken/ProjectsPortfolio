---
permalink: /2023/spring/
---
## Simulations
### Boids:
My implementation of boids (https://en.wikipedia.org/wiki/Boids)  
Status: Functional with one major bug (atan calculation is off -> why they sort of peel from the flock when facing at certain angles)
<details>
    <summary>Controls</summary>
    
    To run: python 2023/Spring/Simulations/boids/main.py  
    Sim:
     * N - Add a single boid per tick
     * M - Add a chunk of boids per tick

</details>
![](boids.gif)

### Renderer:
A slightly better 3D renderer with a placement GUI (v2)  
Status: Functional with a few bugs (movement normalization, occlusion clipping)

<details>
    <summary>Controls</summary>
    
    To run: python 2023/Spring/Simulations/renderer/main.py  
    In GUI:  
    * RClick - Enter cube  
    * LClick - Remove cube
    * Shift/Ctrl - Layer up/down  
    * Escape - Exit GUI to simulation  
    In simulation:  
    * Up/Down - Rotate dynamic x  
    * Right/Left - Rotate dynamic z  
    * W/S - Move forward/backward  
    * A/D - Rotate perspective around the orgin?  

</details>
![](renderer.gif)