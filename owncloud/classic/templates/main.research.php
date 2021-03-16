<?php
style('rds', array('style', "rds.css"));
script('rds', array("rds.umd.min.js"));
?>

<div id='app'>
    <rds />
</div>


<script>
    OC.rds = {
        server: <?php print_unescaped($_['cloudURL']); ?>
    }

    new Vue({
        components: {
            rds
        }
    }).$mount('#app')
</script>