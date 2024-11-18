document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("employeeTable");
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows); // Получаем строки данных

    const columnIndex = 0; // Укажите индекс столбца для сортировки (0 для "ФИО")
    const isAscending = true; // Укажите направление сортировки: true для возрастания, false для убывания

    // Сортируем строки только по столбцу "ФИО"
    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].textContent.trim().toLowerCase();
        const cellB = rowB.cells[columnIndex].textContent.trim().toLowerCase();

        if (cellA < cellB) return isAscending ? -1 : 1;
        if (cellA > cellB) return isAscending ? 1 : -1;
        return 0;
    });

    // Перемещаем отсортированные строки обратно в `<tbody>`
    rows.forEach(row => tbody.appendChild(row));
});

document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("theme-toggle");
    const body = document.body;

    // Проверяем, есть ли сохранённая тема
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      body.classList.add(savedTheme);
    }

    // Переключение темы
    themeToggle.addEventListener("click", () => {
      if (body.classList.contains("dark-theme")) {
        body.classList.remove("dark-theme");
        localStorage.setItem("theme", ""); // Очищаем тему
      } else {
        body.classList.add("dark-theme");
        localStorage.setItem("theme", "dark-theme"); // Сохраняем тёмную тему
      }
    });
  });

  function logout() {
    fetch('/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }).then(() => {
      window.location.href = '/';
    }).catch(err => console.error('Ошибка при выходе:', err));
  }