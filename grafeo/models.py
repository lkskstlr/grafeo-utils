from django.db import models
from django.contrib.postgres.fields import ArrayField
from data.crypto_base import separators, current_version_major, current_version_minor, current_version_patch


class Producer(models.Model):
    """Database Model of a Producer"""

    """Public Key"""
    pub_key = models.CharField(
        max_length=64,
        primary_key=True,
        help_text="The public key which uniquely identifies the producer. Encoded as hex-string (characters 0-f representing 4 bits each).",
    )

    """Major Version Number. Version = major.minor.patch"""
    version_major = models.IntegerField(
        default=current_version_major,
    )

    """Minor Version Number. Version = major.minor.patch"""
    version_minor = models.IntegerField(
        default=current_version_minor,
    )

    """Patch Version Number. Version = major.minor.patch"""
    version_patch = models.IntegerField(
        default=current_version_patch,
    )

    """Full name in Human Readable Form"""
    name = models.TextField(
        help_text="This should be the full producer name in a Human Readable Form",
        )
    
    """Signature of the serialized version with the private key"""
    signature = models.CharField(
        max_length=128,
        help_text="Construct the payload as utf-8 string. Convert to binary and sign with the producers private key",
    )

    def __str__(self):
        return self.name

    def payload(self) -> str:
        """Returns the payload associated with a producer"""

        return separators.field.join([
            self.pub_key,
            separators.list.join([
                str(self.version_major),
                str(self.version_minor),
                str(self.version_patch)
            ]),
            self.name])


class Product(models.Model):
    """Database Model of a Product"""

    """Public key"""
    pub_key = models.CharField(
        max_length=64,
        primary_key=True,
        help_text="The public key which uniquely identifies the product. Encoded as hex-string (characters 0-f representing 4 bits each)."
    )

    """Major Version Number. Version = major.minor.patch"""
    version_major = models.IntegerField(
        default=current_version_major,
    )

    """Minor Version Number. Version = major.minor.patch"""
    version_minor = models.IntegerField(
        default=current_version_minor,
    )

    """Patch Version Number. Version = major.minor.patch"""
    version_patch = models.IntegerField(
        default=current_version_patch,
    )

    """Full name in Human Readable Form"""
    name = models.TextField(
        help_text="This should be the full product name in a Human Readable Form",
        )

    """Producer"""
    producer_pub_key = models.CharField(
        max_length=64,
        help_text="The public key which uniquely identifies the producer. Encoded as hex-string (characters 0-f representing 4 bits each).",
    )

    """Inputs"""
    input_pub_keys = ArrayField(
        base_field=models.CharField(
            max_length=64,
            help_text="The public key which uniquely identifies the input product. Encoded as hex-string (characters 0-f representing 4 bits each).",
        ),
        null=True
    )

    """Own Signatures"""
    product_signature = models.CharField(
        max_length=128,
        help_text="Construct the payload as utf-8 string. Convert to binary and sign with the product's private key",
    )

    """Signature with the producers private"""
    producer_signature = models.CharField(
        max_length=128,
        help_text="Construct the payload as utf-8 string. Convert to binary and sign with the producers private key",
    )

    """Signatures with the inputs private keys"""
    input_signatures = ArrayField(
        base_field=models.CharField(
            max_length=128,
            help_text="Construct the payload as utf-8 string. Convert to binary and sign with the inputs private key",
        ),
        null=True,
    )

    def __str__(self):
        return self.name

    def payload(self):
        """Returns the payload associated with this product"""

        return separators.field.join([
            self.pub_key,
            separators.list.join([
                str(self.version_major),
                str(self.version_minor),
                str(self.version_patch)
            ]),
            self.name,
            self.producer_pub_key,
            separators.list.join(self.input_pub_keys),
        ])
