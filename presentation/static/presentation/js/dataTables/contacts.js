$(document).ready( 
    function () {
	$('#users').DataTable( {
	    "searching": true,
	    "bLengthChange": false,
	    "bInfo": false,
	    "bPaginate": false,
	    "language": { search: '',
			  searchPlaceholder: 'Rechercher contact'
			}
	});
    });
