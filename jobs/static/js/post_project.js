var modal = document.getElementById("project-modal-id");

// Get the image and insert it inside the modal - use its "alt" text as a caption
var add_project_btn = document.getElementById("add-project-btn");
// var modalImg = document.getElementById("img01");
// var captionText = document.getElementById("caption");
add_project_btn.onclick = function(){
  modal.style.display = "block";
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() { 
  modal.style.display = "none";
}
