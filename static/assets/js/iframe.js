$("#quiz-container").fadeOut();

var counter = 1;

$(function(){
    if(typeof ajax_url !== 'undefined') {
    $.get( ajax_url+"setup/setup", function( data ) {
        if(!data.end) {
        $("#qtext").text(data.nv_question);
        $("#qid").text(counter);
        $("#fact").val(data.fact);

        }
    });
    }
    var loading = $('#loadbar').hide();



    $("label.btn").on('click',function (e) {
e.preventDefault()
    counter++;

    	var choice = $(this).find('input:radio').val();
    	$('#loadbar').show();
    	$('#quiz').fadeOut();
    	console.log(typeof choice);
    	var rep = choice === '1'?'yes':'no';
    	//alert(choice);
    	$.get( ajax_url+$("#fact").val()+"/"+rep, function( data ) {
        if(!data.end) {
        $("#qtext").text(data.nv_question);
        $("#qid").text(counter);
        $("#fact").val(data.fact);
        $('#loadbar').fadeOut();
    	$('#quiz').fadeIn();
        }else{
        //counter =1;
        //$("#quiz").fadeIn();
        $('#loadbar').fadeOut();
        $('.modal-dialog').fadeOut();
        $('body').append('<div class="alert alert-success" role="alert">'+data.result+'</div>');
        //alert(data.result);
        }


   });

});

});

$("#quiz-container").fadeOut();



