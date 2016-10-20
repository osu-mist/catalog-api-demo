function row_display(items, display) {
	if (display == "hide") {
		for (i=0; i<items.length; i++) {
			$(items[i]).parent().parent().hide();
		}
	} else if (display == "show") {
		for (i=0; i<items.length; i++) {
			$(items[i]).parent().parent().show();
		}
	}
}


$(document).ready(function(){
	var totle_count = $(".result:visible").length;
	console.log(totle_count);
	$("#totle_count").text(totle_count);

	if ($("#id_is_open").is(":checked")) {
		row_display(["#id_is_all", "#id_year", "#id_term", "#id_page_size", "#id_page_num"], "hide");
	} else if ($("#id_is_all").is(":checked")) {
		row_display(["#id_is_open", "#id_year", "#id_term", "#id_page_size", "#id_page_num"], "hide");
	}		

	$("input").click(function(){
		if ($("#id_is_all").is(":checked")) {
			row_display(["#id_is_open", "#id_year", "#id_term", "#id_page_size", "#id_page_num"], "hide");
		}
		else if ($("#id_is_open").is(":checked")) {
			row_display(["#id_is_all", "#id_year", "#id_term", "#id_page_size", "#id_page_num"], "hide");
		} else {
			row_display(["#id_is_all", "#id_is_open", "#id_year", "#id_term", "#id_page_size", "#id_page_num"], "show");
		}
	});

	// results filter
	$("#filter_box").keyup(function(){
		var value = $(this).val().toLowerCase();
		$("#results table").each(function(index, element){
			$(element).children("tbody").children("tr").children("td").each(function(idx, ele){
				if ($(ele).text().toLowerCase().indexOf(value) == -1){
					$(ele).closest("table").hide();
				} else {
					$(ele).closest("table").show();
					return false;
				}
			});
		});
		var totle_count = $(".result:visible").length;
		$("#totle_count").text(totle_count);
	});
});