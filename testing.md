---
permalink: /testing/
---
Hello World!

[x] Learn basic markdown  
[ ] Learn more markdown

[About][About link]

[About link]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/about

<p id="time"></p>

<script>
    var timeS = 0;
    while(true) {
        var time = new Date();
        document.getElementById("time").htmlt(ime.getSeconds() + timeS);
    }
</script>
<button type="button" onclick="timeS = (timeS + 30) % 60">Time travel.</button>