var modal1 = document.getElementById("freelancer-photo-modal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var add_btn = document.getElementById("circle-edit-btn");
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");
add_btn.onclick = function(){
  modal1.style.display = "block";
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal1.style.display = "none";
}

function PreviewImage1() {
    var oFReader = new FileReader();
    oFReader.readAsDataURL(document.getElementById("id_photo").files[0]);

    oFReader.onload = function (oFREvent) {
        document.getElementById("freelancer-logo-edit").src = oFREvent.target.result;
    };
};