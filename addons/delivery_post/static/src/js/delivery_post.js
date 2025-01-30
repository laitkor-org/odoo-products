const currentPath = window.location.pathname;

if (currentPath === '/trackOrderPage') {
document.getElementById('trackForm').onsubmit = function(e) {
    e.preventDefault();
    document.getElementById('headingFetch').style.display = 'block';
    document.getElementById('loader').style.display = 'block';
    document.getElementById('headingTrack').style.display = 'none';
    document.getElementById('trackForm').style.display = 'none';
    var form = document.getElementById('trackForm');
    var formData = new FormData(form);
    fetch('/track', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.redirected) {
          window.location.href = response.url;
        }
        setTimeout(() => {
            document.getElementById('headingTrack').style.display = 'block';
            document.getElementById('trackForm').style.display = 'block';
            document.getElementById('headingFetch').style.display = 'none';
            document.getElementById('loader').style.display = 'none';
        }, 500);
    })
    .catch(error => {
        alert('There was an error tracking the consignment. Please try again.');
        console.error("Error -> ", error)
        document.getElementById('loader').style.display = 'none';
    });
};
window.addEventListener('pageshow', function(event) {
    if (event.persisted) {
        window.location.reload();
    }
});
}

