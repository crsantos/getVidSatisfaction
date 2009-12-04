function playlist_edit() {
	var item = $(this).parent();
	var url = item.find(".title").attr("href");
	item.load("/save/?ajax&url=" + escape(url), null, function () {
		$("#save-form").submit(playlist_save);
	});
	return false;
}

function playlist_save() {
	var item = $(this).parent();
	var data = {
		url: item.find("#id_url").val(),
		nome: item.find("#id_nome").val(),
		descricao: item.find("#id_descricao").val(),
		categoria: item.find("#id_categoria").val(),
		image: item.find("#id_image").val(),
		tags: item.find("#id_tags").val(),
		share: item.find("#id_share").val(),
		
	};
	
	$.post("/save/?ajax", data, function (result) {
		if (result != "failure"){
			item.before($("li", result).get(0));
			item.remove();
			$("ul.playlists .edit").click(playlist_edit);
		} 
		else
		{
			alert("Failed to validate playlist before saving.");
		}
	}); 
	return false; 
}

$(document).ready(function () {
	$("ul.playlists .edit").click(playlist_edit);
});
