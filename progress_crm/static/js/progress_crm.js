$(document).ready(function() {
	$(document).on('click', '.dashboard-module .dashboard-module a', function(e) {
		e.preventDefault();
		var module = $(this);
		$.get(
			$(this).attr('href')
		).done(function(data) {
			module.closest(".dashboard-module").find('.content-target').html(data);
		});
	});

	$(document).on('submit', '.dashboard-module .dashboard-module form', function(e) {
		e.preventDefault();
		var module = $(this);
		$.post(
			$(this).attr('action'),
			$(this).serialize()
		).success(function(data) {
			module.closest(".dashboard-module").find('.content-target').html(data);
		});
	});
});