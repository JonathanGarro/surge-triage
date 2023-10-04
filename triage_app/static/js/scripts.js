window.setTimeout(function() {
    $("#alert").fadeTo(500, 0) 
}, 6000);

// $(document).ready(function () {
//     $('#alert-table').DataTable({
//         order: [[5, 'desc']],
//         dom: 'frtipB',
//         buttons: [
//             'copy', 'csv'
//         ],
//         columnDefs: [{
//             target: 6,
//             visible: false,
//             searchable: true,
//         },
//         {
//             target: 7, 
//             visible: false,
//             searchable: true
//         }],
//     });
// });

$(document).ready(function () {
    $('#alert-table').DataTable({
        order: [[0, 'desc']], // Sort by column index 5 (reverse chronological order)
        dom: 'frtipB',
        buttons: [
            'copy', 'csv'
        ],
        columnDefs: [
            {
                targets: [0], // Target the first column (column index 0)
                visible: false, // Hide the first column
                searchable: false, // Make it not searchable
            },
        ],
    });
});
