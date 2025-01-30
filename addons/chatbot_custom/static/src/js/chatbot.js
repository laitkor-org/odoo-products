const fixedReply = `
Support: Thank you for your message! Kindly connect with us on WhatsApp by clicking the link below:<br>
<a href="https://wa.me/9209831369?text=Hi" target="_blank">https://wa.me/9209831369</a><br>
Or scan the QR code below:<br>
<img src="/chatbot_custom/static/images/QR.png" alt="QR Code">
`;

$(document).ready(function () {
    const $chatPopup = $("#chatPopup");
    const $chatIcon = $("#chatIcon");
    $chatIcon.css("display", "flex");

    if (!localStorage.getItem("chatOpened")) {
        setTimeout(function () {
            $chatPopup.css("display", "block");
            $chatIcon.css("display", "none");
            localStorage.setItem("chatOpened", "true");
        }, 3000);
    }

    function toggleChat(open) {
        if (open) {
            $chatPopup.css("display", "block");
            $chatIcon.css("display", "none");
        } else {
            $chatPopup.css("display", "none");
            $chatIcon.css("display", "flex");
        }
    }

    function sendMessage() {
        const $input = $("#chatInput");
        const $chatMessages = $("#chatMessages");

        if ($input.val().trim() !== "") {
            const $userMessage = $("<div>")
                .addClass("user-reply")
                .text($input.val());
            $chatMessages.prepend($userMessage);

            const $botReply = $("<div>")
                .addClass("bot-reply")
                .html(fixedReply);
            $chatMessages.prepend($botReply);
            $input.val("");
            $chatMessages.scrollTop($chatMessages[0].scrollHeight);
        }
    }

    $("#sendButton").on("click", sendMessage);
    $("#chatInput").on("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });

    $("#closeChat").on("click", function () {
        toggleChat(false);
    });

    $("#chatIcon").on("click", function () {
        toggleChat(true);
    });
});