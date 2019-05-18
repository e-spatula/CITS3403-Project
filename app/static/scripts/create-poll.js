function displayError(errorText) {
    $("#errors").empty();
    $("#errors").append("<span class =  'alert-box error banner'> " + errorText + " </span>");

}


function addOption() {
    let $templateForm = $("#options-_");
    if(!$templateForm) {
        console.log("Can't find template");
    }
    let $lastForm = $(".subform").last();
    let newIndex = 0;
    if($lastForm.length > 0) {
        newIndex = parseInt($lastForm.data("index")) + 1;
    }
    if(newIndex > 10) {
        displayError("Can't have more than 10 options");
        return false;
    }
    
    let $newForm = $templateForm.clone();

    $newForm.attr('id', $newForm.attr('id').replace('_', newIndex));
    $newForm.data('index', newIndex);

    $newForm.find('input').each(function(idx) {
        var $item = $(this);

        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
    });

    $('#subforms-container').append($newForm);
    $newForm.addClass('subform');
    $newForm.removeClass('is-hidden');
}

function removeOption() {

}

$(document).ready(function() {
    $(".add").click(addOption)
    $(".remove").click(removeOption);
});

