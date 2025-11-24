post_group = {"groupname": "g", "replies": [{"attribute": "Filter-Id", "op": ":=", "value": "10m"}]}

post_group_bad_user = post_group | {"users": [{"username": "non-existing-user", "priority": 1}]}

post_group_only_user = {"groupname": "g", "users": [{"username": "u"}]}

patch_group_only_checks = {
    "replies": [],
    "checks": [{"attribute": "Auth-Type", "op": ":=", "value": "Accept"}],
    "users": [],
}
patch_group_only_replies = {
    "replies": [{"attribute": "Filter-Id", "op": ":=", "value": "20m"}],
    "checks": [],
    "users": None,  # same as empty list
}
patch_group_only_users = {
    "replies": None,  # same as empty list
    "checks": None,  # same as empty list
    "users": [{"username": "u"}],
}
patch_group_bad_user = patch_group_only_checks | {"users": [{"username": "non-existing-user"}]}
patch_group_dup_user = patch_group_only_checks | {"users": [{"username": "u"}, {"username": "u"}]}

post_user = {
    "username": "u",
    "checks": [{"attribute": "Cleartext-Password", "op": ":=", "value": "my-pass"}],
    "replies": [
        {"attribute": "Framed-IP-Address", "op": ":=", "value": "10.0.0.1"},
        {"attribute": "Framed-Route", "op": "+=", "value": "192.168.1.0/24"},
        {"attribute": "Framed-Route", "op": "+=", "value": "192.168.2.0/24"},
        {"attribute": "Huawei-Vpn-Instance", "op": ":=", "value": "my-vrf"},
    ],
}

post_user_bad_group = post_user | {"groups": [{"groupname": "non-existing-group", "priority": 1}]}

post_user_with_group = post_user | {"groups": [{"groupname": "g", "priority": 1}]}

post_user_only_group = {"username": "u", "groups": [{"groupname": "g"}]}

patch_user_only_checks = {
    "replies": [],
    "checks": [{"attribute": "Auth-Type", "op": ":=", "value": "Accept"}],
    "groups": [],
}
patch_user_only_replies = {
    "replies": [{"attribute": "Framed-IP-Address", "op": ":=", "value": "10.0.0.1"}],
    "checks": [],
    "groups": None,  # same as empty list
}
patch_user_only_groups = {
    "replies": None,  # same as empty list
    "checks": None,  # same as empty list
    "groups": [{"groupname": "g"}],
}
patch_user_bad_group = {"groups": [{"groupname": "non-existing-group"}]}
patch_user_dup_group = {"groups": [{"groupname": "g"}, {"groupname": "g"}]}

post_nas = {"nasname": "5.5.5.5", "secret": "my-secret", "shortname": "my-nas"}

patch_nas = {"secret": "new-secret", "shortname": "new-nas"}

# Expected results

get_group = {
    "groupname": "g",
    "checks": [],
    "replies": [{"attribute": "Filter-Id", "op": ":=", "value": "10m"}],
    "users_number": 0,
}

get_group_patched_only_checks = {
    "groupname": "g",
    "checks": [{"attribute": "Auth-Type", "op": ":=", "value": "Accept"}],
    "replies": [],
    "users_number": 0,
}

get_group_patched_only_replies = {
    "groupname": "g",
    "checks": [],
    "replies": [{"attribute": "Filter-Id", "op": ":=", "value": "20m"}],
    "users_number": 0,
}

get_group_patched_only_users = {
    "groupname": "g",
    "checks": [],
    "replies": [],
    "users_number": 0,
}

get_user = {
    "username": "u",
    "checks": [{"attribute": "Cleartext-Password", "op": ":=", "value": "my-pass"}],
    "replies": [
        {"attribute": "Framed-IP-Address", "op": ":=", "value": "10.0.0.1"},
        {"attribute": "Framed-Route", "op": "+=", "value": "192.168.1.0/24"},
        {"attribute": "Framed-Route", "op": "+=", "value": "192.168.2.0/24"},
        {"attribute": "Huawei-Vpn-Instance", "op": ":=", "value": "my-vrf"},
    ],
    "groups": [{"groupname": "g", "priority": 1}],
}

get_user_patched_only_checks = {
    "username": "u",
    "checks": [{"attribute": "Auth-Type", "op": ":=", "value": "Accept"}],
    "replies": [],
    "groups": [],
}

get_user_patched_only_replies = {
    "username": "u",
    "checks": [],
    "replies": [{"attribute": "Framed-IP-Address", "op": ":=", "value": "10.0.0.1"}],
    "groups": [],
}

get_user_patched_only_groups = {
    "username": "u",
    "checks": [],
    "replies": [],
    "groups": [{"groupname": "g", "priority": 1}],
}

get_nas = {"nasname": "5.5.5.5", "secret": "my-secret", "shortname": "my-nas"}

get_nas_patched = {"nasname": "5.5.5.5", "secret": "new-secret", "shortname": "new-nas"}
