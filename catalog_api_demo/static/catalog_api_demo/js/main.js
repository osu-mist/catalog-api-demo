$(document).ready(function(){
	// hide unnecessary parameters
	if ($("#id_is_open").is(":checked")) {
		$("#id_year").parent().parent().hide();
		$("#id_term").parent().parent().hide();
		$("#id_page_size").parent().parent().hide();
		$("#id_page_num").parent().parent().hide();
	}	

	$("#id_is_open").click(function(){
		if ($("#id_is_open").is(":checked")) {
			$("#id_year").parent().parent().hide();
			$("#id_term").parent().parent().hide();
			$("#id_page_size").parent().parent().hide();
			$("#id_page_num").parent().parent().hide();
		} else {
			$("#id_year").parent().parent().show();
			$("#id_term").parent().parent().show();
			$("#id_page_size").parent().parent().show();
			$("#id_page_num").parent().parent().show();
		}
	});

	$("#id_term").click(function(){
		if ($("#id_term_4").is(":checked")) {
			$("#id_year").parent().parent().hide();
		} else {
			$("#id_year").parent().parent().show();
		}
	});

	// result filter
	$("#filter_box").keyup(function(){
		var value = $(this).val().toLowerCase();
		$("#results").each(function(){

		});
	});
});