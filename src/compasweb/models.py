import os
import math

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.core.files.uploadedfile import UploadedFile

import tarfile
from bokeh.embed import server_document
import h5py

from .utils.constants import *


class Keyword(models.Model):
    tag = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.tag


def job_directory_path(instance, filename):
    """
    a callable to generate a custom directory path to upload file to
    instance: an instance of the model to which the file belongs
    filename: name of the file to be uploaded
    """
    # change file name if it has spaces
    fname = filename.replace(" ", "_")
    dataset_id = str(instance.compasjob.id)
    model_id = str(instance.compasmodel.id)
    # dataset files will be saved in MEDIA_ROOT/datasets/dataset_id/model_id/
    return os.path.join("datasets", dataset_id, model_id, fname)


class COMPASJob(models.Model):
    author = models.CharField(max_length=255, blank=False, null=False)
    # published defines if the job was published in a journal/arxiv
    published = models.BooleanField(default=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    year = models.IntegerField(null=True)
    journal = models.CharField(max_length=255, null=True)
    journal_DOI = models.CharField(max_length=255, null=True)
    dataset_DOI = models.CharField(max_length=255, null=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    # public defines if the job is publicly accessible
    public = models.BooleanField(default=False)
    download_link = models.TextField(blank=True, null=True)
    arxiv_id = models.CharField(max_length=255, blank=False)
    keywords = models.ManyToManyField(Keyword)

    @classmethod
    def filter_by_keyword(cls, keyword=None):
        return cls.objects.all().filter(keywords__tag=keyword) if keyword else cls.objects.all()

    def __str__(self):
        return self.title


class COMPASModel(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    summary = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class COMPASDatasetModel(models.Model):
    compasjob = models.ForeignKey(COMPASJob, models.CASCADE)
    compasmodel = models.ForeignKey(COMPASModel, models.CASCADE)
    files = models.FileField(upload_to=job_directory_path, blank=True, null=True)

    def __str__(self):
        return f"{self.compasjob.title} - {self.compasmodel.name}"

    def save(self, *args, **kwargs):
        """
        overwrites default save behavior
        """
        super().save(*args, **kwargs)
        # Check file name is not empty after saving the model and uploading file
        if self.files.name:
            # Check the uploaded file could be decompressed using tarfile
            if tarfile.is_tarfile(self.files.path):
                self.decompress_tar_file()
            # If the uploaded file is an individual file
            else:
                self.create_upload(self.files.name)

    def decompress_tar_file(self):
        # Get the actual path for uploaded file
        dataset_dir = os.path.dirname(self.files.path)
        dataset_tar = tarfile.open(self.files.path)
        # dataset_tar.extractall(dataset_dir)
        for member in dataset_tar.getmembers():
            # ignore any directory but include its contnets
            if not member.isdir():
                # extract files into dataset directory (this will create subdirectories as well, exactly as in the tarball)
                dataset_tar.extract(member, dataset_dir)
                self.create_upload(os.path.join(os.path.dirname(self.files.name), member.name))
        dataset_tar.close()
        # remove the tar file after decompression
        os.remove(self.files.path)

    # create an Upload model for an uploaded file
    def create_upload(self, filepath):
        """
        filepath is the relative path of the uploaded file within MEDIA_ROOT
        """
        upload = Upload()
        upload.file = filepath
        upload.datasetmodel = self
        upload.save()

    def get_rundetails(self):
        """
        query file: "run_details.txt"
        """
        return self.upload_set.filter(file__iendswith="Run_Details.txt")

    def get_data(self):
        """
        query file: "*.h5"
        """
        return self.upload_set.filter(file__iendswith=".h5")


class Upload(models.Model):
    file = models.FileField(blank=True, null=True)
    datasetmodel = models.ForeignKey(COMPASDatasetModel, models.CASCADE)

    def __str__(self):
        return os.path.basename(self.file.name)

    def get_content(self):
        """
        get the content of a file; will be called only on txt files
        """
        if self.file.storage.exists(self.file.name):

            with self.file.open("r") as f:
                return f.read()
        else:
            return "File not found"

    def get_plots(self, input, is_mobile=False):
        if input:
            script = server_document(settings.BOKEH_SERVER, arguments={"filename": input, "is_mobile": is_mobile})
        else:
            script = "<p>No data was provided for plots</p>"
        return script

    def read_stats(self):
        """
        read data length in h5 file
        """
        data_stats = {}

        if self.file.storage.exists(self.file.name):
            data = h5py.File(self.file, "r")
            for key in data.keys():
                prim_key = list(data[key])[0]
                stat = len(data[key][prim_key])
                data_stats[key] = stat

        return data_stats


class COMPASModelRun(models.Model):

    # required input parameters
    # --initial-mass-1
    mass1 = models.FloatField(
        blank=False,
        null=False,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(150.0)],
        help_text="Mass of the initially more massive star.  0 < Value < 150",
    )
    # --initial-mass-2
    mass2 = models.FloatField(
        blank=False,
        null=False,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(150.0)],
        help_text="Mass of the initially less massive star. 0 < Value < 150",
    )
    # --metalicity
    metallicity = models.FloatField(
        blank=False,
        null=False,
        default=0.0142,
        validators=[MinValueValidator(1e-4), MaxValueValidator(0.03)],
        help_text="Metallicity of stars.  1E-4 < Value < 0.03",
    )
    # --eccentricity
    eccentricity = models.FloatField(
        blank=False,
        null=False,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1)],
        help_text="Orbital eccentricity of the binary. 0 <= Value < 1",
    )
    # --semi_major_axis
    separation = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        help_text="Value > 0",
    )
    # --orbital_period
    orbital_period = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        help_text="Value > 0",
    )
    # --maximum-evolution-time
    max_time = models.FloatField(
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(1400)],
        help_text="Maximum time to evolve binary for. 0 < Value <= 1400",
    )

    # advanced settings
    # kicks
    kick_enabled = models.BooleanField(default=True)
    common_envelope_enabled = models.BooleanField(default=True)
    mass_transfer_enabled = models.BooleanField(default=True)
    supernova_enabled = models.BooleanField(default=True)

    # --kick-magnitude-random-1
    velocity_random_number_1 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="--kick-magnitude-random-1: Value to be used to draw the kick magnitude for the primary star of a binary system when evolving in BSE mode, should the star undergo a supernova event, 0 < Value < 1",
    )
    # --kick-magnitude-random-2
    velocity_random_number_2 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="--kick-magnitude-random-2: Value to be used to draw the kick magnitude for the secondary star of a binary system when evolving in BSE mode, should the star undergo a supernova event, 0 < Value < 1",
    )
    # --kick-magnitude-1
    velocity_1 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="--kick-magnitude-1(Velocity1): Value to be used as the (drawn) kick magnitude for the primary star of a binary system when evolving in BSE mode, should the star undergo a supernova event (km s −1 ), Value > 0",
    )
    # --kick-magnitude-2
    velocity_2 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=0.0,
        help_text="--kick-magnitude-2(Velocity2): Value to be used as the (drawn) kick magnitude for the secondary star of a binary system when evolving in BSE mode, should the star undergo a supernova event (km s −1 ), Value > 0",
    )

    # --kick-theta-1
    theta_1 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0 * math.pi)],
        help_text="--kick-theta-1: The angle between the orbital plane and the ’z’ axis of the supernova vector for the for the primary star of a binary system when evolving in BSE mode, should it undergo a supernova event (radians), 0 < Value < 2pi",
    )
    # --kick-theta-2
    theta_2 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0 * math.pi)],
        help_text="--kick-theta-2: The angle between the orbital plane and the ’z’ axis of the supernova vector for the for the secondary star of a binary system when evolving in BSE mode, should it undergo a supernova event (radians), 0 < Value < 2pi",
    )
    # --kick-phi-1
    phi_1 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0 * math.pi)],
        help_text="--kick-phi-1: The angle between ’x’ and ’y’, both in the orbital plane of the supernova vector, for the for the primary star of a binary system when evolving in BSE mode, should it undergo a supernova event (radians), 0 < Value < 2pi",
    )
    # --kick-phi-2
    phi_2 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0 * math.pi)],
        help_text="--kick-phi-2: The angle between ’x’ and ’y’, both in the orbital plane of the supernova vector, for the for the seocndary star of a binary system when evolving in BSE mode, should it undergo a supernova event (radians), 0 < Value < 2pi",
    )
    # --kick-mean-anomaly-1
    mean_anomaly_1 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0 * math.pi)],
        help_text="--kick-mean-anomaly-1: The mean anomaly at the instant of the supernova for the primary star of a binary system when evolving in BSE mode, should it undergo a supernova event, 0 < Value < 2pi",
    )
    # --kick-mean-anomaly-2
    mean_anomaly_2 = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0 * math.pi)],
        help_text="--kick-mean-anomaly-2: The mean anomaly at the instant of the supernova for the secondary star of a binary system when evolving in BSE mode, should it undergo a supernova event, 0 < Value < 2pi",
    )

    # common envelope
    # --common-envelope-alpha
    common_envelope_alpha = models.FloatField(
        blank=True,
        null=True,
        default=1.0,
        validators=[MinValueValidator(0.0)],
        help_text="--common-envelope-alpha: Common Envelope efficiency alpha, Value > 0",
    )
    # --common-envelope-lambda-prescription
    common_envelope_lambda_prescription = models.CharField(
        choices=COMMON_ENVELOPE_LAMBDA_PRESCRIPTION_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=COMMON_ENVELOPE_LAMBDA_PRESCRIPTION_NANJING_VALUE,
        help_text="--common-envelope-lambda-prescription: CE lambda prescription",
    )
    # --common-envelope-lambda
    common_envelope_lambda = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=0.1,
        help_text="--common-envelope-lambda: Common Envelope lambda, Value > 0",
    )

    # supernova
    # --remnant-mass-prescription
    remnant_mass_prescription = models.CharField(
        choices=REMNANT_MASS_PRESCRIPTION_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=REMNANT_MASS_PRESCRIPTION_FRYER2012_VALUE,
        help_text="--remnant-mass-prescription: Remnant mass prescription",
    )
    # --fryer-supernova-engine
    fryer_supernova_engine = models.CharField(
        choices=FRYER_SUPERNOVA_ENGINE_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=FRYER_SUPERNOVA_ENGINE_DELAYED_VALUE,
        help_text="--fryer-supernova-engine: Supernova engine type if using the fallback prescription from Fryer et al. (2012)",
    )
    # --black-hole-kicks
    black_hole_kicks = models.CharField(
        choices=BLACK_HOLE_KICKS_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=BLACK_HOLE_KICKS_FALLBACK_VALUE,
        help_text="--black-hole-kicks: Black hole kicks relative to NS kicks",
    )
    # --kick-magnitude-distribution
    Kick_velocity_distribution = models.CharField(
        choices=KICK_VELOCITY_DISTRIBUTION_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=KICK_VELOCITY_DISTRIBUTION_MAXWELLIAN,
        help_text="--kick-magnitude-distribution: Natal kick magnitude distribution",
    )
    # --kick-magnitude-sigma-CCSN-NS
    kick_velocity_sigma_CCSN_NS = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=250.0,
        help_text="--kick-magnitude-sigma-CCSN-NS: Sigma for chosen kick magnitude distribution for neutron stars (km s − 1 ), Value > 0",
    )
    # --kick-magnitude-sigma-CCSN-BH
    kick_velocity_sigma_CCSN_BH = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=256.0,
        help_text="--kick-magnitude-sigma-CCSN-BH: Sigma for chosen kick magnitude distribution for black holes (km s − 1 ), Value > 0",
    )
    # --kick-magnitude-sigma-ECSN
    kick_velocity_sigma_ECSN = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=30.0,
        help_text="--kick-magnitude-sigma-ECSN: Sigma for chosen kick magnitude distribution for ECSN (km s − 1 ), Value > 0",
    )
    # --kick-magnitude-sigma-USSN
    kick_velocity_sigma_USSN = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=30.0,
        help_text="--kick-magnitude-sigma-USSN: Sigma for chosen kick magnitude distribution for USSN (km s − 1 ), Value > 0",
    )

    # --pair-instability-supernovae
    pair_instability_supernovae = models.BooleanField(
        default=True, help_text="--pair-instability-supernovae: Enable pair instability supernovae (PISN)"
    )

    # --pisn-lower-limit
    pisn_lower_limit = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=60.0,
        help_text="--pisn-lower-limit: Minimum core mass for PISN, Value > 0",
    )
    # --pisn-upper-limit
    pisn_upper_limit = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=135.0,
        help_text="--pisn-upper-limit: Maximum core mass for PISN, 0 < Value >  --pisn-lower-limit",
    )
    # --pulsational-pair-instability
    pulsational_pair_instability_supernovae = models.BooleanField(
        default=True,
        help_text="--pulsational-pair-instability: Enable mass loss due to pulsational-pair-instability (PPI)",
    )

    # --pisn-lower-limit
    ppi_lower_limit = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=35.0,
        help_text="--pisn-lower-limit: Minimum core mass for PPI, Value > 0",
    )
    # --pisn-upper-limit
    ppi_upper_limit = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=60.0,
        help_text="--pisn-upper-limit: Maximum core mass for PPI, 0 < Value > --pisn-lower-limit",
    )
    # --pulsational-pair-instability-prescription
    pulsational_pair_instability_prescription = models.CharField(
        choices=PULSATIONAL_PAIR_INSTABILITY_PRESCRIPTION_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=PULSATIONAL_PAIR_INSTABILITY_PRESCRIPTION_MARCHANT,
        help_text="--pulsational-pair-instability-prescription: Pulsational pair instability prescription",
    )
    # --maximum-neutron-star-mass
    maximum_neutron_star_mass = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=3.0,
        help_text="--maximum-neutron-star-mass: Maximum mass of a neutron star, Value > 0",
    )

    # Mass transfer
    # --mass-transfer-angular-momentum-loss-prescription
    mass_transfer_angular_momentum_loss_prescription = models.CharField(
        choices=MASS_TRANSFER_ANGULAR_MOMENTUM_LOSS_PRESCRIPTION_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=MASS_TRANSFER_ANGULAR_MOMENTUM_LOSS_PRESCRIPTION_ISOTROPIC_VALUE,
        help_text="--mass-transfer-angular-momentum-loss-prescription: Mass Transfer Angular Momentum Loss prescription",
    )
    # --mass-transfer-accretion-efficiency-prescription
    mass_transfer_accertion_efficiency_prescription = models.CharField(
        choices=MASS_TRANSFER_ACCERTION_EFFICIENCY_PRESCRIPTION_CHOICES,
        max_length=55,
        blank=True,
        null=True,
        default=MASS_TRANSFER_ACCERTION_EFFICIENCY_PRESCRIPTION_THERMAL_VALUE,
        help_text="--mass-transfer-accretion-efficiency-prescription: Mass transfer accretion efficiency prescription",
    )
    # Ideally should only appear if using --mass-transfer-accretion-efficiency-prescription FIXED
    # --mass-transfer-fa
    mass_transfer_fa = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=0.5,
        help_text='--mass-transfer-fa: Mass Transfer fraction accreted in FIXED prescription',
    )
    # Ideally should only appear if using --mass-transfer-angular-momentum-loss-prescription ARBITRARY
    # --mass-transfer-jloss
    mass_transfer_jloss = models.FloatField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0)],
        default=1.0,
        help_text='--mass-transfer-jloss: Specific angular momentum with which the non-accreted system leaves the system',
    )

    def save(self, *args, **kwargs):
        """
        overwrites default save model behavior
        """
        super().save(*args, **kwargs)
        self.save_BSE_Grid_file()

    def save_BSE_Grid_file(self):
        """
        saves initial parameters and advanced settings in BSE_grid.txt file to filesystem
        """
        content = ""

        for field in self._meta.get_fields():
            field_value = getattr(self, field.name)
            if field_value and (field.name in FIELD_COMMANDS):
                if field.name in INITIAL_PARAMETERS:
                    # or (self.kick_enabled and (field.name in KICK_SETTINGS))\
                    # or (self.common_envelope_enabled and (field.name in COMMON_ENVELOPE_SETTINGS))\
                    # or (self.supernova_enabled and (field.name in SUPERNOVA_SETTINGS))\
                    # or (self.mass_transfer_enabled and (field.name in MASS_TRANSFER_SETTINGS)):
                    # print (f'Name: {field.name}, Value: {field_value} Initial')
                    content += f'{FIELD_COMMANDS[field.name]} {field_value}' + " "
                elif self.kick_enabled and (field.name in KICK_SETTINGS):
                    # print (f'Name: {field.name}, Value: {field_value} Kick')
                    content += f'{FIELD_COMMANDS[field.name]} {field_value}' + " "
                elif self.common_envelope_enabled and (field.name in COMMON_ENVELOPE_SETTINGS):
                    # print (f'Name: {field.name}, Value: {field_value} COMMON_ENVELOPE')
                    content += f'{FIELD_COMMANDS[field.name]} {field_value}' + " "
                elif self.supernova_enabled and (field.name in SUPERNOVA_SETTINGS):
                    # print (f'Name: {field.name}, Value: {field_value} supernova')
                    content += f'{FIELD_COMMANDS[field.name]} {field_value}' + " "
                elif self.mass_transfer_enabled and (field.name in MASS_TRANSFER_SETTINGS):
                    # print (f'Name: {field.name}, Value: {field_value} mass transfer')
                    content += f'{FIELD_COMMANDS[field.name]} {field_value}' + " "

        print(content)
        # path where the file is saved: media_root/job_key
        storage_location = os.path.join(settings.MEDIA_ROOT, 'jobs', str(self.id))
        # create directory
        if not os.path.exists(storage_location):
            os.makedirs(
                storage_location,
            )
        # name parameter file
        grid_file_path = os.path.join(storage_location, 'BSE_grid.txt')

        # write parameters string to file
        with open(grid_file_path, 'w') as f:
            f.write(content)

        # # save file url to database
        # self.parameter_file_url = self.job_key + "/galaxia_param"
        # # save file content to database as bytes
        # self.parameters = bytes(content, encoding='utf-8')
