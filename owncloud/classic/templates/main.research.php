<?php
style('rds', array('style', "rds-web.css"));
script('rds', array("rds-web.umd.min.js"));
?>

<div id='app'>
    <rdsWeb />
</div>


<script>
    new Vue({
        components: {
            rdsWeb: rds-web
        }
    }).$mount('#app')
</script>