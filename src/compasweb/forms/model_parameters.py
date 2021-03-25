from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ..models import COMPASModelRun
from ..utils.constants import *

INITIAL_PARAMETERS = [
    'mass1',
    'mass2',
    'metallicity',
    'eccentricity',
    'separation',
    'orbital_period',
    'max_time',
]

ADVANCED_SETTINGS = [
    'velocity_random_number_1',
    'velocity_1',
    'theta_1',
    'phi_1',
    'mean_anomaly_1',
    'velocity_random_number_2',
    'velocity_2',
    'theta_2',
    'phi_2',
    'mean_anomaly_2',
    'common_envelope_alpha',
    'common_envelope_lambda_prescription',
    'common_envelope_lambda',
    'remnant_mass_prescription',
    'fryer_supernova_engine',
    'black_hole_kicks',
    'Kick_velocity_distribution',
    'kick_velocity_sigma_CCSN_NS',
    'kick_velocity_sigma_CCSN_BH',
    'kick_velocity_sigma_ECSN',
    'kick_velocity_sigma_USSN',
    'pair_instability_supernovae',
    'pisn_lower_limit',
    'pisn_upper_limit',
    'pulsational_pair_instability_supernovae',
    'ppi_lower_limit',
    'ppi_upper_limit',
    'pulsational_pair_instability_prescription',
    'maximum_neutron_star_mass',
    'mass_transfer_angular_momentum_loss_prescription',
    'mass_transfer_accertion_efficiency_prescription',
    'mass_transfer_fa',
    'mass_transfer_jloss',
]

FIELDS = INITIAL_PARAMETERS + ADVANCED_SETTINGS

# FIELDS = [
#     'mass1',
#     'mass2',
#     'metallicity',
#     'eccentricity',
#     'seperation',
#     'orbital_period',
#     'max_time',

#     'velocity_random_number',
#     'velocity',
#     'theta',
#     'phi',
#     'mean_anomaly',

#     'common_envelope_alpha',
#     'common_envelope_lambda_prescription',
#     'common_envelope_lambda',

#     'remnant_mass_prescription',
#     'fryer_supernova_engine',
#     'black_hole_kicks',
#     'Kick_velocity_distribution',
#     'kick_velocity_sigma_CCSN_NS',
#     'kick_velocity_sigma_CCSN_BH',
#     'kick_velocity_sigma_ECSN',
#     'kick_velocity_sigma_USSN',
#     'pair_instability_supernovae',
#     'pisn_lower_limit',
#     'pisn_upper_limit',
#     'pulsational_pair_instability_supernovae',
#     'ppi_lower_limit',
#     'ppi_upper_limit',
#     'pulsational_pair_instability_prescription',
#     'maximum_neutron_star_mass',

#     'mass_transfer_angular_momentum_loss_prescription',
#     'mass_transfer_accertion_efficiency_prescription',
#     'mass_transfer_fa',
#     'mass_transfer_jloss',
# ]

