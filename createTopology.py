import auth
from vmware.vapi.bindings.struct import PrettyPrinter

from com.vmware.nsx_policy.model_client import Tier1
from com.vmware.nsx_policy.model_client import Segment
from com.vmware.nsx_policy.model_client import Tag
from com.vmware.nsx_policy.model_client import SegmentSubnet

from com.vmware.nsx_policy.model_client import ApiError
from com.vmware.vapi.std.errors_client import Error


def main():

    api_client = auth.create_nsx_policy_api_client(
        "admin", "superSecretPassword", "nsx1.yasen.local", 443,
        auth_type=auth.SESSION_AUTH)

    # Create a pretty printer to make the output look nice.
    pp = PrettyPrinter()

    tag1 = Tag(
        scope="Event",
        tag="VMworld2019"
    )
    tag2 = Tag(
        scope="Session",
        tag="CODE2544U"
    )

    tagList = [tag1, tag2]

    t1id = 'my_t1_id'
    tier1 = Tier1(
        id=t1id,
        display_name='myVMworldT1',
        description='T1 GW created using python SDK for VMworld demo',
        route_advertisement_types=['TIER1_STATIC_ROUTES', 'TIER1_CONNECTED'],
        tier0_path='/infra/tier-0s/t0',
        tags=tagList
    )

    try:
        api_client.infra.Tier1s.patch(t1id, tier1)
        newTier1 = api_client.infra.Tier1s.get(t1id)
        pp.pprint(newTier1)
    except Error as ex:
        api_error = ex.data.convert_to(ApiError)
        print("An error occurred when creating Segment: %s" % api_error.error_message)

    subnet = SegmentSubnet(
        dhcp_ranges=None,
        gateway_address='10.114.209.121/30',
        network='10.114.209.120/30',
    )

    segmentId = 'testSegmentId'
    segment = Segment(
        id=segmentId,
        display_name='testSegmentName',
        tags=tagList,
        subnets=[subnet],
        connectivity_path='/infra/tier-1s/%s' % t1id,
        transport_zone_path='/infra/sites/default/enforcement-points/default/transport-zones/4052b9da-2912-4c79-8709-3e25a34457ac'
    )

    try:
        api_client.infra.Segments.patch(segmentId, segment)
        newSegment = api_client.infra.Segments.get(segmentId)
        pp.pprint(newSegment)
    except Error as ex:
        api_error = ex.data.convert_to(ApiError)
        print("An error occurred when creating Segment: %s" % api_error.error_message)




if __name__ == "__main__":
    main()