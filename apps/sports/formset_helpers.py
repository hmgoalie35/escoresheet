from escoresheet.utils.formsets import BaseFormSetHelper


class SportRegistrationCreateFormSetHelper(BaseFormSetHelper):
    def get_extra_field_names(self):
        return ['sport', 'roles']