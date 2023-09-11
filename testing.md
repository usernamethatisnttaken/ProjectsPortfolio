---
permalink: /testing/
---
Hello World!

[x] Learn basic markdown  
[ ] Learn more markdown

[About][About link]

[About link]: https://usernamethatisnttaken.github.io/ProjectsPortfolio/about

<p id="time">0</p>

<script>
    var timeS = 0;
    var clock = new Date();

    setInterval(countTime, 1000);

    function countTime() {
        document.getElementById("time").innerHTML = clock.getSeconds() + timeS;
    }
</script>
<button type="button" onclick="timeS = (timeS + 30) % 60">Time travel.</button>