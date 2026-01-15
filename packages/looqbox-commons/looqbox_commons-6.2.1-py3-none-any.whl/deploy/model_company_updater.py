import os
from typing import Any, Mapping

import sys
from pymongo import MongoClient
from pymongo.collection import Collection


def main() -> None:

    looqbox_company_collection = open_mongo_connection()

    company_model_id = 202
    package_version = sys.argv[1]
    package_name = "versionInfo.versions.DYNAMIC_PACKAGE.looqbox_commons"

    company_filter, version_to_update = get_query(company_model_id, package_name, package_version)
    looqbox_company_collection.update_one(company_filter, version_to_update)


def get_query(company_model_id: int, package_name: str, package_version: str) -> tuple[dict, dict]:
    company_filter = {"companyId": company_model_id}
    version_to_update = {"$set": {package_name: package_version}}
    return company_filter, version_to_update


def open_mongo_connection() -> Collection[Mapping[str, Any] | Any]:
    database_url = os.environ["MONGOURL"]
    looqbox_mongo = MongoClient(database_url)
    mongo_database = looqbox_mongo["looqbox"]
    company_collection = mongo_database["company"]
    return company_collection


if __name__ == "__main__":
    main()
