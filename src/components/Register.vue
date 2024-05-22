<template>
    <h1>Register</h1>
    <form action="/register" method="post">
        <label for="username">Username</label>
        <input type="text" name="username"/>
        <label for="password">Password</label>
        <input type="text" name="password">
        <label for="firstname">Firstname</label>
        <input type="text" name="firstname">
        <label for="lastname">Lastname</label>
        <input type="text" name="lastname">
        <label for="email">Email</label>
        <input type="email" name="email">
        <label for="location">Location</label>
        <input type="location" name="location">
        <label for="biography">Biography</label>
        <textarea name="biography"></textarea>
        <label for="photo">Photo</label>
        <input type="file" name="photo">
    </form>
</template>