LABELS = {
    'mass1': _(MASS_1_LABEL),
    'mass2': _(MASS_2_LABEL),
    'metallicity': _(METALICITY_LABEL),
    'eccentricity': _(ECCENTRICITY_LABEL),
    'separation': _(SEPARATION_LABEL),
    'orbital_period': _(ORBITAL_PERIOD_LABEL),
    'max_time': _(MAX_TIME_LABEL),
    'velocity_random_number_1': _(VELOCITY_RANDOM_NUMBER_1_LABEL),
    'velocity_1': _(VELOCITY_1_LABEL),
    'theta_1': _(THETA_1_LABEL),
    'phi_1': _(PHI_1_LABEL),
    'mean_anomaly_1': _(MEAN_ANOMALY_1_LABEL),
    'velocity_random_number_2': _(VELOCITY_RANDOM_NUMBER_2_LABEL),
    'velocity_2': _(VELOCITY_2_LABEL),
    'theta_2': _(THETA_2_LABEL),
    'phi_2': _(PHI_2_LABEL),
    'mean_anomaly_2': _(MEAN_ANOMALY_2_LABEL),
    'common_envelope_alpha': _(COMMON_ENVELOPE_ALPHA_LABEL),
    'common_envelope_lambda_prescription': _(COMMON_ENVELOPE_LAMBDA_PRESCRIPTION),
    'common_envelope_lambda': _(COMMON_ENVELOPE_LAMBDA_LABEL),
    'remnant_mass_prescription': _(REMNANT_MASS_PRESCRIPTION_LABEL),
    'fryer_supernova_engine': _(FRYER_SUPERNOVA_ENGINE_LABEL),
    'black_hole_kicks': _(BLACK_HOLE_KICKS_LABEL),
    'Kick_velocity_distribution': _(KICK_VELOCITY_DISTRIBUTION_LABEL),
    'kick_velocity_sigma_CCSN_NS': _(KICK_VELOCITY_SIGMA_CCSN_NS_LABEL),
    'kick_velocity_sigma_CCSN_BH': _(KICK_VELOCITY_SIGMA_CCSN_BH_LABEL),
    'kick_velocity_sigma_ECSN': (KICK_VELOCITY_SIGMA_ECSN_LABEL),
    'kick_velocity_sigma_USSN': (KICK_VELOCITY_SIGMA_USSN_LABEL),
    'pair_instability_supernovae': _(PULSATIONAL_PAIR_INSTABILITY_SUPERNOVAE_LABEL),
    'pisn_lower_limit': _(PISN_LOWER_LIMIT_LABEL),
    'pisn_upper_limit': _(PISN_UPPER_LIMIT_LABEL),
    'pulsational_pair_instability_supernovae': _(PULSATIONAL_PAIR_INSTABILITY_SUPERNOVAE_LABEL),
    'ppi_lower_limit': _(PPI_LOWER_LIMIT_LABEL),
    'ppi_upper_limit': _(PPI_UPPER_LIMIT_LABEL),
    'pulsational_pair_instability_prescription': _(PULSATIONAL_PAIR_INSTABILITY_PRESCRIPTION_LABEL),
    'maximum_neutron_star_mass': _(MAXIMUM_NEUTRON_STAR_MASS_LABEL),
    'mass_transfer_angular_momentum_loss_prescription': _(MASS_TRANSFER_ANGULAR_MOMENTUM_LOSS_PRESCRIPTION_LABEL),
    'mass_transfer_accertion_efficiency_prescription': _(MASS_TRANSFER_ACCERTION_EFFICIENCY_PRESCRIPTION_LABEL),
    'mass_transfer_fa': _(MASS_TRANSFER_FA_LABEL),
    'mass_transfer_jloss': _(MASS_TRANSFER_JLOSS_LABEL),
}


class COMPASModelRunForm(ModelForm):
    class Meta:
        model = COMPASModelRun
        fields = FIELDS
        labels = LABELS

    def __init__(self, *args, **kwargs):
        super(COMPASModelRunForm, self).__init__(*args, **kwargs)

    def get_initial_parameters(self):
        for field_name in self.fields:
            if field_name in INITIAL_PARAMETERS:
                yield self[field_name]

    def get_advanced_settings(self):
        for field_name in self.fields:
            if field_name in ADVANCED_SETTINGS:
                yield self[field_name]

    def clean(self):

        """
        overwrites the default clean behavior before saving field values to model
        Validate some form fields against each other and push error messages to be displayed in template
        :return: Cleaned data after validation checks pass
        """
        cleaned_data = super().clean()

        mass1 = cleaned_data.get('mass1')
        mass2 = cleaned_data.get('mass2')

        if mass1 and mass2:
            if mass2 > mass1:
                msg = 'Mass 2 should be less than Mass 1'
                self.add_error('mass1', msg)
                self.add_error('mass2', msg)

        separation = cleaned_data.get('separation')
        orbital_period = cleaned_data.get('orbital_period')

        if separation and orbital_period:
            msg = 'Separation and Orbital Period cannot be used together. Specify only one of them'
            self.add_error('separation', msg)
            self.add_error('orbital_period', msg)
        elif not separation and not orbital_period:
            msg = 'Please specify either Separation or Orbital Period'
            self.add_error('separation', msg)
            self.add_error('orbital_period', msg)

        pisn_lower_limit = cleaned_data.get('pisn_lower_limit')
        pisn_upper_limit = cleaned_data.get('pisn_upper_limit')

        if pisn_lower_limit and pisn_upper_limit:
            if pisn_lower_limit > pisn_upper_limit:
                msg = 'PISN_lower_limit should be less than PISN_upper_limit'
                self.add_error('pisn_lower_limit', msg)
                self.add_error('pisn_upper_limit', msg)

        ppi_lower_limit = cleaned_data.get('ppi_lower_limit')
        ppi_upper_limit = cleaned_data.get('ppi_upper_limit')

        if ppi_lower_limit and ppi_upper_limit:
            if ppi_lower_limit > ppi_upper_limit:
                msg = 'PPI_lower_limit should be less than PPI_upper_limit'
                self.add_error('ppi_lower_limit', msg)
                self.add_error('ppi_upper_limit', msg)

        return cleaned_data
