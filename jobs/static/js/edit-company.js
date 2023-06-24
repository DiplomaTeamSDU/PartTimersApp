// var modal = document.getElementById("company-photo-modal-1");

// var add_btn = document.getElementById("circle-edit-btn");

// add_btn.onclick = function(){
//   modal.style.display = "block";
// }

// var span = document.getElementsByClassName("close")[0];

// span.onclick = function() { 
//   modal.style.display = "none";
// }

function PreviewImage() {
    var oFReader = new FileReader();
    oFReader.readAsDataURL(document.getElementById("id_logo").files[0]);

    oFReader.onload = function (oFREvent) {
        document.getElementById("company-logo-edit").src = oFREvent.target.result;
    };
};
