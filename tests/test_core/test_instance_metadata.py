import sure  # noqa # pylint: disable=unused-import
import requests

from moto import mock_ec2, settings

if settings.TEST_SERVER_MODE:
    BASE_URL = "http://localhost:5000"
else:
    BASE_URL = "http://169.254.169.254"


@mock_ec2
def test_latest_meta_data():
    res = requests.get(f"{BASE_URL}/latest/meta-data/")
    res.content.should.equal(b"iam")


@mock_ec2
def test_meta_data_iam():
    res = requests.get(f"{BASE_URL}/latest/meta-data/iam")
    json_response = res.json()
    default_role = json_response["security-credentials"]["default-role"]
    default_role.should.contain("AccessKeyId")
    default_role.should.contain("SecretAccessKey")
    default_role.should.contain("Token")
    default_role.should.contain("Expiration")


@mock_ec2
def test_meta_data_security_credentials():
    res = requests.get(f"{BASE_URL}/latest/meta-data/iam/security-credentials/")
    res.content.should.equal(b"default-role")


@mock_ec2
def test_meta_data_default_role():
    res = requests.get(
        f"{BASE_URL}/latest/meta-data/iam/security-credentials/default-role"
    )
    json_response = res.json()
    json_response.should.contain("AccessKeyId")
    json_response.should.contain("SecretAccessKey")
    json_response.should.contain("Token")
    json_response.should.contain("Expiration")
