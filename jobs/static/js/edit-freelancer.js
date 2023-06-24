var modal1 = document.getElementById("freelancer-photo-modal");

var add_btn = document.getElementById("circle-edit-btn");

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

function PreviewImage() {
    var oFReader = new FileReader();
    oFReader.readAsDataURL(document.getElementById("id_logo").files[0]);

    oFReader.onload = function (oFREvent) {
        document.getElementById("company-logo-edit").src = oFREvent.target.result;
    };
};



$(document).ready(function () {
  $('#add-education').click(function () {
      var formCount = parseInt($('#id_education-TOTAL_FORMS').val());
      var formTmpl = $('#education-formset').find('.editprofile-education-grid:last').clone(true).get(0);
      $(formTmpl).find(':input').each(function () {
          var id = $(this).attr('id').replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
          $(this).attr({ 'name': id, 'id': id }).val('');
      });
      $(formTmpl).find('label').each(function () {
          var newFor = $(this).attr('for').replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
          $(this).attr('for', newFor);
      });
      $(formTmpl).find('#id_education-' + (formCount - 1) + '-DELETE').attr('id', 'id_education-' + formCount + '-DELETE');
      $(formTmpl).insertAfter('#education-formset .editprofile-education-grid:last');
      $('#id_education-TOTAL_FORMS').val(formCount + 1);
  });
});

$(document).ready(function () {
  $('#add-experience').click(function () {
      var formCount = parseInt($('#experience-TOTAL_FORMS').val());
      var formTmpl = $('#experience-formset').find('.editprofile-experience-grid:last').clone(true).get(0);
      $(formTmpl).find(':input').each(function () {
          var id = $(this).attr('id').replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
          $(this).attr({ 'name': id, 'id': id }).val('');
      });
      $(formTmpl).find('label').each(function () {
          var newFor = $(this).attr('for').replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
          $(this).attr('for', newFor);
      });
      $(formTmpl).find('#experience-' + (formCount - 1) + '-DELETE').attr('id', 'experience-' + formCount + '-DELETE');
      $(formTmpl).insertAfter('#experience-formset .editprofile-experience-grid:last');
      $('#id_experience-TOTAL_FORMS').val(formCount + 1);
  });
});

$(document).ready(function () {
  $('#add-skill').click(function () {
      var formCount = parseInt($('#skill-TOTAL_FORMS').val());
      var formTmpl = $('#skill-formset').find('.editprofile-skill-grid:last').clone(true).get(0);
      $(formTmpl).find(':input').each(function () {
          var id = $(this).attr('id').replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
          $(this).attr({ 'name': id, 'id': id }).val('');
      });
      $(formTmpl).find('label').each(function () {
          var newFor = $(this).attr('for').replace('-' + (formCount - 1) + '-', '-' + formCount + '-');
          $(this).attr('for', newFor);
      });
      $(formTmpl).find('#skill-' + (formCount - 1) + '-DELETE').attr('id', 'skill-' + formCount + '-DELETE');
      $(formTmpl).insertAfter('#skill-formset .editprofile-skill-grid:last');
      $('#id_skill-TOTAL_FORMS').val(formCount + 1);
  });
});