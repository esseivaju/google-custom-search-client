import httplib2
import json

from googleapiclient.discovery import build
from urllib.parse import parse_qs


class CustomSearchParams:

    def __init__(self, rights=None, num=None, siteSearchFilter=None,
                 imgColorType=None, sort=None, lowRange=None, orTerms=None,
                 imgSize=None, linkSite=None, gl=None, c2coff=None, q=None,
                 excludeTerms=None, fileType=None, imgType=None, start=None,
                 filter=None, dateRestrict=None, imgDominantColor=None,
                 hq=None, cx=None, searchType=None, cr=None, lr=None,
                 highRange=None, relatedSite=None, safe=None, hl=None,
                 exactTerms=None, siteSearch=None, googlehost=None,
                 x__xgafv=None):
        self.rights = rights
        self.num = num
        self.siteSearchFilter = siteSearchFilter
        self.imgColorType = imgColorType
        self.sort = sort
        self.lowRange = lowRange
        self.orTerms = orTerms
        self.imgSize = imgSize
        self.linkSite = linkSite
        self.gl = gl
        self.c2coff = c2coff
        self.q = q
        self.excludeTerms = excludeTerms
        self.fileType = fileType
        self.imgType = imgType
        self.start = start
        self.filter = filter
        self.dateRestrict = dateRestrict
        self.imgDominantColor = imgDominantColor
        self.hq = hq
        self.cx = cx
        self.searchType = searchType
        self.cr = cr
        self.lr = lr
        self.highRange = highRange
        self.relatedSite = relatedSite
        self.safe = safe
        self.hl = hl
        self.exactTerms = exactTerms
        self.siteSearch = siteSearch
        self.googlehost = googlehost
        self.x__xgafv = x__xgafv

    def __str__(self):
        return json.dumps(self.__dict__)

    def to_qs(self):
        s = ""
        for k, v in self.__dict__.items():
            if not v:
                continue
            sep = '&' if s else ""
            s = f"{s}{sep}{k}={v}"
        return s

    def from_qs(querystring):
        params = parse_qs(querystring)
        for k, v in params.items():
            if isinstance(v, list) and len(v) == 1:
                params[k] = v[0]
        if not params:
            params['q'] = querystring
        return CustomSearchParams(**params)


class CustomSearchService:

    def __init__(self, apikey, search_engine=None):
        self.__http_client = httplib2.Http(cache=".cache")
        self.__service = build("customsearch", "v1",
                               http=self.__http_client, developerKey=apikey)
        self.__batch = self._new_batch()
        self.__api_key = apikey
        self.__search_engine = search_engine

    def _new_batch(self):
        return self.__service.new_batch_http_request(callback=self.__batch_cb)

    def __batch_cb(self, request_id, response, exception):
        with open(f"{request_id}.json", "w") as f:
            json.dump(response, f)

    def search(self, callback=None, *args, **kwargs):
        if "cx" not in kwargs or not kwargs["cx"]:
            kwargs["cx"] = self.__search_engine

        request = self.__service.cse().list(*args, **kwargs)
        self.__batch.add(request, callback=callback)

    def search_csp(self, csp, callback=None):
        self.search(callback=callback, **csp.__dict__)

    def search_qs(self, qs, callback=None):
        self.search_csp(CustomSearchParams.from_qs(qs), callback=callback)

    def flush(self):
        self.__batch.execute(self.__http_client)
        self.__batch = self._new_batch()

    def register_search_engine(self, search_engine_id):
        self.__search_engine = search_engine_id

    def update_apikey(self, apikey):
        self.__service = build("customsearch", "v1",
                               http=self.__http_client, developerKey=apikey)
        self.__api_key = apikey

    def get_search_engine(self):
        return self.__search_engine

    def is_configured(self):
        return self.__api_key is not None and self .__search_engine is not None


if __name__ == "__main__":
    querystring = "q=rust&cx=1234"
    csp = CustomSearchParams.from_qs(querystring)
    s = str(csp)
    print(s)
    data = json.loads(s)
    csp = CustomSearchParams(**data)
    print(csp)
    print(csp.to_qs())
    csp = CustomSearchParams(**csp.__dict__)
    print(csp)
    csp = CustomSearchParams.from_qs("querystring")
    print(csp)
