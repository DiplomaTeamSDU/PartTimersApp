$('.input-file input[type=file]').on('change', function(){
	let file = this.files[0];
	$(this).closest('.input-file').find('.input-file-text').html(file.name);
});

function removeFiles(target){
	let name = $(target).prev().text();
	let input = $(target).closest('.input-file-row').find('input[type=file]');	
	$(target).closest('.input-file-list-item').remove();	
	for(let i = 0; i < dt.items.length; i++){
		if(name === dt.items[i].getAsFile().name){
			dt.items.remove(i);
		}
	}
	input[0].files = dt.files;  
}


$(document).ready(function() { 
	$('select[multiple]').mousedown(function(e) { 
	e.preventDefault(); 
	
	var select = this; 
	var scroll = select.scrollTop; 
	
	e.target.selected = !e.target.selected; 
	
	setTimeout(function() { 
		select.scrollTop = scroll; 
	}, 0); 
	
	$(select).focus(); 
	}).mousemove(function(e) { 
	e.preventDefault(); 
	}); 
}); 
