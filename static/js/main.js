function changeColor() {
    let color = document.querySelector('select[name="color-scheme"]').value;
    let elem = document.querySelector('html');
    elem.dataset.colorScheme = color;
}