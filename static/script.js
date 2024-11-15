<script>
function sortTable(columnIndex) {
    const table = document.getElementById("employeeTable");
    const rows = Array.from(table.tBodies[0].rows); // Получить строки тела таблицы
    const isAsc = table.dataset.sortOrder !== "asc"; // Определить направление сортировки
    table.dataset.sortOrder = isAsc ? "asc" : "desc"; // Переключить направление

    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].textContent.trim().toLowerCase();
        const cellB = rowB.cells[columnIndex].textContent.trim().toLowerCase();
        if (cellA < cellB) return isAsc ? -1 : 1;
        if (cellA > cellB) return isAsc ? 1 : -1;
        return 0;
    });

    // Переместить строки в отсортированном порядке
    const tbody = table.tBodies[0];
    rows.forEach(row => tbody.appendChild(row));
}
</script>
