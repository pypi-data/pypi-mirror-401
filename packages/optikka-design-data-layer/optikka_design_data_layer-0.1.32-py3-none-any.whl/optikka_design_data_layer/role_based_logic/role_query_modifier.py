"""
Modify the query for the given role.
"""

from optikka_design_data_layer.validation import Role#pylint: disable=import-error
from ods_types import ODSObjectType#pylint: disable=import-error

def modify_query_for_role(
    query: dict,
    user_info: dict[str, str],#role: Role, account_id: str, studio_id: str, user_id: str
    object_type: ODSObjectType,
) -> dict:
    """
    Modify the query for the given role.
    """
    #brand related objects
    if object_type == ODSObjectType.BRAND or object_type == ODSObjectType.BRAND_REGISTRY:
        return _modify_query_for_studios_and_accounts_related_object(#universal filter for brand and brand registry as it is a brand-level object
            query, user_info, use_universal_filter=True
        )
    #template related objects
    if object_type == ODSObjectType.TEMPLATE_REGISTRY:
        return _modify_query_for_studios_and_accounts_related_object(#no universal filter for template registry as it doesnt have this
            query, user_info, use_universal_filter=False
        )
    if object_type == ODSObjectType.TEMPLATE_INPUT or object_type == ODSObjectType.RENDER_RUN or object_type == ODSObjectType.TEMPLATE_INPUT_JOB:#both have studio and account id (singular)
        return _modify_query_for_studio_and_account_related_object(
            query, user_info
        )


#HELPER FUNCTIONS BY OBJECT TYPE#
#OBJECTS THAT HAVE STUDIO AND ACCOUNT IDS AND UNIVERSAL FILTER#
def _modify_query_for_studios_and_accounts_related_object(
    mongo_query: dict,
    user_info: dict[str, str],
    use_universal_filter: bool = True,
) -> dict:
    """
    Modify the query for the given brand.
    """
    if user_info["role"] == Role.SUPER_ADMIN.value:
        return mongo_query #no modifications needed, do whatever the user wants
    if use_universal_filter:
    #build the role-based filter with universal access as base
        role_filter: dict = {"$or": [{"is_universal": True}]}
    else:
        role_filter: dict = {"$or": []}
    #if admin, scope to the account + universal filter
    if user_info["role"] == Role.ADMIN.value:
        role_filter["$or"].append({"account_ids": user_info["account_id"]}) #scope to the account
    #if read only, scope to the studio + universal filter
    elif user_info["role"] == Role.READ_ONLY.value or user_info["role"] == Role.READ_WRITE.value:
        role_filter["$or"].append({"studio_ids": user_info["studio_id"]}) #scope to the studio

    #wrap original query + role filter in $and to force the filtering
    return {
        "$and": [
            mongo_query,
            role_filter
        ]
    }

def _modify_query_for_studio_and_account_related_object(
    query: dict, user_info: dict[str, str]
) -> dict:
    """
    Modify the query for the given render run.
    """
    if user_info["role"] == Role.SUPER_ADMIN.value:
        return query #no modifications needed, do whatever the user wants

    final_query: dict = {"$and": [query]}
    if user_info["role"] == Role.ADMIN.value:
        final_query["$and"].append({"account_id": user_info["account_id"]})
    if user_info["role"] == Role.READ_ONLY.value or user_info["role"] == Role.READ_WRITE.value:
        final_query["$and"].append({"studio_id": user_info["studio_id"]})
    return final_query

