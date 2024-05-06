document.addEventListener("DOMContentLoaded", function() {
    var messageArea = document.getElementById("messageArea");
    var messageFormeight = document.getElementById("messageFormeight");

    messageArea.addEventListener("submit", function(event) {
        event.preventDefault();

        var date = new Date();
        var hour = date.getHours();
        var minute = date.getMinutes();
        var str_time = hour + ":" + minute;
        var rawText = document.getElementById("text").value;

        var userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="https://i.ibb.co/d5b84Xw/Untitled-design.png" class="rounded-circle user_img_msg"></div></div>';

        document.getElementById("text").value = "";
        messageFormeight.insertAdjacentHTML('beforeend', userHtml);

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="https://i.ibb.co/fSNP7Rz/icons8-chatgpt-512.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + xhr.responseText + '<span class="msg_time">' + str_time + '</span></div></div>';
                    messageFormeight.insertAdjacentHTML('beforeend', botHtml);
                } else {
                    console.error('Error:', xhr.status);
                }
            }
        };
        xhr.open("POST", "/get", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("msg=" + encodeURIComponent(rawText));
    });
});