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
    var clock = new Date();

    function countTime() {
        document.getElementById("time").innerHTML = clock.getSeconds() + timeS;
        console.log(time.getSeconds);
    }

    setInterval(countTime, 1000);
    countTime();
</script>
<button type="button" onclick="timeS = (timeS + 30) % 60">Time travel.</button>