$('.portfolio-item').click(function() {
    // Find the corresponding portfolio-item-modal
    var modal = $(this).next('.portfolio-item-modal');
    // Toggle the display of the portfolio-item-modal
    modal.toggle();
  });