/*
 * Table Filter - jQuery Plugin
 * Very simple jQuery table filter plugin
 *
 * Documentation at: https://github.com/vmichnowicz/jquery.tablefilter
 * Examples at: http://www.vmichnowicz.com/examples/tablefilter/index.html
 *
 * Copyright (c) 2011 Victor Michnowicz
 *
 * Version: 1.0 (2011/9/27)
 * Requires: jQuery
 *
 * Dual licensed under the MIT and GPL licenses:
 *   http://www.opensource.org/licenses/mit-license.php
 *   http://www.gnu.org/licenses/gpl.html
 */
(function($) {
    $.fn.tableFilter = function(options) {

        // Loop through each selected element
        return this.each(function() {
            // Find all table rows inside the table body
            var rows = $(this).find('tbody tr'),
                index, rowsLength;

            // Run the table filter
            function filter() {
                // Loop through each table row
                for (index = 0, rowsLength = rows.size(); index < rowsLength; index += 1) {
                    var row = $(rows.get(index)),
                        filters_count_matched = 0, // Count of matched filters within each table row
                        filters_count = 0; // Count of all filters
                    row.hide(); // Hide this current row

                    // Loop through each filter
                    $.each(options.filters, function(key, element) {
                        var text = row.find('.' + key)[0].textContent, // Text from the table we want to match against
                            value = element.val(),
                            filiation = text.split(" - "); // User inputed filter text
                        filters_count++;

                        // If the user inputed text is found in this table cell
                        if (value === filiation[0] || value === filiation[1] || (value.indexOf("Todos") === 0)) {
                            filters_count_matched++; // Add +1 to our matched filters counter
                        }
                    });

                    // If the number of filter matches is equal to the number of filters, show the row
                    if (filters_count_matched == filters_count) {
                        row.show();
                    }
                // });
                }
            }

            // Loop through each filter input
            
            $.each(options.filters, function(index, element) {
                // Attach event handeler to each input
                $(element).live('change', function() {
                    filter();
                });
            });

        });
    }
})(jQuery);