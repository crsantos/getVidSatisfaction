$(document).ready(function () { 
	$("#id_query").autocomplete('/ajax/playlist/autocomplete/', { multiple: true, multipleSeparator: ''} ); 
});