Just a collection of all of my finished projects (now with extra polishing!)  
Status of the project enumerates whether it works or not along with my reflection (as of Fall 2023)  
To be safe: I'd appreciate it if you wouldn't rip from my work when this goes public (super arrogant, I know), as I worked really hard on these and that's kinda rude. Thanks!

* 2022  
    * [Fall][2022 fall]

* 2023  
    * [Spring][2023 spring]
    * [Summer][2023 summer]
    * [Fall][2023 fall]

[2022 fall]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/2022/fall
[2023 spring]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/2023/spring
[2023 summer]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/2023/summer
[2023 fall]:  https://usernamethatisnttaken.github.io/ProjectsPortfolio/2023/fall

## 2023 Spring
### Simulations
#### Boids:
<p id = boidText></p>
<script>
    const fs = require("fs");
    var boidText = "My implementation of boids (https://en.wikipedia.org/wiki/Boids)\nStatus: Functional with one major bug (atan calculation is off -> why they sort of peel from the flock when facing at certain angles)\n"
    document.getElementById("boidText").innerHTML = boidText;
</script>


#### Renderer:
A slightly better 3D renderer with a placement GUI (v2)  
Status: Functional with a few bugs (movement normalization, occlusion clipping)


## 2023 Summer
I'm currently in the process of porting/doing cleanup on projects from here onward!
### Data Analysis
#### Experimental Data Compression:
A data transformer I made as an experiment that takes a large amount of input data and encodes/decodes it into/from a PNG file  
Status: One single bug (*ahem* feature): Image size hardcapping seems to be broken, so it is softcapped by processing time instead. Please do not try to do 1E7+ entries, as that image's size is >10MB, and I don't want your computer to hate you


## 2023 Fall
Empty for now  
Currently working on adding a pages deployment as well.


## Other Pages
_In progress, of course_  
[About me][about me]  
Link to [my testing page][testing] (for me)

[about me]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/about
[testing]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/testing