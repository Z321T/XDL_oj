function addClass() {
    // 获取弹窗元素
    var modal = document.getElementById("myModal");
    // 获取打开弹窗的按钮元素
    var btn = document.getElementById("newClassButton");
    // 获取关闭按钮元素
    var span = document.getElementsByClassName("close")[0];
    // 当用户点击按钮时，打开弹窗
    btn.onclick = function () {
        modal.style.display = "block";
    }
    // 当用户点击 x 按钮时，关闭弹窗
    span.onclick = function () {
        modal.style.display = "none";
    }
    // 当用户点击弹窗外的区域时，关闭弹窗
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
    // 获取确定按钮元素
    var confirmBtn = document.getElementById("confirmButton");

    // 当用户点击确定按钮时，执行相关操作（例如收集数据等）并关闭弹窗
    confirmBtn.onclick = function () {
        // 获取班级名称输入字段的值
        var name = document.getElementById('classNameInput').value;
        var initialPassword = document.getElementById('initialPasswordInput').value;
        // 获取文件输入元素并提取文件
        var fileInput = document.getElementById('excelFileInput');
        var file = fileInput.files[0];

        // 使用 FormData 对象封装数据
        var formData = new FormData();
        formData.append('name', name);
        formData.append('initialPassword', initialPassword);
        formData.append('file', file);

        console.log('Sending data to backend:', {
            name: name,
            initialPassword: initialPassword,
            file: file.name
        });
        if (name.trim() === "" || initialPassword.trim() === "" || !file) {
            // 数据为空，显示错误模态框
            $('#emptyDataModal').modal('show');
            return; // 不执行后续的AJAX请求
        }
        else {
            $.ajax({
                url: '/teacher/class/create/',  // 后端处理上传的API端点
                method: 'POST',
                processData: false,  // 告诉jQuery不要处理发送的数据
                contentType: false,  // 告诉jQuery不要设置Content-Type请求头
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: formData,
                success: function (response) {
                    // 处理后端响应
                    if (response.message === '班级创建成功') {
                        alert('上传成功');
                        // 成功上传后,可能需要进行一些操作，如刷新页面等
                    }
                    else {
                        alert(response.message);
                    }
                    modal.style.display = "none";
                },
                error: function (error) {
                    console.error(error);
                    if (error.status === 400) {
                        alert('请求的数据无效');
                    }
                    else {
                        alert('发生了未知错误');
                    }
                    modal.style.display = "none";
                }
            });
        }
    }
}

// 获取指定名称的cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // 判断cookie是否以指定的name开头
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


