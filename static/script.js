document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("employeeTable");
    const headers = table.tHead.rows[0].cells; // Получаем ячейки заголовков
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.rows); // Получаем строки данных

    Array.from(headers).forEach((header, columnIndex) => {
        header.addEventListener("click", () => {
            const isAscending = header.dataset.sortOrder !== "asc"; // Проверяем направление сортировки
            header.dataset.sortOrder = isAscending ? "asc" : "desc";

            rows.sort((rowA, rowB) => {
                const cellA = rowA.cells[columnIndex].textContent.trim().toLowerCase();
                const cellB = rowB.cells[columnIndex].textContent.trim().toLowerCase();

                if (cellA < cellB) return isAscending ? -1 : 1;
                if (cellA > cellB) return isAscending ? 1 : -1;
                return 0;
            });

            // Перемещаем строки в отсортированном порядке
            rows.forEach(row => tbody.appendChild(row));
        });
    });
});
