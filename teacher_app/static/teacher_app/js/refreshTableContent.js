function refreshTableContent(classId) {
    // 更新表格标题
    var tableTitle = document.getElementById('table-title');
    if (tableTitle) {
        tableTitle.textContent = '班级详情'; // 更改为你想要的新标题
    }
    var table = document.getElementById('dataTable');
    var thead = table.getElementsByTagName('thead')[0];
    var tbody = table.getElementsByTagName('tbody')[0];
    // 清除现有的表格内容
     // 清除现有的 thead 和 tbody 内容
    thead.innerHTML = '';
    tbody.innerHTML = '';

    // 定义新的 thead 内容
    var newTheadData = ["姓名", "学号", "班级", "操作"];

    // 创建新的标题行
    var headerRow = thead.insertRow();
    newTheadData.forEach(function(headerText) {
        var headerCell = document.createElement("th");
        headerCell.textContent = headerText;
        headerRow.appendChild(headerCell);
    });

    // 使用Ajax请求从后端获取数据
    $.ajax({
        url: '/teacher/class/get_students/' + classId + '/',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // 使用返回的数据更新表格内容
            data.forEach(function(student) {
                var row = tbody.insertRow();
                var nameCell = row.insertCell();
                nameCell.textContent = student.name;
                var numberCell = row.insertCell();
                numberCell.textContent = student.student_number;
                var classCell = row.insertCell();
                classCell.textContent = student.class_id;
                // 在“操作”列添加“删除”和“重置密码”按钮
                var actionCell = row.insertCell();
                actionCell.innerHTML = '<button class="button-class" onclick="deleteRow(this)">删除</button>' +
                                       '<button class="button-class" onclick="resetPassword(this)">重置密码</button>';
            });
        }
    });

    // 显示“返回初始”按钮
    document.getElementById('newButton').style.display = 'block';
    document.getElementById('newClassButton').style.display = 'none';

    // 由于刷新按钮可能被重新创建，确保再次绑定事件
    bindButtonEvents();
    addClass();
}

// 使用事件委托监听按钮点击
function bindButtonEvents() {
    // 绑定刷新按钮事件
    document.getElementById('dataTable').addEventListener('click', function(event) {
        if (event.target && event.target.id.startsWith('refreshButton-')) {
            var parts = event.target.id.split('-');
            var classId = parts[1];
            // 现在你可以使用classId来获取班级信息
            refreshTableContent(classId);
        }
    });
    // 绑定刷新按钮事件
    document.getElementById('refreshButton').addEventListener('click', refreshTableContent);
    // 绑定返回初始按钮事件
    document.getElementById('newButton').addEventListener('click',
        function () {
            // 使用原始HTML恢复表格
            document.getElementById('dataTable').innerHTML = originalTableHTML;
            // 隐藏返回初始按钮
            this.style.display = 'none';
            document.getElementById('newClassButton').style.display = 'block';
        }
    );
    document.getElementById('dataTable').addEventListener('click',
        function (event) {
            // 检查是否点击了刷新按钮
            if (event.target.id === 'refreshButton') {
                refreshTableContent();
            }
            // 检查是否点击了返回初始按钮
            else if (event.target.id === 'newButton') {
                // 使用原始HTML恢复表格
                document.getElementById('dataTable').innerHTML = originalTableHTML;
                // 隐藏返回初始按钮
                event.target.style.display = 'none';
            }
        }
    );
}
