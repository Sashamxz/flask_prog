<template>
  <div>
    <h1>Список постів</h1>
    <ul>
      <li v-for="post in posts" :key="post.url">
        <h2>{{ post.title }}</h2>
        <p>{{ post.body }}</p>
        <p>Автор: <a :href="post.author_url">{{ post.author }}</a></p>
        <p>Дата публікації: {{ formatDate(post.timestamp) }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      posts: [],
    };
  },
  created() {
    this.fetchPosts();
  },
  methods: {
    fetchPosts() {
      axios
        .get('http://127.0.0.1:5000/api/posts/')
        .then(response => {
          this.posts = response.data.posts;
        })
        .catch(error => {
          console.log(error);
        });
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getDate()}.${date.getMonth() + 1}.${date.getFullYear()}`;
    },
  },
};
</script>


<style>
h1 {
  font-size: 2rem;
  text-align: center;
  margin: 2rem 0;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 2rem 0;
  border: 1px solid #ccc;
  padding: 1rem;
}
</style>