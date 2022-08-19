Generating endpoint libraries
================================

# TODO This is documentation stub - not yet used anywhere

Endpoint method names
-----------------------
Method names are first generated from ``operationId`` property from OpenAPI. Following property::

    "operationId": "restGenTokenUsingGET"

results in method name::

    def rest_gen_token_using_get()

If ``operationId`` does not exist, the name is generated from method and path. Given spec::

    (...)
    "paths": {
        "/perf-test/tokensCount": {
            "get": {}
        "/check-name/generate-nid-identity/{nickname}": {
            "post": {}
    (...)

Following names are generated::

    def get_perf_test_tokens_count()

    def post_check_name_generate_nid_identity_nickname()


