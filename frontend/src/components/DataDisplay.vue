<template>
  <div class="data-display">
    <h2>Data from Backend</h2>
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <ul v-if="items && items.length">
      <li v-for="item in items" :key="item.ProductID">
        <strong>{{ item.Name }}</strong> (ID: {{ item.ProductID }})
        <br />
        Price: ${{ item.ListPrice.toFixed(2) }}
        <span v-if="item.Color"> | Color: {{ item.Color }}</span>
        <span v-if="item.Size"> | Size: {{ item.Size }}</span>
      </li>
    </ul>
    <div v-else-if="!loading && !error">No data available.</div>
  </div>
</template>

<script>
export default {
  name: 'DataDisplay',
  data() {
    return {
      items: [],
      loading: true,
      error: null,
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      try {
        // Assuming the backend API is running on port 5000
        // and accessible via /api/data
        const response = await fetch('/api/data');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.items = data;
      } catch (e) {
        this.error = `Failed to fetch data: ${e.message}`;
        console.error(e);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.data-display {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  max-width: 800px;
  margin: 20px auto; /* Center the box */
}
.error {
  color: #e74c3c; /* A slightly nicer red */
  font-weight: bold;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  padding: 15px;
  margin-bottom: 10px; /* Space between items */
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  text-align: left; /* Align text to the left within list items */
}
li strong {
  font-size: 1.2em;
  color: #3498db; /* Blue color for product name */
}
li br {
  display: none; /* Hide the <br> if we use block/flex for layout */
}
/* Add some spacing for item details */
li span {
  margin-right: 10px;
  font-size: 0.9em;
  color: #555;
}
</style>
