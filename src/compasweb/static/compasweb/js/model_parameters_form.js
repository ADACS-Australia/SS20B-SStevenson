let ready = $(document).ready(function() {
    
    $('#advanced_settings').addClass('d-none');

    $('#show_advanced').on('click', function() {
        if($('#advanced_settings').hasClass('d-none') === true){
            $('#advanced_settings').removeClass('d-none');
        }
        else{
            $('#advanced_settings').addClass('d-none');
        }
    });

    lambda_prescription_onChange();
    remnant_mass_prescription_onChange();
    accertion_efficiency_prescription_onChange();
    angular_momentum_loss_prescription_onChange();
    kick_enabled_onchange();
    common_envelope_enabled_onchange();
    supernova_enabled_onchange();
    mass_transfer_enabled_onchange();


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

    $('#id_kick_enabled').change(function() { 
        kick_enabled_onchange();      
    });

    $('#id_common_envelope_enabled').change(function() { 
        common_envelope_enabled_onchange();      
    });

    $('#id_supernova_enabled').change(function() { 
        supernova_enabled_onchange();      
    });

    $('#id_mass_transfer_enabled').change(function() { 
        mass_transfer_enabled_onchange();      
    });

    $('#supernova_explanation_link').click(function() { 
        show_supernova_explanation();      
    });

    $('#common_envelope_explanation_link').click(function() { 
        show_common_envelope_explanation();      
    });

    $('#kick_explanation_link').click(function() { 
        show_kick_explanation();      
    });
    $('#mass_transfer_explanation_link').click(function() { 
        show_mass_transfer_explanation();      
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

    function kick_enabled_onchange(){
        let checked = $('#id_kick_enabled').is(":checked");
        
        if(checked){
            $('#kick_settings').removeClass('d-none');
        }
        else{
            $('#kick_settings').addClass('d-none');
        }
    }

    function show_kick_explanation(){
        
        if($('#kick_explanation').hasClass('d-none') === true){
            $('#kick_explanation').removeClass('d-none');
        }
        else{
            $('#kick_explanation').addClass('d-none');
        }
    }

    function common_envelope_enabled_onchange(){
        let checked = $('#id_common_envelope_enabled').is(":checked");

        if(checked){
            $('#common_envelope_settings').removeClass('d-none');
        }
        else{
            $('#common_envelope_settings').addClass('d-none');
        }
    }

    function show_common_envelope_explanation(){
        
        if($('#common_envelope_explanation').hasClass('d-none') === true){
            $('#common_envelope_explanation').removeClass('d-none');
        }
        else{
            $('#common_envelope_explanation').addClass('d-none');
        }
    }

    function supernova_enabled_onchange(){
        let checked = $('#id_supernova_enabled').is(":checked");
        if(checked){
            $('#supernova_settings').removeClass('d-none');
        }
        else{
            $('#supernova_settings').addClass('d-none');
        }
    }
    function show_supernova_explanation(){
        
        if($('#supernova_explanation').hasClass('d-none') === true){
            $('#supernova_explanation').removeClass('d-none');
        }
        else{
            $('#supernova_explanation').addClass('d-none');
        }
    }

    function mass_transfer_enabled_onchange(){
        let checked = $('#id_mass_transfer_enabled').is(":checked");
        if(checked){
            $('#mass_transfer_settings').removeClass('d-none');
        }
        else{
            $('#mass_transfer_settings').addClass('d-none');
        }
        
    }

    function show_mass_transfer_explanation(){
        
        if($('#mass_transfer_explanation').hasClass('d-none') === true){
            $('#mass_transfer_explanation').removeClass('d-none');
        }
        else{
            $('#mass_transfer_explanation').addClass('d-none');
        }
    }

});
