# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from auto_nag import utils
from auto_nag.bzcleaner import BzCleaner
from auto_nag.people import People


class MetaNoDepsNoActivity(BzCleaner):
    def __init__(self):
        super(MetaNoDepsNoActivity, self).__init__()
        self.people = People.get_instance()
        self.nmonths = utils.get_config(self.name(), "months_lookup")
        self.max_ni = utils.get_config(self.name(), "max_ni")
        self.skiplist = set(utils.get_config(self.name(), "skiplist", []))

    def description(self):
        return "Bugs with meta keyword, not depending on bugs and no activity for the last {} months".format(
            self.nmonths
        )

    def get_extra_for_needinfo_template(self):
        return self.get_extra_for_template()

    def get_extra_for_template(self):
        return {"nmonths": self.nmonths}

    def get_auto_ni_skiplist(self):
        return self.skiplist

    def get_max_ni(self):
        return self.max_ni

    def get_mail_to_auto_ni(self, bug):
        for field in ["assigned_to", "triage_owner"]:
            person = bug.get(field, "")
            if person and self.people.is_mozilla(person):
                return {"mail": person, "nickname": bug[f"{field}_detail"]["nick"]}

        return None

    def get_bz_params(self, date):
        fields = ["assigned_to", "triage_owner"]
        params = {
            "include_fields": fields,
            "resolution": "---",
            "f1": "keywords",
            "o1": "casesubstring",
            "v1": "meta",
            "f2": "days_elapsed",
            "o2": "greaterthan",
            "v2": self.nmonths * 30,
            "f3": "dependson",
            "o3": "isempty",
        }

        return params


if __name__ == "__main__":
    MetaNoDepsNoActivity().run()
