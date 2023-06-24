$(document).ready(function() {
    $("[id^='submit-modal-']").each(function() {
      var modalId = $(this).attr("id");
      var buttonId = modalId.replace("submit-modal-", "submit-btn-");
  
      var modal = $("#" + modalId);
      var addProjectBtn = $("#" + buttonId);
  
      addProjectBtn.click(function() {
        modal.css("display", "block");
      });
  
      var span = modal.find(".close").eq(0);
  
      span.click(function() {
        modal.css("display", "none");
      });
    });
});

// $(document).ready(function() {
//   $("[id^='view-submit-modal-']").each(function() {
//     var modalId = $(this).attr("id");
//     var buttonId = modalId.replace("view-submit-modal-", "view-submit-btn-");

//     var modal = $("#" + modalId);
//     var addProjectBtn = $("#" + buttonId);

//     addProjectBtn.click(function() {
//       modal.css("display", "block");
//     });

//     var span = modal.find(".close").eq(0);

//     span.click(function() {
//       modal.css("display", "none");
//     });
//   });
// });

$(document).ready(function() {
  // Show applications section by default
  $('#ongoing-id').show();
  $('#finished-id').hide();
  $('#ongoing-button').addClass('active');

  // Handle button clicks
  $('#ongoing-button').click(function() {
      $(this).addClass('active');
      $('#finished-button').removeClass('active');
      $('#ongoing-id').show();
      $('#finished-id').hide();
  });

  $('#finished-button').click(function() {
      $(this).addClass('active');
      $('#ongoing-button').removeClass('active');
      $('#ongoing-id').hide();
      $('#finished-id').show();
  });
});