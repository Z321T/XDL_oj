
// JavaScript文件中的AJAX请求函数
function performLogin() {
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    if (username.trim() === "") {
        // 账号为空，显示账号为空的模态框
        $('#emptyusernameModal').modal('show');
        return; // 不执行后续的AJAX请求
    }
    else if (password.trim() === "") {
        $('#emptyPasswordModal').modal('show');
        return; // 不执行后续的AJAX请求
    }
    else {
        $.ajax({
            url: 'login/',  // 后端处理登录的API端点
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({username: username, password: password}),
            success: function (response) {
                // 处理后端响应
                if (response.status === 'success') 
                {
                    alert('登录成功');
                    // 成功登录后,重定向到下一个页面
                    if(response.message.includes('student'))
                    window.location.href = 'student/home/';
                    else if(response.message.includes('teacher'))
                    window.location.href='teacher/home/';
                    else if(response.message.includes('administrator'))
                    window.location.href='administrator/home/';

                }

                else {
                    alert(response.message);
                    // 检查特定的错误条件
                    if (response.message.includes('Username is incorrect')) {
                        // 显示学号错误模态框
                        $('#usernameErrorModal').modal('show');
                    }
                    else if (response.message.includes('Password is incorrect')) {
                        // 显示密码错误模态框
                        $('#passwordErrorModal').modal('show');
                    }
                }
            },
            error: function (error) {
                console.error(error);
            }
        });
    }
}