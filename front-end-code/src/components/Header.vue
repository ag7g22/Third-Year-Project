<template>
    <header>
        <nav>
            <ul>
                <li><router-link to="/main">Main</router-link></li>
                <li><router-link to="/login">Login</router-link></li>
            </ul>
        </nav>
    </header>
</template>

<script>
export default {
    name: 'Header'
}
</script>

<style lang="scss" scoped>
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