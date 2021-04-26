# Generated by Django 2.2.14 on 2021-04-13 03:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compasweb', '0009_auto_20210413_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compasmodelrun',
            name='Kick_velocity_distribution',
            field=models.CharField(blank=True, choices=[('ZERO', 'ZERO'), ('FIXED', 'FIXED'), ('FLAT', 'FLAT'), ('MAXWELLIAN', 'MAXWELLIAN'), ('BRAYELDRIDGE', 'BRAYELDRIDGE'), ('MULLER2016', 'MULLER2016'), ('MULLER2016MAXWELLIAN', 'MULLER2016MAXWELLIAN'), ('MULLERMANDEL', 'MULLERMANDEL')], default='MAXWELLIAN', help_text='--kick-magnitude-distribution: Natal kick magnitude distribution', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='black_hole_kicks',
            field=models.CharField(blank=True, choices=[('FALLBACK', 'FALLBACK'), ('FULL', 'FULL'), ('REDUCED', 'REDUCED'), ('ZERO', 'ZERO')], default='FALLBACK', help_text='--black-hole-kicks: Black hole kicks relative to NS kicks', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='common_envelope_alpha',
            field=models.FloatField(blank=True, default=1.0, help_text='--common-envelope-alpha: Common Envelope efficiency alpha, Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='common_envelope_lambda',
            field=models.FloatField(blank=True, default=0.1, help_text='--common-envelope-lambda: Common Envelope lambda, Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='common_envelope_lambda_prescription',
            field=models.CharField(blank=True, choices=[('LAMBDA_FIXED', 'LAMBDA_FIXED'), ('LAMBDA_KRUCKOW', 'LAMBDA_KRUCKOW'), ('LAMBDA_LOVERIDGE', 'LAMBDA_LOVERIDGE'), ('LAMBDA_NANJING', 'LAMBDA_NANJING'), ('LAMBDA_DEWI', 'LAMBDA_DEWI')], default='LAMBDA_NANJING', help_text='--common-envelope-lambda-prescription: CE lambda prescription', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='fryer_supernova_engine',
            field=models.CharField(blank=True, choices=[('DELAYED', 'DELAYED'), ('RAPID', 'RAPID')], default='DELAYED', help_text='--fryer-supernova-engine: Supernova engine type if using the fallback prescription from Fryer et al. (2012)', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='kick_velocity_sigma_CCSN_BH',
            field=models.FloatField(blank=True, default=256.0, help_text='--kick-magnitude-sigma-CCSN-BH: Sigma for chosen kick magnitude distribution for black holes (km s − 1 ), Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='kick_velocity_sigma_CCSN_NS',
            field=models.FloatField(blank=True, default=250.0, help_text='--kick-magnitude-sigma-CCSN-NS: Sigma for chosen kick magnitude distribution for neutron stars (km s − 1 ), Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='kick_velocity_sigma_ECSN',
            field=models.FloatField(blank=True, default=30.0, help_text='--kick-magnitude-sigma-ECSN: Sigma for chosen kick magnitude distribution for ECSN (km s − 1 ), Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='mass_transfer_accertion_efficiency_prescription',
            field=models.CharField(blank=True, choices=[('THERMAL', 'THERMAL'), ('FIXED', 'FIXED')], default='THERMAL', help_text='--mass-transfer-accretion-efficiency-prescription: Mass transfer accretion efficiency prescription', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='mass_transfer_angular_momentum_loss_prescription',
            field=models.CharField(blank=True, choices=[('ARBITRARY', 'ARBITRARY'), ('ISOTROPIC', 'ISOTROPIC'), ('JEANS', 'JEANS'), ('CIRCUMBINARY', 'CIRCUMBINARY')], default='ISOTROPIC', help_text='--mass-transfer-angular-momentum-loss-prescription: Mass Transfer Angular Momentum Loss prescription', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='mass_transfer_fa',
            field=models.FloatField(blank=True, default=0.5, help_text='--mass-transfer-fa: Mass Transfer fraction accreted in FIXED prescription', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='mass_transfer_jloss',
            field=models.FloatField(blank=True, default=1.0, help_text='--mass-transfer-jloss: Specific angular momentum with which the non-accreted system leaves the system', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='maximum_neutron_star_mass',
            field=models.FloatField(blank=True, default=3.0, help_text='--maximum-neutron-star-mass: Maximum mass of a neutron star, Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='pisn_lower_limit',
            field=models.FloatField(blank=True, default=60.0, help_text='--pisn-lower-limit: Minimum core mass for PISN, Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='pisn_upper_limit',
            field=models.FloatField(blank=True, default=135.0, help_text='--pisn-upper-limit: Maximum core mass for PISN, 0 < Value >  --pisn-lower-limit', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='ppi_lower_limit',
            field=models.FloatField(blank=True, default=35.0, help_text='--pisn-lower-limit: Minimum core mass for PPI, Value > 0', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='ppi_upper_limit',
            field=models.FloatField(blank=True, default=60.0, help_text='--pisn-upper-limit: Maximum core mass for PPI, 0 < Value > --pisn-lower-limit', null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='pulsational_pair_instability_prescription',
            field=models.CharField(blank=True, choices=[('COMPAS', 'COMPAS'), ('STARTRACK', 'STARTRACK'), ('MARCHANT', 'MARCHANT')], default='MARCHANT', help_text='--pulsational-pair-instability-prescription: Pulsational pair instability prescription', max_length=55, null=True),
        ),
        migrations.AlterField(
            model_name='compasmodelrun',
            name='remnant_mass_prescription',
            field=models.CharField(blank=True, choices=[('HURLEY2000', 'HURLEY2000'), ('BELCZYNSKI2002', 'BELCZYNSKI2002'), ('FRYER2012', 'FRYER2012'), ('MULLER2016', 'MULLER2016'), ('MULLERMANDEL', 'MULLERMANDEL')], default='FRYER2012', help_text='--remnant-mass-prescription: Remnant mass prescription', max_length=55, null=True),
        ),
    ]