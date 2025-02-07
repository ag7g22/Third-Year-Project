<template>
    <!-- This is the navigation menu for the different pages (Testing purposes only) -->
    <header>
        <nav>
            <ul>
                <li><router-link to="/main">Main</router-link></li>
                <li><router-link to="/authentication">Authentication</router-link></li>
                <li><router-link to="/dashboard">Dashboard</router-link></li>
            </ul>
        </nav>
    </header>
</template>

<script>
// Vue Component, to be referenced in other parts of the app:
export default {
    name: 'Header'
}
</script>

<style lang="scss" scoped>
/** This section applies SCSS styles to the component: */
header {
    background-color: #f8f8f8;
    padding: 10px 20px;
    text-align: center;
}
nav ul {
    list-style: none;
    padding: 0;
}
nav ul li {
    display: inline;
    margin-right: 10px;
}
</style>