import pytest
from cloudevents.abstract import CloudEvent

from ucam_faas.tests.fixtures import make_cloud_event

# Register the ucam_faas testing module as a pytest plugin - as it provides
# fixtures that we can make use of when testing the functions.
pytest_plugins = ["ucam_faas.testing"]


@pytest.fixture()
def valid_cloud_event() -> CloudEvent:
    return make_cloud_event(type="ucam_faas_event", source="ucam_faas", data={"foo": "bar"})
