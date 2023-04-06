var modal = document.getElementById("company-photo-modal");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var img = document.getElementById("company-logo");
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");
img.onclick = function(){
  modal.style.display = "block";
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}

function PreviewImage() {
    var oFReader = new FileReader();
    oFReader.readAsDataURL(document.getElementById("id_logo").files[0]);

    oFReader.onload = function (oFREvent) {
        document.getElementById("company-logo-edit").src = oFREvent.target.result;
    };
};