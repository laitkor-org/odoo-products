$(document).ready(function() {
    function updateIframeChatHeaderCSS() {
        var iframe = document.getElementById('myiframe');
        $(iframe).on('load', function() {
            try {
                var iframeWindow = iframe.contentWindow;
                var iframeDocument = iframeWindow.document;
                $(iframeDocument).find('.chat-header').css({
                    'background': 'linear-gradient(135deg, #4a90e2, #2c3e50)',
                    'color': 'white',
                    'border-radius': '8px 8px 0 0'
                });
                console.log('Chat header CSS updated successfully');
            } catch (error) {
                console.error('Cannot access iframe content due to same-origin policy:', error);
            }
        });
    }
    updateIframeChatHeaderCSS();
});