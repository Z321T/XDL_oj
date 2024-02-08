$(document).ready(function() {
    // 获取学生信息并显示
    $.get('/student_info/', function(data) {
        $('#name').val(data.name);
        $('#student_id').val(data.student_id);
        $('#class').val(data.class_num);
        $('#email').val(data.email);
    });

    // 修改按钮点击事件
    $('.button').click(function() {
        if ($(this).text() === '修改') {
            $('input').prop('disabled', false);
            $(this).text('保存');
        } else {
            // 保存按钮点击事件
            var name = $('#name').val();
            var student_id = $('#student_id').val();
            var class_num = $('#class').val();
            var email = $('#email').val();
            $.ajax({
                url: '/student_info/',
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({name: name, student_id: student_id, class: class_num, email: email}),
                success: function(data) {
                    if (data.status === 'success') {
                        alert('保存成功！');
                        $('input').prop('disabled', true);
                        $('.button').text('修改');
                    }
                }
            });
        }
    });
});