import logging


class LiminaURIs:
    def __init__(self, url=None, scheme=None, host=None, port=None, **kwargs):
        if url:
            self._limina_uri = url
        elif scheme and host:
            self.valid_schemes = ["http", "https"]
            scheme = scheme.split("://")[0]
            if scheme not in self.valid_schemes:
                raise ValueError(
                    f"Scheme must be one of the following: {', '.join(self.valid_schemes)}"
                )
            port = f":{port}" if port else ""
            self._limina_uri = f"{scheme}://{host}{port}"
        else:
            raise ValueError(
                "LiminaClient needs either a url, or a scheme and host to initialize. You can find more information on which url to use here: https://docs.getlimina.ai/client/"
            )

    @property
    def limina_uri(self):
        return self._limina_uri

    @property
    def bleep(self):
        return self._create_uri(self.limina_uri, "bleep")

    @property
    def health(self):
        return self._create_uri(self.limina_uri, "healthz")

    @property
    def metrics(self):
        return self._create_uri(self.limina_uri, "metrics")

    @property
    def diagnostics(self):
        return self._create_uri(self.limina_uri, "diagnostics")

    @property
    def process_text(self):
        return self._create_uri(self.limina_uri, "process", "text")

    @property
    def process_files_uri(self):
        return self._create_uri(self.limina_uri, "process", "files", "uri")

    @property
    def reidentify_text(self):
        return self._create_uri(self.limina_uri, "process", "text", "reidentify")

    @property
    def process_files_base64(self):
        return self._create_uri(self.limina_uri, "process", "files", "base64")

    @property
    def ner_text(self):
        return self._create_uri(self.limina_uri, "ner", "text")

    @property
    def analyze_text(self):
        return self._create_uri(self.limina_uri, "analyze", "text")

    @property
    def version(self):
        return self._create_uri(self.limina_uri, "")

    def _create_uri(self, *args):
        return "/".join([x.strip("/") for x in args])
