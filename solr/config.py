import pysolr
solr_url = 'http://172.18.102.127:8983/solr/#/'
solr = pysolr.Solr(solr_url)


class SolrInstance:
    instance=None
    try:
        response = solr.ping()
        if response == 'pong':
            print('Connection to Solr server successful!')
        else:
            print('Connection to Solr server failed.')
    except Exception as e:
        print(e)

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__new__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
