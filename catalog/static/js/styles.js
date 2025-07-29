document.querySelectorAll('.enlargeable-image').forEach(function (img) {
    img.addEventListener('click', function () {
        const modal = document.getElementById('image-modal');
        const modalImg = document.getElementById('modal-img');
        modalImg.src = img.src;
        modal.style.display = 'flex';
    });
});

document.getElementById('image-modal').addEventListener('click', function (e) {
    if (e.target === this) {
        this.style.display = 'none';
    }
});
