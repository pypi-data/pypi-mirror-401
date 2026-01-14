from asset_model import AssetType, RelationType
from asset_model import get_asset_by_type, get_relation_by_type
from asset_model import describe_oam_object

fqdn_cls = get_relation_by_type(RelationType.BasicDNSRelation)


