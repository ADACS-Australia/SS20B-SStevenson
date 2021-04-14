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
        $('#id_velocity_random_number_1').prop("disabled", !(checked) );
        $('#id_velocity_random_number_2').prop("disabled", !(checked) );
        $('#id_velocity_1').prop("disabled", !(checked) );
        $('#id_velocity_2').prop("disabled", !(checked) );
        $('#id_theta_1').prop("disabled", !(checked) );
        $('#id_theta_2').prop("disabled", !(checked) );
        $('#id_phi_1').prop("disabled", !(checked) );
        $('#id_phi_2').prop("disabled", !(checked) );
        $('#id_mean_anomaly_1').prop("disabled", !(checked) );
        $('#id_mean_anomaly_2').prop("disabled", !(checked) );
    }

    function common_envelope_enabled_onchange(){
        let checked = $('#id_common_envelope_enabled').is(":checked");

        $('#id_common_envelope_alpha').prop("disabled", !(checked) );
        $('#id_common_envelope_lambda_prescription').prop("disabled", !(checked) );
        $('#id_common_envelope_lambda').prop("disabled", !(checked) );
    }

    function supernova_enabled_onchange(){
        let checked = $('#id_supernova_enabled').is(":checked");

        $('#id_remnant_mass_prescription').prop("disabled", !(checked) );
        $('#id_fryer_supernova_engine').prop("disabled", !(checked) );
        $('#id_black_hole_kicks').prop("disabled", !(checked) );
        $('#id_Kick_velocity_distribution').prop("disabled", !(checked) );
        $('#id_kick_velocity_sigma_CCSN_NS').prop("disabled", !(checked) );
        $('#id_kick_velocity_sigma_CCSN_BH').prop("disabled", !(checked) );
        $('#id_kick_velocity_sigma_ECSN').prop("disabled", !(checked) );
        $('#id_kick_velocity_sigma_USSN').prop("disabled", !(checked) );
        $('#id_pair_instability_supernovae').prop("disabled", !(checked) );
        $('#id_pisn_lower_limit').prop("disabled", !(checked) );
        $('#id_pisn_upper_limit').prop("disabled", !(checked) );
        $('#id_pulsational_pair_instability_supernovae').prop("disabled", !(checked) );
        $('#id_ppi_lower_limit').prop("disabled", !(checked) );
        $('#id_ppi_upper_limit').prop("disabled", !(checked) );
        $('#id_pulsational_pair_instability_prescription').prop("disabled", !(checked) );
        $('#id_maximum_neutron_star_mass').prop("disabled", !(checked) );

    }

    function mass_transfer_enabled_onchange(){
        let checked = $('#id_mass_transfer_enabled').is(":checked");

        $('#id_mass_transfer_angular_momentum_loss_prescription').prop("disabled", !(checked) );
        $('#id_mass_transfer_accertion_efficiency_prescription').prop("disabled", !(checked) );
        $('#id_mass_transfer_fa').attr( "disabled", !(checked) );
        $('#id_mass_transfer_jloss').attr( "disabled", !(checked) );
    }
});
