let ready = $(document).ready(function() {
    
    $('#advanced_settings').addClass('d-none');

    $('#show_advanced').on('click', function() {
        if($('#advanced_settings').hasClass('d-none') === true){
            $('#advanced_settings').removeClass('d-none')
        }
        else{
            $('#advanced_settings').addClass('d-none')
        }
    });

    lambda_prescription_onChange();
    remnant_mass_prescription_onChange();
    accertion_efficiency_prescription_onChange();
    angular_momentum_loss_prescription_onChange();

    $('#id_common_envelope_lambda_prescription').on('change', function() {
        lambda_prescription_onChange();
    });

    $('#id_remnant_mass_prescription').on('change', function() {
        remnant_mass_prescription_onChange();
    });

    $('#id_mass_transfer_accertion_efficiency_prescription').on('change', function() {
        accertion_efficiency_prescription_onChange();
    });

    $('#id_mass_transfer_angular_momentum_loss_prescription').on('change', function() {
        angular_momentum_loss_prescription_onChange();
    });


    function lambda_prescription_onChange(){

        let lambda_prescription = $('#id_common_envelope_lambda_prescription').find(":selected").text();

        if(lambda_prescription === 'LAMBDA_FIXED'){
            $('.div-common_envelope_lambda').removeClass('d-none')
        }
        else{
            $('.div-common_envelope_lambda').addClass('d-none')
        }
    }

    function remnant_mass_prescription_onChange(){

        let mass_prescription = $('#id_remnant_mass_prescription').find(":selected").text();

        if(mass_prescription === 'FRYER2012'){
            $('.div-fryer_supernova_engine').removeClass('d-none')
        }
        else{
            $('.div-fryer_supernova_engine').addClass('d-none')
        }
    }

    function accertion_efficiency_prescription_onChange(){

        let accertion_efficiency_prescription = $('#id_mass_transfer_accertion_efficiency_prescription').find(":selected").text();

        if(accertion_efficiency_prescription === 'FIXED'){
            $('.div-mass_transfer_fa').removeClass('d-none')
        }
        else{
            $('.div-mass_transfer_fa').addClass('d-none')
        }
    }

    function angular_momentum_loss_prescription_onChange(){

        let angular_momentum_loss_prescription = $('#id_mass_transfer_angular_momentum_loss_prescription').find(":selected").text();

        if(angular_momentum_loss_prescription === 'ARBITRARY'){
            $('.div-mass_transfer_jloss').removeClass('d-none')
        }
        else{
            $('.div-mass_transfer_jloss').addClass('d-none')
        }
    }

    
    //set initial state.
    // $('#kick_enabled').val(this.checked);
    
    $('#kick_enabled').change(function() {
        if(this.checked) {
            // alert('enabled')
            // var returnVal = confirm("Are you sure?");
            // $(this).prop("checked", returnVal);
            $('#kick_settings').prop('disabled', false);
        }
        else{
            // alert('disabled')
            // var returnVal = confirm("Are you sure?");
            // $(this).prop("checked", returnVal);
            $('#kick_settings').prop('disabled', true);
        }
        //$('#textbox1').val(this.checked);        
    });
});