
from .config import SolrInstance

solr=SolrInstance()
print(solr.instance)
solr.instance.create_core('mycore')
# Define the schema for the core
schema = [
    {
        "name": "id",
        "type": "string",
        "indexed": True,
        "stored": True,
        "required": True,
        "uniqueKey": True
    },
    {
        "name": "title",
        "type": "text_general",
        "indexed": True,
        "stored": True
    },
    {
        "name": "content",
        "type": "text_general",
        "indexed": True,
        "stored": True
    }
]
# Configure the schema for the core
solr.schema.create('mycore', schema)
