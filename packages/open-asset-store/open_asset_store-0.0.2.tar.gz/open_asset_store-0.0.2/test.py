from asset_store.repository.neo4j import NeoRepository
from asset_store.types import Edge
from asset_store.types import Entity
from asset_model import FQDN
from asset_model import IPAddress, IPAddressType
from asset_model import BasicDNSRelation
from asset_model import DNSRecordProperty
from asset_model import SourceProperty

uri = "neo4j://localhost"
auth = ("neo4j", "password")

with NeoRepository(uri, auth) as db:
    fqdn = db.create_asset(FQDN("owasp.org"))
    
    ip = db.create_entity(
        Entity(
            asset = IPAddress("104.20.44.163", IPAddressType.IPv4)))
    
    a_record  = db.create_edge(
        Edge(
            relation    = BasicDNSRelation("dns_record", rrtype=1, rrname="A"),
            from_entity = fqdn,
            to_entity   = ip))
    
    txt_record = db.create_entity_property(
        fqdn,
        DNSRecordProperty("dns_record", "token=awes0me", 16, "TXT"))
    
    source = db.create_edge_property(
        a_record,
        SourceProperty("myscript", 100))
