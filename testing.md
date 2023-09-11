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
    var time;
    var timeS = 0;

    function countTime() {
        let time = new Date();
        document.getElementById("time").innerHTML = (time.getSeconds() + timeS) % 60;
    }

    setInterval(countTime, 1000);
    countTime();
</script>
<button type="button" onclick="timeS = (timeS + 30) % 60">Time travel.</button>