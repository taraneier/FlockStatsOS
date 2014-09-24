/**
 * Created by tneier on 9/23/14.
 */

django.jQuery(document).ready(function() {

    dateVal = window.location.search.replace('?', '')
    if (dateVal.length < 10) {
        dateVal = new Date().toLocaleDateString();
    }


    django.jQuery('#id_start_0').val(dateVal);
    django.jQuery('#id_finish_0').val(dateVal);
});
