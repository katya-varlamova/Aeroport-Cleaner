// base

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("info-icon")) {
        if (document.getElementById('info-text').style.display == 'none') {
            setTimeout(function () { $("#info-text").fadeIn() }, 200);
        }
        else
            setTimeout(function () { $("#info-text").fadeOut() }, 200);
    }
});


setTimeout(function () { $(".my-alert").fadeIn() }, 200)
setTimeout(function () { $(".my-alert").fadeOut() }, 3000)
document.querySelector('.flashes-ul').onclick = function (e) {
    const btn = e.target.closest('.alert-delete');
    if (btn) {
        btn.closest('li').remove();
    }

}



// index


const dropArea = document.querySelector('.drag-area');
let file;
let allowed_upl = false;

document.querySelector('.input_file').addEventListener("change", function () {
    file = this.files[0];
    dropArea.classList.add("dropArea-active");
    sendFile();
});

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    // console.log('file is over in DragArea');
    dropArea.classList.add("dropArea-active");
    document.getElementsByClassName('input_file-button-text')[0].innerHTML = "Отпустите файл здесь";
});

dropArea.addEventListener("dragleave", () => {
    // console.log('file is leave in DragArea');
    dropArea.classList.remove("dropArea-active");
    document.getElementsByClassName('input_file-button-text')[0].innerHTML = "Перетяните файл<br>или<br>Выберете из списка";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    // console.log('file is dropped in DragArea');
    // dropArea.classList.remove("dropArea-active");
    file = e.dataTransfer.files[0];
    // console.log(file);
    sendFile();
});

$("#video_form").on('submit', function (e) {
    if (!allowed_upl) // ничего не произойдет
        alert('Выберете корректный файл');
    return allowed_upl;
});

function sendFile() {

    let filetype = file.type;
    let validExtensions = ["video/mp4", "video/MOV", "video/avi"];
    if (validExtensions.includes(filetype)) {
        allowed_upl = true;
        let fileReader = new FileReader(); //creating new FileReader object
        fileReader.onload = function (event) {
            var dt = new DataTransfer();
            dt.items.add(file);
            var file_list = dt.files;

            console.log('Коллекция файлов создана:');
            // console.dir(file_list);

            document.querySelector('input[type="file"]').files = file_list;
        }
        fileReader.readAsDataURL(file);


        if (String(file.name).length > 20)
            document.getElementsByClassName('input_file-button-text')[0].innerHTML = String(file.name).substr(0, 17) + "...";
        else document.getElementsByClassName('input_file-button-text')[0].innerHTML = file.name;
    }
    else {
        allowed_upl = false;
        console.log("Invalid file ext");
        dropArea.classList.remove("dropArea-active");
        document.getElementsByClassName('input_file-button-text')[0].innerHTML = "Перетяните файл<br>или<br>Выберете из списка";
        alert('Недопустимый формат файла');
    }
}
document.addEventListener("click", function (e) {
    if (e.target.className == "use_stream_link") {
        document.getElementById('use_file').style.display = 'none';
        document.getElementById('use_stream').style.display = 'block';
    }
});
document.addEventListener("click", function (e) {
    if (e.target.className == "use_file_link") {

        document.getElementById('use_file').style.display = 'block';
        document.getElementById('use_stream').style.display = 'none';
    }
});

document.getElementById('video_form')[0].onchange = function () {
    if (this.files[0])
        if (String(this.files[0].name).length > 20)
            document.getElementsByClassName('input_file-button-text')[0].innerHTML = String(this.files[0].name).substr(0, 17) + "...";
        else document.getElementsByClassName('input_file-button-text')[0].innerHTML = this.files[0].name;
};


