const sumInputsByClass = (inputlassName) => {
    const inputFields = document.getElementsByClassName(inputlassName);
    const inputArray = Array.from(inputFields);
    const sum = inputArray.reduce((acc, inputField) => {
        return parseFloat(inputField.value !== '' ? inputField.value : 0) + parseFloat(acc)
    }, 0);

    return sum;
}

jQuery(document).ready(() => {
    jQuery(".excfirstBlock").change(() => {
        const sumFirstBlock = sumInputsByClass("excfirstBlock").toFixed(1);   
        jQuery("#totblock1 > label").html(sumFirstBlock);
        jQuery("#firstBlockTotal").val(sumFirstBlock);
    });
    
    jQuery(".excsecondBlock").change(() => {
        const sumSecondBlock = sumInputsByClass("excsecondBlock").toFixed(1);                
        jQuery("#totblock2 > label").html(sumSecondBlock);
        jQuery("#secondBlockTotal").val(sumSecondBlock);     
    });

    jQuery(".sumAppenOne").change(() => {
        const sumAppendBlock = sumInputsByClass("sumAppenOne").toFixed(1);                
        jQuery("#sumAppend > label").html(sumAppendBlock); 
        jQuery("#totalOI").val(sumAppendBlock);    
    });

    jQuery(".sumOut").change(() => {
        const sumOutBlock = sumInputsByClass("sumOut").toFixed(1);                
        jQuery("#sumOut > label").html(sumOutBlock);
        jQuery("#totalOut").val(sumOutBlock);     
    });

    jQuery(".sumOth").change(() => {
        const sumOthBlock = sumInputsByClass("sumOth").toFixed(1);                
        jQuery("#sumOth > label").html(sumOthBlock);     
    });

    jQuery(".excfirstBlock").first().trigger("change");
    jQuery(".excsecondBlock").first().trigger("change");
    jQuery(".sumAppenOne").first().trigger("change");
    jQuery(".sumOut").first().trigger("change");
    jQuery(".sumOth").first().trigger("change");

    //jQuery( document ).tooltip();
    //$('[data-toggle="tooltip"]').tooltip(); 
    jQuery('[data-toggle="tooltip"]').tooltip(); 


    jQuery("#formPlant input.input100, #formPlant select.shifdropdown").on("keydown", function(e){
        if(e.keyCode == 13){
            e.preventDefault();
            return false; 
        }
    })

    jQuery("#formExcep input.input100").on("keydown", function(e){
        if(e.keyCode == 13){
            e.preventDefault();
            return false; 
        }
    })

    jQuery("#formAppend input.input100").on("keydown", function(e){
        if(e.keyCode == 13){
            e.preventDefault();
            return false; 
        }
    })

    //$('#example').tooltip('show')
});

//$(document).ready(function(){
  //  $('#example').tooltip('show')
    //$('.header').height($(window).height());
//})


//function message() {
//    document.getElementById("advise").style.color = "red";
//    document.getElementById("advise").tooltip();
    //$('[data-toggle="tooltip"]').tooltip(); 
 // }