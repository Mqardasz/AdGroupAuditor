
from infra.ad_executor import AdExecutor
from infra.excel_fetcher import ExcelFetcher


class AuditService:

    @staticmethod
    def compare_user_groups(all_users: dict, reference_templates: dict):

        results = []

        for jobtitle, users in all_users.items():

            # Get template groups for this jobtitle
            template_groups = reference_templates.get(jobtitle, [])

            # Normalize template data:
            if isinstance(template_groups, str):
                template_groups = [template_groups]
            elif template_groups is None:
                template_groups = []
            elif not isinstance(template_groups, list):
                template_groups = list(template_groups)

            # for forbidden templates
            template_groups = [g for g in template_groups if g != "USER NOT FOUND"]

            for username, user_groups in users.items():

                #normalize user_groups
                if user_groups is None:
                    user_groups = []
                if not isinstance(user_groups, list):
                    user_groups = list(user_groups)

                # convert to sets for comparison
                user_set = set(user_groups)
                template_set = set(template_groups)

                missing = sorted(template_set - user_set)
                extra = sorted(user_set - template_set)

                results.append({
                    "jobtitle": jobtitle,
                    "user": username,
                    "missing": missing,
                    "extra": extra
                })

        return results
    fetcher = ExcelFetcher()
    compare_user_groups(AdExecutor.get_all_users_groups_grouped_by_jobtitle(fetcher.rows),
                        AdExecutor.get_reference_user_groups(fetcher.rows))

