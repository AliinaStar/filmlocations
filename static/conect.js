fetch('http://localhost:8000/tasks/')
  .then(response => response.json())
  .then(data => {
    console.log(data); // Обробка даних
  })
  .catch(error => console.error('Error:', error));
