/*jQuery(document).ready(function () {
    jQuery(".login100-form").submit(() => {

        var guard = 0;
        var gateAttendant = parseFloat(jQuery("input[name='OutOthGat']").val() || 0);
        var generalServiceSecurity = parseFloat(jQuery("input[name='OutOthGene']").val() || 0);

        var guard = gateAttendant + generalServiceSecurity;
        var guardTotal = parseFloat(jQuery("input[id='guardTotal']").val() || 0);
        var guardEvaluation = guardTotal === guard;

        if (!guardEvaluation) {
            alert("Values for guard does not match.\n Actual value: " + guard + "\nExpected value: " + guardTotal);
            return false;
        }

        return true;
    })
});*/