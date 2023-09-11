---
permalink: /testing/
---
Hello World!

[x] Learn basic markdown  
[ ] Learn more markdown

[About][About link]

[About link]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/about

<div id="time"></div>

<script>
    var timeS = 0;

    setInterval(countTime, 1000);

    function countTime() {
        var time = new Date();
        document.getElementById("time").innerHTML = time.getSeconds() + timeS;
    }
</script>
<button type="button" onclick="timeS = (timeS + 30) % 60">Time travel.</button>