<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>جلب بيانات كل ثانية</title>
</head>
<body>
    <h1>جلب بيانات JSON كل ثانية</h1>
    <div id="data-container">جاري تحميل البيانات...</div>

    <script>
        function fetchData() {
            fetch('scrap.php') 
                .then(response => response.json())
                .then(data => {
                    document.getElementById('data-container').innerText = JSON.stringify(data, null, 2);
                })
                .catch(error => console.error('خطأ في جلب البيانات:', error));
        }

        setInterval(fetchData, 1000);

        fetchData();
    </script>
</body>
</html>
