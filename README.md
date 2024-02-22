# Projects_Portfolio
Just a collection of all of my finished personal projects (now with extra polishing!)  
Status of the project enumerates whether it works or not along with my reflection (as of Fall 2023)  
You're free to check out any of these projects and use ideas or methods that you like for yourself, but I'd appreciate if you wouldn't rip from this repo (i.e. Ctrl-A > Ctrl-C > Ctrl-V, you know how it is)
Thanks!


## 2022 Fall
### Simulations
#### Cube Simulation:
A basic 3D renderer (v1)  
Status: Seems to be broken for some reason

#### Collision Simulation:
Simulates a bunch of colliding spheres  
Status: Buggy but functional (has problems with offsetting at certain gravity values, no GUI, ...)

#### Pathfinders:
Simulates one of three different pathfinding algorithms  
Status: Non-optimized but functional. I also like my custom one (Rivulet), as it seems like a weird implementation of A* that CERTAINLY has some problems


## 2023 Spring
### Simulations
#### Boids:
My implementation of boids (https://en.wikipedia.org/wiki/Boids)  
Status: Functional with one major bug (atan calculation is off -> why they sort of peel from the flock when facing at certain angles)

#### Renderer:
A slightly better 3D renderer with a placement GUI (v2)  
Status: Functional with a few bugs (movement normalization, occlusion clipping)


## 2023 Summer
I'm currently in the process of porting/doing cleanup on projects from here onward!  
(projects pending)
### Data Analysis
#### Experimental Data Compression:
A data transformer I made as an experiment that takes a large amount of input data and encodes/decodes it into/from a PNG file  
Status: One single bug (*ahem* feature): Image size hardcapping seems to be broken, so it is softcapped by processing time instead  
Please do not try to do 1E7+ entries, as that image's size is >10MB, and I don't want your computer to hate you as much as mine does :)


## 2023 Fall
Empty for now (projects pending)  

Working on adding a pages deployment as well, so that should be done at some point in the future

## 2023 Winter  
Empty for now (projects pending)
