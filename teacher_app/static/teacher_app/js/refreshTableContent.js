/* 定义一个全局变量，稍后在 window.onload 中对其进行初始化8*/
var originalTableHTML;
function refreshTableContent(classId) {
    console.log("Requested class ID:", classId);  // 调试语句，确认获取到的classId
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
    var newTheadData = ["姓名", "学号", "操作"];

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
            console.log("Success response:", data);  // 成功响应的调试信息
            // 使用返回的数据更新表格内容
            data.forEach(function(student) {
                var row = tbody.insertRow();
                var nameCell = row.insertCell();
                nameCell.textContent = student.name;
                var numberCell = row.insertCell();
              numberCell.textContent = student.userid;  // 修改为 student.userid

                // 在“操作”列添加“删除”和“重置密码”按钮
                var actionCell = row.insertCell();
                actionCell.innerHTML = '<button class="button-class delete-class">删除</button>' +
                                       '<button class="button-class" onclick="resetPassword(this)">重置密码</button>';
            });
        },

        error: function(xhr, status, error) {
            console.log("Error response:", xhr, status, error);  // 错误响应的调试信息
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
    // 为所有的“详情”按钮绑定点击事件
    document.querySelectorAll('.refresh-button').forEach(button => {
        button.addEventListener('click', function() {
            var classId = this.getAttribute('data-class-id'); // 从按钮的data-class-id属性获取班级ID
            refreshTableContent(classId); // 调用refreshTableContent函数并传递班级ID
        });
    });
}


function bindDeleteButtonEvents() {
    // 由于每一行都可能有删除按钮，最好是用事件委托来绑定事件，而不是直接绑定到每个按钮上
    document.getElementById('dataTable').addEventListener('click',
        function(event) {
            // 检查点击的是否是删除按钮
            if (event.target && event.target.classList.contains('delete-class')) {
                 var confirmation = confirm("确定要删除吗？"); // 确认删除操作
                if (confirmation) {
                    // 获取按钮所在的行（tr元素）
                    var row = event.target.closest('tr');
                    // 删除该行
                    row.remove();
                }
            }
        })
}


function resetPassword(button) {
    var row = button.parentNode.parentNode; // 获取按钮所在的行
    var nameCell = row.cells[0]; // 假设姓名在第一列
    alert("重置 " + nameCell.textContent + " 的密码");
}




// 确保在页面加载完成后调用函数以设置事件监听器
window.onload = function() {
    addClass();
    originalTableHTML = document.getElementById('dataTable').innerHTML;
    bindButtonEvents(); // 绑定
    bindDeleteButtonEvents();
}
